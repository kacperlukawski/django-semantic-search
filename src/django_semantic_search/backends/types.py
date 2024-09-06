from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class Distance(str, Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"


@dataclass(frozen=True, eq=True, slots=True)
class VectorConfiguration:
    size: int
    distance: Distance


@dataclass(frozen=True, eq=True, slots=True)
class IndexConfiguration:
    """
    Configuration of the indexes to create in the vector store.
    """

    # Name of the collection representing a particular entity type
    namespace: str
    # List of indexes to create, along with their configuration
    vectors: Dict[str, VectorConfiguration] = field(default_factory=dict)
    # Name of the property that contains the document id
    id_field: str = "id"

    def __hash__(self):
        frozen_vectors = frozenset(sorted(self.vectors.items()))
        return hash(self.namespace) + hash(self.id_field) + hash(frozen_vectors)
