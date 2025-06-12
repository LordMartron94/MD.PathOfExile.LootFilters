from typing import Protocol, Dict, Any


class StyleConfigLoader(Protocol):
    def load(self) -> Dict[str, Any]:
        ...
