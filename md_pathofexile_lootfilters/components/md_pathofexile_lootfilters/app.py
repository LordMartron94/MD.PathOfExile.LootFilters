import time
import traceback

from md_pathofexile_lootfilters.components.md_common_python.py_common.cli_framework import CommandLineInterface
from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import CONFIG_DIR, CURRENT_LEAGUE
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.filter_constructor import \
    FilterConstructor
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.ninja_client import \
    PoeNinjaClient
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.rarity_calculation.log_scaled_rarity_calculator import \
    LogScaledRarityCalculator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.unique_item_exporter import \
    UniqueItemExporter
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.unique_item_repository import \
    UniqueItemRepository


class App:
    """
    The main entry point of the application.
    """

    def __init__(self, logger: HoornLogger):
        self._logger: HoornLogger = logger
        self._separator: str = self.__class__.__name__

        self._filter_constructor: FilterConstructor = FilterConstructor(logger)

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

    def _build_filter(self, update_uniques: bool = False) -> None:
        if update_uniques:
            self._extract_uniques()

        self._filter_constructor.construct_filter()

    def _initialize_commands(self) -> None:
        self._cli.add_command(["build_filter", "bf"], description="Builds the filter.", action=self._build_filter)
        self._cli.add_command(["build_filter-update", "bf-u"], description="Builds the filter but first updates the uniques for proper tiering.", action=self._build_filter, arguments=[True])
        self._cli.add_command(["extract_uniques", "eu"], description="Extracts uniques and assigns rarities based on the current league's economy.", action=self._extract_uniques)
        self._logger.debug("Successfully initialized CLI commands.", separator=self._separator)

    def _extract_uniques(self) -> None:
        output_path = CONFIG_DIR / "uniques.csv"

        client = PoeNinjaClient()
        repo = UniqueItemRepository(client, league=CURRENT_LEAGUE)
        calculator = LogScaledRarityCalculator()
        exporter = UniqueItemExporter(self._logger, repo, calculator)
        exporter.export(output_path)

        self._logger.info(f"Successfully extracted unique items to {output_path}.", separator=self._separator)

    def _exit(self) -> None:
        self._logger.save()
        time.sleep(0.5)
        exit()
