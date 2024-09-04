import abc

from django_semantic_search.types import Vector


class BaseEmbeddingModel(abc.ABC):
    """
    Base class for all the embedding models, such as sentence-transformers or 3rd party libraries.
    """

    def vector_size(self) -> int:
        """
        Return the size of the individual embedding.
        :return: size of the embedding.
        """
        raise NotImplementedError


class TextEmbeddingMixin:
    """
    Mixin class for all the text embedding models.
    """

    def embed_document(self, document: str) -> Vector:
        """
        Embed a document into a vector.
        :param document: document to embed.
        :return: document embedding.
        """
        raise NotImplementedError

    def embed_query(self, query: str) -> Vector:
        """
        Embed a query into a vector.
        :param query: query to embed.
        :return: query embedding.
        """
        raise NotImplementedError
