import pprint
from pathlib import Path
from typing import List, Any

import requests
from lupa.lua54 import LuaRuntime

from md_pathofexile_lootfilters.components.md_common_python.py_common.handlers import FileHandler
from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import PATH_OF_BUILDING_DATA_DIR


def _stub_shared_api(lua: LuaRuntime):
    # Provide minimal stubs for Generated.lua dependencies
    lua.execute('function isValueInTable(_) return false end')


class PoeNinjaClient:
    """
    Client for fetching valid base types, including those in Programmatically Generated Lua.
    """
    def __init__(
            self,
            logger: HoornLogger,
            base_url: str = "https://poe.ninja/api/data/itemoverview"
    ):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._base_url = base_url
        self._lua = LuaRuntime()
        _stub_shared_api(self._lua)
        self._paths = self._gather_data_paths()
        self._logger.info(
            f"Data paths collected: {[p.name for p in self._paths]}",
            separator=self._separator
        )

    def _gather_data_paths(self) -> List[Path]:
        gems = PATH_OF_BUILDING_DATA_DIR / "Gems.lua"
        uniques_dir = PATH_OF_BUILDING_DATA_DIR / "Uniques"
        special_dir = uniques_dir / "Special"
        new_file = special_dir / "New.lua"
        gen_file = special_dir / "Generated.lua"

        handler = FileHandler()
        unique_files = handler.get_children_paths_fast(
            uniques_dir, extensions=".lua", recursive=False
        )

        candidates = [gems] + unique_files + [new_file, gen_file]
        existing: List[Path] = []
        for p in candidates:
            if p.exists():
                existing.append(p)
            else:
                self._logger.warning(
                    f"Missing data file: {p}", separator=self._separator
                )
        return existing

    def fetch_valid_base_types(self) -> List[str]:
        self._logger.info("Starting valid base type extraction...", separator=self._separator)
        collected: List[str] = []

        for path in self._paths:
            name_lower = path.name.lower()
            # Determine loader based on file content
            if name_lower == "generated.lua":
                entries = self._load_generated_entries(path)
                names = [self._parse_entry(e, path) for e in entries]
            elif name_lower == "new.lua":
                entries = self._load_new_entries(path)
                names = [self._parse_entry(e, path) for e in entries]
            else:
                tbl = self._load_returning_table(path)
                names = self._extract_names_from_table(tbl, path)

            unique_names = list(dict.fromkeys(filter(None, names)))
            collected.extend(unique_names)
            self._logger.info(
                f"Loaded {len(unique_names)} types from {path.name}",
                separator=self._separator
            )

        final = list(dict.fromkeys(collected))
        self._logger.info(
            f"Total valid base types extracted: {len(final)}", separator=self._separator
        )
        return final

    def fetch_game_items(self, league: str, item_type: str) -> dict:
        self._logger.debug(
            f"Fetching game items for type '{item_type}' in league '{league}'",
            separator=self._separator
        )
        resp = requests.get(self._base_url, params={"league": league, "type": item_type})
        resp.raise_for_status()
        return resp.json()

    def _load_returning_table(self, path: Path) -> Any:
        """
        Execute a Lua file that returns its top-level table via 'return'.
        """
        code = path.read_text(encoding="utf-8")
        return self._lua.execute(code)

    def _load_generated_entries(self, path: Path) -> List[str]:
        """
        Execute Programmatically Generated Lua and return the 'data.uniques.generated' table.
        """
        # Initialize environment with all the tables that Generated.lua will iterate over:
        init = r"""
                data = {
                  uniques    = { generated = {} },
                  veiledMods = {},
                  clusterJewels = { notableSortOrder = {} },
                  uniqueMods = {
                    ["Watcher's Eye"] = {},
                    ["Sublime Vision"] = {},
                    ["Vorana's March"] = {}
                  },
                  gems = {}
                }
        
                -- stub out the two helper functions the generated code calls:
                function isValueInTable(_)    return false end
                function isValueInArray(_,_)  return false end
        
                -- stub out Module loading so the charms section doesn't blow up
                function LoadModule(_)        return {} end
                """
        self._lua.execute(init)
        code = path.read_text(encoding="utf-8")
        self._lua.execute(code)
        gen = self._lua.globals().data.uniques.generated
        count = len(gen)
        self._logger.debug(
            f"Generated entries loaded: {count} from {path.name}",
            separator=self._separator
        )
        return [gen[i] for i in range(1, count + 1)]

    def _load_new_entries(self, path: Path) -> List[str]:
        # Initialize environment
        self._lua.execute('data = { uniques = { new = {} } }')
        code = path.read_text(encoding="utf-8")
        self._lua.execute(code)
        gen = self._lua.globals().data.uniques.new
        count = len(gen)
        self._logger.debug(
            f"New entries loaded: {count} from {path.name}",
            separator=self._separator
        )
        return [gen[i] for i in range(1, count + 1)]

    def _extract_names_from_table(self, table: Any, source: Path) -> List[str]:
        names: List[str] = []
        for key in table.keys():
            entry = table[key]
            name = self._parse_entry(entry, source)
            if name is not None and name != "":
                names.append(name)
        return names

    def _parse_entry(self, entry: Any, source: Path) -> str:
        # If it's a raw Lua string, parse as before
        if isinstance(entry, str):
            lines = [l.strip() for l in entry.splitlines()
                     if l.strip() and not l.startswith('--')]
            return lines[1] if len(lines) > 1 else ""

        entry_dict = dict(entry)

        # Otherwise it's a Lua table–style object
        # 1. Try the baseTypeName, 2. if that's empty use the name field
        base_type = getattr(entry, "baseTypeName", None)
        name = getattr(entry, "name", None)

        if not base_type and name:
            name = name + " Support"

        base = base_type or name

        variant = getattr(entry, "variantId", "")

        if not base:
            self._logger.warning(f"Rejected: {base} -> {source.name} | (reason: no name)\n{pprint.pformat(entry_dict)}", separator=self._separator)
            return ""

        if "alt" in variant.lower():
            self._logger.warning(f"Rejected: {base} -> {source.name} | (reason: variant)\n{pprint.pformat(entry_dict)}", separator=self._separator)
            return ""

        self._logger.debug(f"Added: {base} -> {source.name}\n{pprint.pformat(entry_dict)}", separator=self._separator)

        return base
