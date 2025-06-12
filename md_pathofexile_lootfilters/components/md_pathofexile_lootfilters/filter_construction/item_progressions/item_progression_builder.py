import enum
from typing import List, Dict, Optional

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
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class ItemProgressionBuilder:
    """
    Orchestrates creation of progression rules for items and class filters,
    with optional extra conditions for each rarity's showing.
    """

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
            styles: Dict[str, Style],
            rarity_extra_conditions: Optional[Dict[str, List[Condition]]] = None,
    ) -> List[Rule]:
        """
        Build rules for each progression item (Magic/Rare)
        and the class-level Normal show/exclude rules.

        rarity_extra_conditions: optional mapping from rarity name to extra Condition instances.
        """
        extra_conditions = rarity_extra_conditions or {}
        rules: List[Rule] = []
        for item in items:
            rules.extend(
                self._build_item_rarity_rules(item, styles, extra_conditions)
            )

        rules.append(self._build_class_show_rule(associated_class, styles["Normal"]))
        rules.append(self._build_class_exclude_rule(associated_class))
        return rules

    def _build_item_rarity_rules(
            self,
            item: ItemProgressionItem,
            styles: Dict[str, Style],
            extra_conditions: Dict[str, List],
    ) -> List[Rule]:
        """Generate SHOW rules for Magic and Rare variants of a base-type + level-range, including any extra conditions."""
        # common conditions
        base = self._condition_factory.create_condition(
            ConditionKeyWord.BaseType, operator=None, value=item.base_type.value
        )
        level_min = self._condition_factory.create_condition(
            ConditionKeyWord.ItemLevel,
            operator=ConditionOperator.greater_than_or_equal,
            value=item.start_level,
        )
        level_max = self._condition_factory.create_condition(
            ConditionKeyWord.ItemLevel,
            operator=ConditionOperator.less_than_or_equal,
            value=item.end_level,
        )

        rules: List[Rule] = []
        for rarity in ("Magic", "Rare"):
            rarity_cond = self._condition_factory.create_condition(
                ConditionKeyWord.Rarity, operator=None, value=rarity
            )
            # assemble conditions, appending any extras for this rarity
            conditions = [base, rarity_cond, level_min, level_max]
            additional = extra_conditions.get(rarity, [])
            conditions.extend(additional)

            rules.append(
                self._rule_factory.get_rule(
                    RuleType.SHOW,
                    conditions,
                    styles[rarity],
                )
            )
        return rules

    def _build_class_show_rule(
            self,
            associated_class: enum.Enum,
            normal_style: Style,
    ) -> Rule:
        """Show Normal items in the early acts for this class."""
        class_cond = self._condition_factory.create_condition(
            ConditionKeyWord.Class, operator=None, value=associated_class.value
        )
        act_conditions = ConditionGroupFactory.for_act_area_levels(
            self._condition_factory, Act.Act1
        )
        rarity_normal = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            ConditionKeyWord.Rarity,
            values=["Normal"],
        )
        return self._rule_factory.get_rule(
            RuleType.SHOW,
            [class_cond] + act_conditions + rarity_normal,
            normal_style,
            )

    def _build_class_exclude_rule(
            self,
            associated_class: enum.Enum,
    ) -> Rule:
        """Hide items outside act range or with undesired rarities."""
        class_cond = self._condition_factory.create_condition(
            ConditionKeyWord.Class, operator=None, value=associated_class.value
        )
        exclude_areas = ConditionGroupFactory.between_acts(
            self._condition_factory, Act.Act2, Act.Act10
        )
        exclude_rarities = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            ConditionKeyWord.Rarity,
            values=["Normal", "Magic", "Rare"],
        )
        return self._rule_factory.get_rule(
            RuleType.HIDE,
            exclude_areas + exclude_rarities + [class_cond],
            style=None,
            )
