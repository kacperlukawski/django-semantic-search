import abc
from typing import Protocol

from django_semantic_search.types import (
    DenseVector,
    DocumentContent,
    Query,
    SparseVector,
)


class EmbeddingModel(Protocol):
    """Protocol defining common interface for all embedding models."""

    def vector_size(self) -> int:
        """Return the size of the individual embedding."""
        ...

    def supports_document(self, document: DocumentContent) -> bool:
        """Check if the embedding model supports the document."""
        ...


class DenseEmbeddingModel(abc.ABC):
    """Base class for models producing dense vector embeddings."""

    @abc.abstractmethod
    def vector_size(self) -> int:
        """Return the fixed size of dense embeddings."""
        raise NotImplementedError

    @abc.abstractmethod
    def embed_document(self, document: DocumentContent) -> DenseVector:
        """Embed a document into a dense vector."""
        raise NotImplementedError

    @abc.abstractmethod
    def embed_query(self, query: Query) -> DenseVector:
        """Embed a query into a dense vector."""
        raise NotImplementedError


class SparseEmbeddingModel(abc.ABC):
    """Base class for models producing sparse vector embeddings."""

    @abc.abstractmethod
    def embed_document(self, document: DocumentContent) -> SparseVector:
        """Embed a document into a sparse vector."""
        raise NotImplementedError

    @abc.abstractmethod
    def embed_query(self, query: Query) -> SparseVector:
        """Embed a query into a sparse vector."""
        raise NotImplementedError


class TextEmbeddingMixin:
    """Mixin for text-specific embedding functionality."""

    def supports_document(self, document: DocumentContent) -> bool:
        return isinstance(document, str)


class DenseTextEmbeddingModel(TextEmbeddingMixin, DenseEmbeddingModel, abc.ABC):
    """Base class for dense text embedding models."""

    pass


class SparseTextEmbeddingModel(TextEmbeddingMixin, SparseEmbeddingModel, abc.ABC):
    """Base class for sparse text embedding models."""

    pass
