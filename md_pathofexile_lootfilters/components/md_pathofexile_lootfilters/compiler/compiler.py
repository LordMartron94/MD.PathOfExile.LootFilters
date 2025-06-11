from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.block import Block


class FilterCompiler:
    """
    Used to transform blocks and styling into an actual lootfilter file.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def transform(self, block: Block) -> str:
        return f"""{block.block_type.value}
    SetBackgroundColor 255 0 255 255
    SetBorderColor 0 255 255 255
    SetTextColor 0 0 0 255
    SetFontSize 45
"""
