import time
import traceback
from pathlib import Path

from md_pathofexile_lootfilters.components.md_common_python.py_common.cli_framework import CommandLineInterface
from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.compiler import FilterCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import BlockFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.block import Block
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import OUTPUT_DIRECTORIES


class App:
    """
    The main entry point of the application.
    """

    def __init__(self, logger: HoornLogger):
        self._logger: HoornLogger = logger
        self._separator: str = self.__class__.__name__

        self._block_factory: BlockFactory = BlockFactory(logger)
        self._compiler: FilterCompiler = FilterCompiler(logger)

        self._cli: CommandLineInterface = CommandLineInterface(logger, exit_command=self._exit)
        self._initialize_commands()

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def run(self) -> None:
        try:
            self._cli.start_listen_loop()
        except Exception as e:
            tb = traceback.format_exc()
            self._logger.critical(f"Something went terribly wrong, causing the application to crash! Restarting. Exception: \"{e}\"\n{tb}", separator=self._separator)
            time.sleep(1)
            return self.run()

    def _test_basic_filter(self) -> None:
        catch_all_block: Block = self._block_factory.get_catch_all_block(BlockType.SHOW)
        transformed_str: str = self._compiler.transform(catch_all_block)

        for output_dir in OUTPUT_DIRECTORIES:
            filter_path: Path = output_dir / "MD.TestFilter.filter"

            try:
                with open(filter_path, "w") as filter_file:
                    filter_file.write(transformed_str)
            except Exception as e:
                tb = traceback.format_exc()
                self._logger.error(f"Something went wrong while outputting to \"{filter_path}\". Exception: \"{e}\"\n{tb}", separator=self._separator)

            self._logger.info(f"Output written to \"{filter_path}\".", separator=self._separator)

    def _initialize_commands(self) -> None:
        self._cli.add_command(["test_basic_filter", "tbf"], description="Tests the basic filter.", action=self._test_basic_filter)
        self._logger.debug("Successfully initialized CLI commands.", separator=self._separator)

    def _exit(self) -> None:
        self._logger.save()
        time.sleep(0.5)
        exit()
