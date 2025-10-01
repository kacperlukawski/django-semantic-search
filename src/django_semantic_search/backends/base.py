import abc
from typing import Any, List, Optional

from django_semantic_search.backends.types import IndexConfiguration
from django_semantic_search.documents import Document
from django_semantic_search.types import DocumentID


class BaseVectorSearchBackend(abc.ABC):
    """
    Base class for all the vector search backends, such as Qdrant.
    """

    def __init__(self, index_configuration: IndexConfiguration):
        self.index_configuration = index_configuration
        self.configure()

    @abc.abstractmethod
    def configure(self):
        """
        Configure the indexes for the backend.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search(
        self,
        vector_name: str,
        query: List[float],
        limit: int = 10,
        metadata_filter: Optional[Any] = None,
    ) -> List[DocumentID]:
        """
        Search for the documents similar to the query vector in the backend.
        :param vector_name:
        :param query:
        :param limit:
        :param metadata_filter: optional backend-specific filter (e.g. Qdrant models.Filter)
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, document: Document):
        """
        Save the document in the backend.
        :param configuration: vector store configuration.
        :param document:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, document_id: DocumentID):
        """
        Delete the document from the backend.
        :param configuration: vector store configuration.
        :param document_id: id of the document to delete.
        """
        raise NotImplementedError
