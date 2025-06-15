from collections import defaultdict
from typing import List, Dict

import numpy as np
import pandas as pd

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import DATA_DIR
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.appending.strategy.single_tier_base_types import \
    SingleTierBaseTypesAppendingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.constructing.strategy.raw_rarity_and_usefulness_strategy import \
    RawRarityAndUsefulnessMappingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.tier_rule_applier import \
    TierRuleApplier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    filter_rows_by_category, BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.print_tiers import \
    log_tiers
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class AddSkillGems(IPipe):
    def __init__(
            self,
            logger: HoornLogger,
            condition_factory: ConditionFactory,
            rule_factory: RuleFactory,
            tier_mapping_sorter: TierMappingSorter,
            pipeline_prefix: str,
            section_heading: str
    ):
        self._logger = logger
        self._separator = f"{pipeline_prefix}.{self.__class__.__name__}"

        self._condition_factory = condition_factory
        self._rule_factory = rule_factory
        self._tier_mapping_sorter = tier_mapping_sorter
        self._tier_rule_applier = TierRuleApplier(logger, rule_factory, condition_factory, tier_mapping_sorter)

        self._section_heading = section_heading
        self._section_description = (
            "Tiers the skill gems based on rarity and value."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        rules = self._get_rules(data)

        self._register_section(data, rules)

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data

    @staticmethod
    def _prepare_manual_df(data: FilterConstructionPipelineContext) -> pd.DataFrame:
        # just pull the rows; keep original column names including "Rarity (1-6)" and "Usefulness (1-6)"
        return filter_rows_by_category(BaseTypeCategory.skill_gems, data.base_type_data)

    @staticmethod
    def _prepare_economy_df(data: FilterConstructionPipelineContext) -> pd.DataFrame:
        econ = data.skill_gems_data.copy()
        # unify BaseType key
        econ = econ.rename(columns={"Base Type": "BaseType", "Rarity": "econ_rarity"})
        econ["econ_rarity"] = econ["econ_rarity"].astype(float)
        # linear scale from [1,12] into [1,6]
        econ["scaled_rarity__1_6"] = ((econ["econ_rarity"] - 1) * (5.0 / 11.0)) + 1.0
        econ["usefulness__1_6_econ"] = pd.NA
        return econ[["BaseType", "econ_rarity", "scaled_rarity__1_6", "usefulness__1_6_econ"]]

    @staticmethod
    def _merge_dataframes(manual: pd.DataFrame, econ: pd.DataFrame) -> pd.DataFrame:
        # outer join so we keep manual-only and econ-only entries
        return pd.merge(manual, econ, on="BaseType", how="outer")

    @staticmethod
    def _compute_final_columns(
            combined: pd.DataFrame,
            manual_df: pd.DataFrame
    ) -> pd.DataFrame:
        # 1) decide new rarity
        combined["rarity_calc"] = np.where(
            combined["econ_rarity"].notna(),
            np.where(
                combined["Rarity (1-6)"].notna(),
                combined["scaled_rarity__1_6"],  # both exist → scaled
                combined["econ_rarity"]          # econ-only → full 1-12
            ),
            combined["Rarity (1-6)"]             # manual-only
        )
        # 2) decide new usefulness
        combined["usefulness_calc"] = combined["Usefulness (1-6)"].fillna(
            combined["usefulness__1_6_econ"]
        )
        # 3) overwrite manual columns in-place
        combined["Rarity (1-6)"]    = combined["rarity_calc"]
        combined["Usefulness (1-6)"] = combined["usefulness_calc"]
        # 4) drop the economy & helper cols
        drop_cols = [
            "econ_rarity", "scaled_rarity__1_6",
            "usefulness__1_6_econ",
            "rarity_calc", "usefulness_calc"
        ]
        combined = combined.drop(columns=drop_cols)
        # 5) return only the original manual columns
        return combined[manual_df.columns]

    def _get_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        # A) prepare data
        manual_df   = self._prepare_manual_df(data)
        econ_df     = self._prepare_economy_df(data)
        merged      = self._merge_dataframes(manual_df, econ_df)
        final_df    = self._compute_final_columns(merged, manual_df)

        final_df = final_df.astype(object)
        final_df = final_df.replace({ np.nan: None })

        final_df.to_csv(DATA_DIR / "gems_intermediary_stats.csv", index=False)

        # B) apply tier rules
        rules: List[Rule] = []
        tier_counts: Dict[str, int] = defaultdict(int)

        self._tier_rule_applier.apply(
            final_df,
            data,
            BaseTypeCategory.skill_gems,
            tier_counts,
            rules,
            mapping_strategy=RawRarityAndUsefulnessMappingStrategy(self._logger),
            appender_strategy=SingleTierBaseTypesAppendingStrategy(
                self._rule_factory,
                self._condition_factory
            ),
            base_type_accessor="basetype",
            accessors={
                "rarity_accessor": "rarity__1_6",
                "usefulness_accessor": "usefulness__1_6"
            }
        )

        log_tiers(self._logger, tier_counts, self._separator, "Skill Gems")
        return rules

    def _register_section(
            self,
            data: FilterConstructionPipelineContext,
            rules: List[Rule]
    ) -> None:
        data.generated_rules.append(
            RuleSection(
                heading=self._section_heading,
                description=self._section_description,
                rules=rules
            )
        )
