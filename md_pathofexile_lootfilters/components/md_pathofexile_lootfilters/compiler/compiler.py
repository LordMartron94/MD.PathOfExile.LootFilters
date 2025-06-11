import pprint
from typing import List, Optional, Tuple

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.block import Block
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class FilterCompiler:
    """
    Used to transform blocks and styling into an actual lootfilter file.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def transform_single_block(
            self,
            block: Block,
            style: Optional[Style]
    ) -> str:
        """
        Convert a single Block and its optional Style into the filter text, including any conditions.
        """
        self._log_inputs(block, style)

        lines: List[str] = [block.block_type.value]

        self._add_conditions(lines, block.conditions)

        if style:
            self._add_background_color(lines, style)
            self._add_border_color(lines, style)
            self._add_text_color(lines, style)
            self._add_font_size(lines, style)
            self._add_minimap_icon(lines, style)
            self._add_play_effect(lines, style)
            self._add_play_alert_sound(lines, style)
            self._add_custom_alert_sound(lines, style)
            self._add_drop_sound_settings(lines, style)

        return self._assemble_output(lines)

    def transform_batch_blocks(
            self,
            blocks: List[Tuple[Block, Optional[Style]]]
    ) -> List[str]:
        output: List[str] = []
        for block, style in blocks:
            output.append(self.transform_single_block(block, style))
        return output

    def _log_inputs(self, block: Block, style: Optional[Style]) -> None:
        """
        Log block, conditions, and style for debugging.
        """
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
        """
        Add a line with given keyword and values if any values are present.
        """
        parts = [str(v) for v in values if v is not None and v != ""]
        if parts:
            lines.append(f"\t{keyword} {' '.join(parts)}")

    @staticmethod
    def _add_conditions(
            lines: List[str],
            conditions: List[Condition]
    ) -> None:
        """
        Add condition lines before styling.
        """
        for cond in conditions:
            kw = cond.keyword.value
            op = (cond.operator.value + ' ') if cond.operator else ''
            val = cond.value
            token = f"{kw} {op}{val}".strip()
            lines.append(f"\t{token}")

    def _add_background_color(self, lines: List[str], style: Style) -> None:
        bg = style.background_color
        self._add_keyword_line(lines, "SetBackgroundColor", bg.red, bg.green, bg.blue, bg.alpha)

    def _add_border_color(self, lines: List[str], style: Style) -> None:
        bc = style.border_color
        self._add_keyword_line(lines, "SetBorderColor", bc.red, bc.green, bc.blue, bc.alpha)

    def _add_text_color(self, lines: List[str], style: Style) -> None:
        tc = style.text_color
        self._add_keyword_line(lines, "SetTextColor", tc.red, tc.green, tc.blue, tc.alpha)

    def _add_font_size(self, lines: List[str], style: Style) -> None:
        self._add_keyword_line(lines, "SetFontSize", style.font_size)

    def _add_minimap_icon(self, lines: List[str], style: Style) -> None:
        if style.minimap_icon:
            mi = style.minimap_icon
            self._add_keyword_line(lines, "MinimapIcon", mi.size, mi.colour, mi.shape)

    def _add_play_effect(self, lines: List[str], style: Style) -> None:
        if style.play_effect:
            pe = style.play_effect
            token = pe.colour + ("Temp" if pe.temp else "")
            self._add_keyword_line(lines, "PlayEffect", token)

    def _add_play_alert_sound(self, lines: List[str], style: Style) -> None:
        if style.play_alert_sound:
            pas = style.play_alert_sound
            flag = "Positional" if pas.positional else None
            self._add_keyword_line(lines, "PlayAlertSound", pas.id, pas.volume, flag)

    def _add_custom_alert_sound(self, lines: List[str], style: Style) -> None:
        if style.custom_alert_sound:
            cas = style.custom_alert_sound
            flag = "Optional" if cas.optional else None
            self._add_keyword_line(lines, "CustomAlertSound", cas.file_name, cas.volume, flag)

    def _add_drop_sound_settings(self, lines: List[str], style: Style) -> None:
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
        """
        Join lines with newline, ensuring trailing newline.
        """
        return "\n".join(lines) + "\n"
