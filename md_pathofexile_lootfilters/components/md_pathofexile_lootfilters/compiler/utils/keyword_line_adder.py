from typing import List


class KeywordLineAdder:
    def __call__(self, lines: List[str], keyword: str, *values) -> None:
        parts = [str(v) for v in values if v is not None and v != ""]
        if parts:
            lines.append(f"\t{keyword} {' '.join(parts)}")
