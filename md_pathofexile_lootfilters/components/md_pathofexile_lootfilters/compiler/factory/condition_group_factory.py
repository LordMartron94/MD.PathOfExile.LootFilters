from typing import List, Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act, AREA_LEVEL_LOOKUP


class ConditionGroupFactory:
    """
    Utility for composing lists of Condition objects, combining a primary condition
    with optional extra conditions (e.g., area-level constraints).
    """

    @staticmethod
    def from_exact_values(
            condition_factory: ConditionFactory,
            keyword: ConditionKeyWord,
            values: List[str],
            operator: ConditionOperator = ConditionOperator.exact_match,
            extra_conditions: Optional[List[Condition]] = None
    ) -> List[Condition]:
        """
        Builds a base condition matching an exact list of values, plus any extras.
        Example:
            base = from_exact_values(factory, Class, ['A', 'B'], extra=[...])
        """
        quoted_values = " ".join(f'"{v}"' for v in values)
        base = condition_factory.create_condition(
            keyword,
            operator=operator,
            value=quoted_values
        )
        group: List[Condition] = [base]
        if extra_conditions:
            group.extend(extra_conditions)
        return group

    @staticmethod
    def for_act_area_levels(
            condition_factory: ConditionFactory,
            act: Act
    ) -> List[Condition]:
        """
        Retrieves the list of conditions constraining area levels for a given Act.
        """
        max_level = AREA_LEVEL_LOOKUP[act]
        return condition_factory.create_complex_area_level_condition(
            min_area_level=0,
            max_area_level=max_level
        )
