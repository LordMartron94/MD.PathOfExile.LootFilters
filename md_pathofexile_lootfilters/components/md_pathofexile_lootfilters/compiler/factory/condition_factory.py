from typing import Any, Optional, List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition, \
    ConditionOperator, ConditionKeyWord


class ConditionFactory:
    """
    Factory for constructing Condition instances.
    """

    @staticmethod
    def create_condition(
            keyword: ConditionKeyWord,
            operator: Optional[ConditionOperator],
            value: Any
    ) -> Condition:
        """
        Create a Condition instance with the given enum values.

        :param keyword: one of the ConditionKeyWord enums
        :param operator: one of the ConditionOperator enums
        :param value: the comparison value (type depends on keyword)
        :return: a validated Condition instance
        """
        return Condition(keyword=keyword, operator=operator, value=value)

    def create_area_level_condition(self, max_area_level: int) -> Condition:
        return self.create_condition(
            keyword=ConditionKeyWord.AreaLevel,
            operator=ConditionOperator.less_than_or_equal,
            value=max_area_level
        )

    def create_complex_area_level_condition(self, min_area_level: int, max_area_level: int) -> List[Condition]:
        min_cond = self.create_condition(
            keyword=ConditionKeyWord.AreaLevel,
            operator=ConditionOperator.greater_than_or_equal,
            value=min_area_level
        )

        max_cond = self.create_area_level_condition(max_area_level)

        return [min_cond, max_cond]
