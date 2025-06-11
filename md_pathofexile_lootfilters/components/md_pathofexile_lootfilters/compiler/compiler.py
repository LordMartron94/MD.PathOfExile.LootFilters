import pprint

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.block import Block
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class FilterCompiler:
    """
    Used to transform blocks and styling into an actual lootfilter file.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def transform_single_block(self, block: Block, style: Style) -> str:
        """
        Convert a single Block and its Style into the filter text.
        """
        self._log_inputs(block, style)

        lines: list[str] = [block.block_type.value]
        self._add_background_color(lines, style)
        self._add_border_color(lines, style)
        self._add_text_color(lines, style)
        self._add_font_size(lines, style)
        self._add_minimap_icon(lines, style)
        self._add_play_effect(lines, style)

        return self._assemble_output(lines)

    def _log_inputs(self, block: Block, style: Style) -> None:
        """
        Log block and style JSON for debugging.
        """
        block_json = pprint.pformat(block.model_dump(mode='json'))
        style_json = pprint.pformat(style.model_dump(mode='json'))
        self._logger.debug(
            f"Transforming single block:\n{block_json}\nStyle:\n{style_json}"
        )

    @staticmethod
    def _add_keyword_line(lines: list[str], keyword: str, *values) -> None:
        """
        Add a line with given keyword and values if none of the values are None.
        """
        lines.append(f"\t{keyword} {' '.join(str(v) for v in values)}")

    def _add_background_color(self, lines: list[str], style: Style) -> None:
        bg = style.background_color
        self._add_keyword_line(lines, "SetBackgroundColor", bg.red, bg.green, bg.blue, bg.alpha)

    def _add_border_color(self, lines: list[str], style: Style) -> None:
        bc = style.border_color
        self._add_keyword_line(lines, "SetBorderColor", bc.red, bc.green, bc.blue, bc.alpha)

    def _add_text_color(self, lines: list[str], style: Style) -> None:
        tc = style.text_color
        self._add_keyword_line(lines, "SetTextColor", tc.red, tc.green, tc.blue, tc.alpha)

    def _add_font_size(self, lines: list[str], style: Style) -> None:
        self._add_keyword_line(lines, "SetFontSize", style.font_size)

    def _add_minimap_icon(self, lines: list[str], style: Style) -> None:
        """
        Add MinimapIcon line when style.minimap_icon is present.
        """
        icon = style.minimap_icon
        if icon:
            self._add_keyword_line(lines, "MinimapIcon", icon.size, icon.colour, icon.shape)

    def _add_play_effect(self, lines: list[str], style: Style) -> None:
        """
        Add PlayEffect line when style.play_effect is present.
        """
        effect = style.play_effect
        if effect:
            token = effect.colour + ("Temp" if effect.temp else "")
            self._add_keyword_line(lines, "PlayEffect", token)

    @staticmethod
    def _assemble_output(lines: list[str]) -> str:
        """
        Join lines with newline, ensuring trailing newline at end.
        """
        return "\n".join(lines) + "\n"
