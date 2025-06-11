from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.rendering.renderer import Renderer
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.utils.keyword_line_adder import KeywordLineAdder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class StyleRenderer(Renderer):
    """
    Renders styling directives for a lootfilter rule by delegating to smaller helper methods.
    """
    def __init__(self, keyword_line_adder: KeywordLineAdder):
        self._adder = keyword_line_adder

    def render(self, lines: List[str], rule: Rule) -> None:
        style = rule.style
        if not style:
            return

        self._render_basic_colors(lines, style)
        self._render_optional_icon(lines, style)
        self._render_effect(lines, style)
        self._render_sounds(lines, style)
        self._render_drop_toggles(lines, style)

    def _render_basic_colors(self, lines: List[str], style: Style) -> None:
        bg = style.background_color
        tc = style.text_color
        bd = style.border_color
        self._adder(lines, "SetBackgroundColor", bg.red, bg.green, bg.blue, bg.alpha)
        self._adder(lines, "SetBorderColor", bd.red, bd.green, bd.blue, bd.alpha)
        self._adder(lines, "SetTextColor", tc.red, tc.green, tc.blue, tc.alpha)
        self._adder(lines, "SetFontSize", style.font_size)

    def _render_optional_icon(self, lines: List[str], style: Style) -> None:
        icon = style.minimap_icon
        if icon:
            self._adder(lines, "MinimapIcon", icon.size, icon.colour, icon.shape)

    def _render_effect(self, lines: List[str], style: Style) -> None:
        pe = style.play_effect
        if pe:
            token = pe.colour + ("Temp" if pe.temp else "")
            self._adder(lines, "PlayEffect", token)

    def _render_sounds(self, lines: List[str], style: Style) -> None:
        pas = style.play_alert_sound
        if pas:
            flag = "Positional" if pas.positional else None
            self._adder(lines, "PlayAlertSound", pas.id, pas.volume, flag)

        cas = style.custom_alert_sound
        if cas:
            flag = "Optional" if cas.optional else None
            self._adder(lines, "CustomAlertSound", cas.file_name, cas.volume, flag)

    def _render_drop_toggles(self, lines: List[str], style: Style) -> None:
        if style.disable_drop_sound:
            self._adder(lines, "DisableDropSound")
        if style.enable_drop_sound:
            self._adder(lines, "EnableDropSound")
        if style.disable_drop_sound_if_alert_sound:
            self._adder(lines, "DisableDropSoundIfAlertSound")
        if style.enable_drop_sound_if_alert_sound:
            self._adder(lines, "EnableDropSoundIfAlertSound")
