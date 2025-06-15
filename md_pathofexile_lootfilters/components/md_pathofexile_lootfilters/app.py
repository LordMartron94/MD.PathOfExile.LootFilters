import time
import traceback
from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.cli_framework import CommandLineInterface
from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import CONFIG_DIR, CURRENT_LEAGUE
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.filter_constructor import \
    FilterConstructor
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.game_item_exporter import \
    GameItemExporter
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.game_item_repository import \
    GameItemRepository
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.ninja_client import \
    PoeNinjaClient
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.rarity_calculation.log_scaled_rarity_calculator import \
    LogScaledRarityCalculator


class App:
    """
    The main entry point of the application.
    """

    def __init__(self, logger: HoornLogger):
        self._logger: HoornLogger = logger
        self._separator: str = self.__class__.__name__

        self._cli: CommandLineInterface = CommandLineInterface(logger, exit_command=self._exit)
        self._initialize_commands()

        self._valid_bases = self._get_valid_base_types()

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def run(self) -> None:
        try:
            self._cli.start_listen_loop()
        except Exception as e:
            tb = traceback.format_exc()
            self._logger.critical(f"Something went terribly wrong, causing the application to crash! Restarting. Exception: \"{e}\"\n{tb}", separator=self._separator)
            time.sleep(1)
            return self.run()

    def _initialize_commands(self) -> None:
        self._cli.add_command(["build_filter", "bf"], description="Builds the filter.", action=self._build_filter)
        self._cli.add_command(["build_filter-update", "bf-u"], description="Builds the filter but first updates the economy-based items for proper tiering.", action=self._build_filter, arguments=[True])
        self._cli.add_command(["extract_items", "ei"], description="Extracts game items and assigns rarities based on the current league's economy.", action=self._extract_items)
        self._logger.debug("Successfully initialized CLI commands.", separator=self._separator)

    def _build_filter(self, update_economy_items: bool = False) -> None:
        filter_constructor = FilterConstructor(self._logger, self._valid_bases)

        if update_economy_items:
            self._extract_items()
            filter_constructor.reload_data()

        filter_constructor.construct_filter()

    def _get_valid_base_types(self) -> List[str]:
        client = PoeNinjaClient(self._logger)
        return client.fetch_valid_base_types()

    def _extract_items(self) -> None:
        client = PoeNinjaClient(self._logger)
        repo = GameItemRepository(self._logger, client, self._valid_bases, league=CURRENT_LEAGUE, item_types=
        {
            CONFIG_DIR / "uniques.csv":
            [
                "UniqueArmour", "UniqueWeapon", "UniqueAccessory",
                "UniqueJewel", "UniqueFlask", "UniqueMap", "UniqueRelic"
            ],
            CONFIG_DIR / "skill_gems.csv":
            [
                "SkillGem"
            ]
        })
        calculator = LogScaledRarityCalculator()
        exporter = GameItemExporter(self._logger, repo, calculator)
        exporter.export()

        self._logger.info(f"Successfully extracted game items.", separator=self._separator)

    def _exit(self) -> None:
        self._logger.save()
        time.sleep(0.5)
        exit()
