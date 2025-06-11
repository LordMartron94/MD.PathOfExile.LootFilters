from typing import Iterable


class QuotedValueListBuilder:
    @staticmethod
    def build(values: Iterable[str], quote: str = '"') -> str:
        return " ".join(f'{quote}{v}{quote}' for v in values)
