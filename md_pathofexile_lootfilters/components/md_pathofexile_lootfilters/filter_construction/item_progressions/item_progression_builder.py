import enum
from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.configs import \
    ClassRuleConfig, RarityRuleConfig, ItemProgressionConfig
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem


class ItemProgressionBuilder:
    def __init__(
            self,
            condition_factory: ConditionFactory,
            rule_factory: RuleFactory,
    ):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory

    def build(
            self,
            items: List[ItemProgressionItem],
            associated_class: enum.Enum,
            config: ItemProgressionConfig,
    ) -> List[Rule]:
        rules: List[Rule] = []
        for item in items:
            for rc in config.rarity_rules:
                rules.append(self._make_item_rule(item, rc))

        rules.extend(self._make_class_show(associated_class, config.class_rule))
        rules.append(self._make_class_hide(associated_class, config.class_rule))

        if config.appendix_rules:
            rules.extend(config.appendix_rules)

        return rules

    def _make_item_rule(
            self,
            item: ItemProgressionItem,
            rc: RarityRuleConfig,
        ) -> Rule:
        # 1. Validate inputs
        self._validate_item_start(item)

        # 2. Build core conditions
        base_cond = self._create_base_condition(item)
        rarity_cond = self._create_rarity_condition(rc)
        lvl_min, lvl_max = self._create_level_conditions(item)
        act_conds = self._create_act_conditions(rc)

        # 3. Combine all conditions and return the rule
        all_conditions = [base_cond, rarity_cond, lvl_min, lvl_max] + act_conds + rc.extra_conditions
        return self._rule_factory.get_rule(RuleType.SHOW, all_conditions, rc.style)

    @staticmethod
    def _validate_item_start(item: ItemProgressionItem) -> None:
        """Ensure exactly one of start_level or start_area is provided."""
        has_level = item.start_level is not None
        has_area = item.start_area is not None
        if has_level == has_area:
            raise ValueError("Exactly one of start_level or start_area must be specified")

    def _create_base_condition(self, item: ItemProgressionItem) -> Condition:
        """Create the base-type condition."""
        return self._condition_factory.create_condition(
            ConditionKeyWord.BaseType,
            operator=None,
            value=f'"{item.base_type if isinstance(item.base_type, str) else item.base_type.value}"',
        )

    def _create_rarity_condition(self, rc: RarityRuleConfig) -> Condition:
        """Create the rarity condition."""
        return self._condition_factory.create_condition(
            ConditionKeyWord.Rarity,
            operator=None,
            value=rc.rarity_name,
        )

    def _create_level_conditions(
            self,
            item: ItemProgressionItem,
    ) -> tuple[Condition, Condition]:
        """Create the minimum and maximum level or area conditions."""
        if item.start_level is not None:
            key = ConditionKeyWord.ItemLevel
            start, end = item.start_level, item.end_level
        else:
            key = ConditionKeyWord.AreaLevel
            start, end = item.start_area, item.end_area

        lvl_min = self._condition_factory.create_condition(
            key,
            operator=ConditionOperator.greater_than_or_equal,
            value=start,
        )
        lvl_max = self._condition_factory.create_condition(
            key,
            operator=ConditionOperator.less_than_or_equal,
            value=end,
        )
        return lvl_min, lvl_max

    def _create_act_conditions(
            self,
            rc: RarityRuleConfig,
    ) -> list[Condition]:
        """Optionally create act-based conditions if acts are specified."""
        if not rc.acts:
            return []
        return ConditionGroupFactory.between_acts(
            self._condition_factory,
            rc.acts[0],
            rc.acts[1],
        )

    def _make_class_show(
            self,
            associated_class: enum.Enum,
            crc: ClassRuleConfig,
    ) -> List[Rule]:
        cls_cond = self._condition_factory.create_condition(
            ConditionKeyWord.Class, operator=None, value=associated_class.value
        )

        act_group = ConditionGroupFactory.between_acts(
            self._condition_factory,
            crc.show_acts[0],
            crc.show_acts[1],
        )

        rules: List[Rule] = []

        for rarity, style in crc.show_rarities.items():
            show_rarity_group = ConditionGroupFactory.from_exact_values(
                self._condition_factory,
                ConditionKeyWord.Rarity,
                values=[rarity],
            )

            rules.append(self._rule_factory.get_rule(
                RuleType.SHOW,
                [cls_cond] + show_rarity_group + act_group,
                style,
                )
            )

        return rules

    def _make_class_hide(
            self,
            associated_class: enum.Enum,
            crc: ClassRuleConfig,
    ) -> Rule:
        cls_cond = self._condition_factory.create_condition(
            ConditionKeyWord.Class, operator=None, value=associated_class.value
        )
        hide_group = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            ConditionKeyWord.Rarity,
            values=crc.hide_rarities,
        )
        hide_act_group = ConditionGroupFactory.between_acts(
            self._condition_factory,
            crc.hide_acts[0],
            crc.hide_acts[1],
        )
        return self._rule_factory.get_rule(
            RuleType.HIDE,
            hide_group + hide_act_group + [cls_cond],
            style=None,
            )
