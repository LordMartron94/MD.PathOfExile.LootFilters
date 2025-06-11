from typing import List, Optional, Tuple

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class ShowHideRuleBuilder:
    """
    Builds a pair of SHOW and HIDE Rule objects given rule_factory,
    sets of conditions, and optional styles.
    """

    @staticmethod
    def build(
            rule_factory: RuleFactory,
            show_conditions: List[Condition],
            hide_conditions: List[Condition],
            show_style: Optional[Style],
            hide_style: Optional[Style] = None
    ) -> Tuple[Rule, Rule]:
        """
        Returns (show_rule, hide_rule).

        - show_rule uses RuleType.SHOW with show_conditions and show_style
        - hide_rule uses RuleType.HIDE with hide_conditions and hide_style
        """
        show_rule = rule_factory.get_rule(
            RuleType.SHOW,
            conditions=show_conditions,
            style=show_style
        )
        hide_rule = rule_factory.get_rule(
            RuleType.HIDE,
            conditions=hide_conditions,
            style=hide_style
        )

        return show_rule, hide_rule
