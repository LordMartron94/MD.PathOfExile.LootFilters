from typing import Dict, Any

from md_pathofexile_lootfilters.components.md_common_python.py_common.json_storage import JsonStorageHandler


class JsonStyleConfigLoader:
    def __init__(self, storage: JsonStorageHandler) -> None:
        self._storage = storage

    def load(self) -> Dict[str, Any]:
        return self._storage.read()
