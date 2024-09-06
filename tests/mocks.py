import random
from collections import defaultdict
from hashlib import md5
from typing import List

from django_semantic_search import Document
from django_semantic_search.backends.base import BaseVectorSearchBackend
from django_semantic_search.backends.types import IndexConfiguration
from django_semantic_search.embeddings.base import (
    BaseEmbeddingModel,
    TextEmbeddingMixin,
)
from django_semantic_search.types import DocumentID, Vector


class MockTextEmbeddingModel(BaseEmbeddingModel, TextEmbeddingMixin):
    """
    Mock text embedding model for testing purposes. It produces short random vectors, but these vectors are consistent
    for the same input. So it can be used for testing purposes.
    """

    def __init__(self, size: int = 10):
        self._size = size

    def vector_size(self) -> int:
        return self._size

    def embed_document(self, document: str) -> Vector:
        """Return a random vector."""
        document_hash = md5(document.encode()).hexdigest()
        random.seed(document_hash)
        return [random.random() for _ in range(self._size)]

    def embed_query(self, query: str) -> Vector:
        return self.embed_document(query)


class MockVectorSearchBackend(BaseVectorSearchBackend):
    """
    Mock vector search backend for testing purposes. It stores the vectors in memory, and allows to search for the
    closest vectors.
    """

    def __init__(self, index_configuration: IndexConfiguration):
        super().__init__(index_configuration)
        self._documents = defaultdict(dict)

    def configure(self):
        """No configuration is needed for the mock backend."""
        pass

    def search(
        self, vector_name: str, query: Vector, limit: int = 10
    ) -> List[DocumentID]:
        random.seed(sum(query))
        max_results = min(
            limit, len(self._documents[self.index_configuration.namespace])
        )
        selected_documents = random.sample(
            list(self._documents[self.index_configuration.namespace].values()),
            k=max_results,
        )
        return [doc.id for doc in selected_documents]

    def save(self, document: Document) -> None:
        self._documents[self.index_configuration.namespace][document.id] = document

    def delete(self, document_id: DocumentID) -> None:
        del self._documents[self.index_configuration.namespace][document_id]
