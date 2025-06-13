from typing import List, Tuple

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import FlaskTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    get_item_progression_for_category, BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_flask_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.quoted_value_list_builder import \
    QuotedValueListBuilder


class FlaskProgressionBuilder:
    def __init__(
            self,
            condition_factory: ConditionFactory,
            rule_factory: RuleFactory,
    ):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory

    def get_progression_rules(
            self,
            data: FilterConstructionPipelineContext,
    ) -> List[Rule]:
        """
        Build SHOW and HIDE rules for all flask progression groups.
        """
        _progressions = get_item_progression_for_category(BaseTypeCategory.life_flasks, data.base_type_data)
        _hybrid_progressions = get_item_progression_for_category(BaseTypeCategory.hybrid_flasks, data.base_type_data)
        _utility_progressions = get_item_progression_for_category(BaseTypeCategory.utility_flasks, data.base_type_data)

        normal_style = determine_flask_style(data)
        utility_style = determine_flask_style(data, is_utility_flask=True)

        rules: List[Rule] = []

        # Normal
        class_condition = self._build_class_condition((FlaskTypeClass.Life, FlaskTypeClass.Mana))
        rules.extend(self._build_show_rules(class_condition, _progressions, normal_style))
        rules.append(self._build_hide_rule(class_condition))

        # Hybrid
        class_condition = self._build_class_condition((FlaskTypeClass.Hybrid,))
        rules.extend(self._build_show_rules(class_condition, _hybrid_progressions, utility_style))
        rules.append(self._build_hide_rule(class_condition))

        # Utility
        class_condition = self._build_class_condition((FlaskTypeClass.Utility,))
        rules.extend(self._build_show_rules(class_condition, _utility_progressions, utility_style))
        rules.append(self._build_hide_rule(class_condition))

        return rules

    def _build_class_condition(self, classes: Tuple[FlaskTypeClass, ...]) -> Condition:
        return self._condition_factory.create_condition(
            ConditionKeyWord.Class,
            operator=ConditionOperator.exact_match,
            value=QuotedValueListBuilder.build([flask_class.value for flask_class in classes]),
        )

    def _build_show_rules(
            self,
            class_condition: Condition,
            progression: List[ItemProgressionItem],
            style,
    ) -> List[Rule]:
        show_rules: List[Rule] = []
        for item in progression:
            base_cond = self._condition_factory.create_condition(
                ConditionKeyWord.BaseType,
                operator=None,
                value=f'"{item.base_type}"',
            )
            area_cond = self._condition_factory.create_area_level_condition(item.end_area)
            show_rules.append(
                self._rule_factory.get_rule(
                    RuleType.SHOW,
                    [class_condition, base_cond, area_cond],
                    style=style,
                )
            )
        return show_rules

    def _build_hide_rule(self, class_condition: Condition) -> Rule:
        hide_conditions = ConditionGroupFactory.between_acts(
            self._condition_factory,
            Act.Act1,
            Act.Act10,
        ) + [class_condition]
        return self._rule_factory.get_rule(
            RuleType.HIDE,
            hide_conditions,
            style=None
        )
