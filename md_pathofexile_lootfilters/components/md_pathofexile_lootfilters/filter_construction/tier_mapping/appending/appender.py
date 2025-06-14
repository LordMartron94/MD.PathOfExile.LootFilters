from abc import abstractmethod
from typing import Protocol, List, Dict, Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory


class Appender(Protocol):
    @abstractmethod
    def append(
            self,
            rows_data: List,
            tier: ItemTier,
            tier_counts: Dict[str, int],
            data: FilterConstructionPipelineContext,
            base_type_accessor: Optional[str],
            base_type_category: BaseTypeCategory,
    ) -> List[Rule]:
        ...
