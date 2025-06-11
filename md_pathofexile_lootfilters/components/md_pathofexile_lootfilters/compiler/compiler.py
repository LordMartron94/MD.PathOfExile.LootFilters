import pprint
from typing import List, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class FilterCompiler:
    """
    Used to transform rules (with optional nested sub-rules) and styling into lootfilter text.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def transform_single_block(
            self,
            rule: Rule
    ) -> str:
        """
        Convert a Rule and its Style into filter text, including nested sub-rules.

        If a sub_rule is present, a 'Continue' line is emitted so matching continues into the nested block.
        """
        style = rule.style
        self._log_inputs(rule, style)

        lines: List[str] = [rule.block_type.value]

        # primary conditions
        self._add_conditions(lines, rule.conditions)

        if style:
            self._add_styling(lines, style)

        return self._assemble_output(lines)

    def transform_batch_blocks(
            self,
            rules: List[Rule]
    ) -> List[str]:
        output: List[str] = []
        for rule in rules:
            output.append(self.transform_single_block(rule))
        return output

    def _log_inputs(self, block: Rule, style: Optional[Style]) -> None:
        block_json = pprint.pformat(block.model_dump(mode='json'))
        style_json = pprint.pformat(style.model_dump(mode='json')) if style else None
        self._logger.debug(
            f"Transforming block:\n{block_json}\nStyle:\n{style_json}",
            separator=self._separator
        )

    @staticmethod
    def _add_keyword_line(
            lines: List[str],
            keyword: str,
            *values
    ) -> None:
        # only include non-empty values
        parts = [str(v) for v in values if v is not None and v != ""]
        if parts:
            lines.append(f"\t{keyword} {' '.join(parts)}")

    @staticmethod
    def _add_conditions(
            lines: List[str],
            conditions: List[Condition]
    ) -> None:
        for cond in conditions:
            kw = cond.keyword.value
            op = f"{cond.operator.value} " if cond.operator else ''
            token = f"{kw} {op}{cond.value}".strip()
            lines.append(f"\t{token}")

    def _add_styling(self, lines: List[str], style: Style) -> None:
        # colors and font
        bg = style.background_color
        self._add_keyword_line(lines, "SetBackgroundColor", bg.red, bg.green, bg.blue, bg.alpha)
        bc = style.border_color
        self._add_keyword_line(lines, "SetBorderColor", bc.red, bc.green, bc.blue, bc.alpha)
        tc = style.text_color
        self._add_keyword_line(lines, "SetTextColor", tc.red, tc.green, tc.blue, tc.alpha)
        self._add_keyword_line(lines, "SetFontSize", style.font_size)

        # optional minimap icon
        if style.minimap_icon:
            mi = style.minimap_icon
            self._add_keyword_line(lines, "MinimapIcon", mi.size, mi.colour, mi.shape)

        # optional play effect
        if style.play_effect:
            pe = style.play_effect
            token = pe.colour + ("Temp" if pe.temp else "")
            self._add_keyword_line(lines, "PlayEffect", token)

        # optional alert sounds
        if style.play_alert_sound:
            pas = style.play_alert_sound
            flag = "Positional" if pas.positional else None
            self._add_keyword_line(lines, "PlayAlertSound", pas.id, pas.volume, flag)
        if style.custom_alert_sound:
            cas = style.custom_alert_sound
            flag = "Optional" if cas.optional else None
            self._add_keyword_line(lines, "CustomAlertSound", cas.file_name, cas.volume, flag)

        # drop sound toggles
        if style.disable_drop_sound:
            self._add_keyword_line(lines, "DisableDropSound")
        if style.enable_drop_sound:
            self._add_keyword_line(lines, "EnableDropSound")
        if style.disable_drop_sound_if_alert_sound:
            self._add_keyword_line(lines, "DisableDropSoundIfAlertSound")
        if style.enable_drop_sound_if_alert_sound:
            self._add_keyword_line(lines, "EnableDropSoundIfAlertSound")

    @staticmethod
    def _assemble_output(lines: List[str]) -> str:
        return "\n".join(lines) + "\n"
