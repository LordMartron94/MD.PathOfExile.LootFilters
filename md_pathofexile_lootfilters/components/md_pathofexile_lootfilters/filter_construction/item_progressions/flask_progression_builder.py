from typing import List, Tuple

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.flask_base_type import FlaskBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_flask_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.quoted_value_list_builder import \
    QuotedValueListBuilder


class FlaskProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory

        self._item_progression: List[Tuple[List[str], ItemProgressionItem]] = [
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Small,      start_area=0, end_area=9)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Medium,     start_area=0, end_area=13)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Large,      start_area=0, end_area=17)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Greater,    start_area=0, end_area=19)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Grand,      start_area=0, end_area=25)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Giant,      start_area=0, end_area=31)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Colossal,   start_area=0, end_area=37)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Sacred,     start_area=0, end_area=43)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Hallowed,   start_area=0, end_area=51)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Sanctified, start_area=0, end_area=60)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Divine,     start_area=0, end_area=68)),
            (["Life Flasks", "Mana Flasks"],
             ItemProgressionItem(base_type=FlaskBaseType.Eternal,    start_area=0, end_area=68)),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        style = determine_flask_style(data)

        rules: List[Rule] = []

        classes = self._item_progression[0][0]
        class_condition = self._condition_factory.create_condition(ConditionKeyWord.Class, operator=ConditionOperator.exact_match, value=QuotedValueListBuilder.build(classes))

        for _, item_progression in self._item_progression:
            base_type_condition = self._condition_factory.create_condition(ConditionKeyWord.BaseType, operator=None, value=f'"{item_progression.base_type.value}"')
            area_level_condition = self._condition_factory.create_area_level_condition(item_progression.end_area)
            rules.append(self._rule_factory.get_rule(RuleType.SHOW, conditions=[class_condition, base_type_condition, area_level_condition], style=style))

        hide_act_group = ConditionGroupFactory.between_acts(
            self._condition_factory,
            Act.Act1,
            Act.Act10,
        )
        rules.append(self._rule_factory.get_rule(
            RuleType.HIDE,
            hide_act_group + [class_condition],
            style=None,
            ))

        return rules
