from typing import List, Tuple, Dict

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.flask_base_type import FlaskBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import determine_flask_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.quoted_value_list_builder import QuotedValueListBuilder


class FlaskProgressionBuilder:
    def __init__(
            self,
            condition_factory: ConditionFactory,
            rule_factory: RuleFactory,
    ):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory
        # progression per flask class group
        self._progressions: Dict[Tuple[str, ...], List[ItemProgressionItem]] = {
            ("Life Flasks", "Mana Flasks"): [
                ItemProgressionItem(base_type=FlaskBaseType.Small,      start_area=0, end_area=9),
                ItemProgressionItem(base_type=FlaskBaseType.Medium,     start_area=0, end_area=13),
                ItemProgressionItem(base_type=FlaskBaseType.Large,      start_area=0, end_area=17),
                ItemProgressionItem(base_type=FlaskBaseType.Greater,    start_area=0, end_area=19),
                ItemProgressionItem(base_type=FlaskBaseType.Grand,      start_area=0, end_area=25),
                ItemProgressionItem(base_type=FlaskBaseType.Giant,      start_area=0, end_area=31),
                ItemProgressionItem(base_type=FlaskBaseType.Colossal,   start_area=0, end_area=37),
                ItemProgressionItem(base_type=FlaskBaseType.Sacred,     start_area=0, end_area=43),
                ItemProgressionItem(base_type=FlaskBaseType.Hallowed,   start_area=0, end_area=51),
                ItemProgressionItem(base_type=FlaskBaseType.Sanctified, start_area=0, end_area=60),
                ItemProgressionItem(base_type=FlaskBaseType.Divine,     start_area=0, end_area=68),
                ItemProgressionItem(base_type=FlaskBaseType.Eternal,    start_area=0, end_area=68),
            ],
            ("Hybrid Flasks",): [
                ItemProgressionItem(base_type=FlaskBaseType.Small,      start_area=0, end_area=20),
                ItemProgressionItem(base_type=FlaskBaseType.Medium,     start_area=0, end_area=30),
                ItemProgressionItem(base_type=FlaskBaseType.Large,      start_area=0, end_area=40),
                ItemProgressionItem(base_type=FlaskBaseType.Colossal,   start_area=0, end_area=50),
                ItemProgressionItem(base_type=FlaskBaseType.Sacred,     start_area=0, end_area=60),
                ItemProgressionItem(base_type=FlaskBaseType.Hallowed,   start_area=0, end_area=67),
            ],
        }

    def get_progression_rules(
            self,
            data: FilterConstructionPipelineContext,
    ) -> List[Rule]:
        """
        Build SHOW and HIDE rules for all flask progression groups.
        """
        style = determine_flask_style(data)
        rules: List[Rule] = []

        for classes, progression in self._progressions.items():
            class_condition = self._build_class_condition(classes)
            rules.extend(self._build_show_rules(class_condition, progression, style))
            rules.append(self._build_hide_rule(class_condition))

        return rules

    def _build_class_condition(self, classes: Tuple[str, ...]) -> Condition:
        return self._condition_factory.create_condition(
            ConditionKeyWord.Class,
            operator=ConditionOperator.exact_match,
            value=QuotedValueListBuilder.build(classes),
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
                value=f'"{item.base_type.value}"',
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
