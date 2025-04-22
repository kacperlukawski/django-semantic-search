import abc
import logging
from typing import Dict, Generic, Iterable, List, Optional, Type, TypeVar

from django.db import models
from django.db.models import QuerySet

from django_semantic_search.backends.types import (
    Distance,
    IndexConfiguration,
    VectorConfiguration,
)
from django_semantic_search.types import DocumentID, MetadataValue, Vector

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=models.Model)


class VectorIndex:
    """
    A definition of a single vector index. It contains the name of the index and the fields that should be indexed,
    but also allows to surpass the default settings of django-semantic-search.
    """

    def __init__(
        self,
        *fields: str,
        index_name: Optional[str] = None,
        distance: Distance = Distance.COSINE,
        embedding_model: Optional[str] = None,
    ):
        """
        :param fields: model fields to index together.
        :param index_name: name of the index to use in a backend. By default, it is the concatenation of the fields.
        :param distance: distance metric to use for similarity search.
        :param embedding_model: name of the embedding model to use, must be defined in SEMANTIC_SEARCH settings.
        """
        # Loading the default embedding model here, as otherwise it would create a circular import
        from django_semantic_search.utils import load_embedding_model

        if len(fields) != 1:
            raise ValueError("Only single field indexes are supported at the moment.")

        self._fields: List[str] = list(fields)
        self._index_name = index_name or "_".join(fields)
        self._distance = distance
        self._embedding_model = load_embedding_model(embedding_model)

    def validate(self, model_cls: Type[models.Model]):
        """
        Validate the index configuration for the model.
        :param model_cls: model class to validate the index for.
        """
        for field in self._fields:
            if not hasattr(model_cls, field):
                raise ValueError(
                    f"Field {field} is not present in the model {model_cls.__name__}"
                )

    def is_for_field(self, field: str) -> bool:
        """
        Check if the index is for the field.
        :param field: field to check.
        :return: True if the index is for the field, False otherwise.
        """
        return field in self._fields

    @property
    def index_name(self) -> str:
        """
        Return the name of the index.
        :return: index name.
        """
        return self._index_name

    @property
    def distance(self) -> Distance:
        """
        Return the distance metric to use for the index.
        :return: distance metric.
        """
        return self._distance

    @property
    def vector_size(self) -> int:
        """
        Return the size of the individual embedding.
        :return: size of the embedding.
        """
        return self._embedding_model.vector_size()

    def get_model_embedding(self, instance: models.Model) -> Vector:
        """
        Get the embedding for the instance.
        :param instance: model instance to get the embedding for.
        :return: embedding for the instance.
        """
        return self._embedding_model.embed_document(
            " ".join(getattr(instance, field) for field in self._fields)
        )

    def get_query_embedding(self, query: str) -> Vector:
        """
        Get the embedding for the query.
        :param query: query to get the embedding for.
        :return: embedding for the query.
        """
        return self._embedding_model.embed_query(query)


class MetaManager:
    """
    A descriptor to store an instance of the Meta class instance on the document class.
    """

    def __get__(self, instance: Optional["Document"], owner: Type["Document"]):
        if not hasattr(owner, "_meta"):
            setattr(owner, "_meta", owner.Meta())
        return getattr(owner, "_meta")


class IndexConfigurationManager:
    """
    A descriptor to store an instance of the IndexConfiguration class instance on the document class. The configuration
    of the index is derived from the Meta class of the document.
    """

    def __get__(
        self, instance: Optional["Document"], owner: Type["Document"]
    ) -> IndexConfiguration:
        if not hasattr(owner, "_index_configuration"):
            attr_meta = owner.meta
            model = getattr(attr_meta, "model", None)
            model_name = model.__name__ if model else None
            index_namespace = getattr(attr_meta, "namespace", model_name)
            indexes = getattr(attr_meta, "indexes", [])
            config = IndexConfiguration(
                namespace=index_namespace,
                vectors={
                    index.index_name: VectorConfiguration(
                        size=index.vector_size,
                        distance=index.distance,
                    )
                    for index in indexes
                },
            )
            setattr(owner, "_index_configuration", config)
        return getattr(owner, "_index_configuration")


class BackendManager:
    """
    A descriptor to store an instance of the backend on the document class. The backend is derived from the index
    configuration and is loaded dynamically.
    """

    def __get__(self, instance: Optional["Document"], owner: Type["Document"]):
        if not hasattr(owner, "_backend"):
            from django_semantic_search.utils import load_backend

            setattr(owner, "_backend", load_backend(owner.index_configuration))
        return getattr(owner, "_backend")


class DocumentManager(Generic[T]):
    """
    A descriptor to store an instance of the document manager on the document class. The document manager is used to
    find similar documents in the vector index, but also to perform any other operations on the querysets of the
    model instances.
    """

    def __init__(self, cls: Type["Document"]):
        self.cls = cls

    def search(
        self,
        limit: int = 10,
        **kwargs,
    ) -> QuerySet[T]:
        """
        Find the documents similar to the query in the vector index. If there are multiple indexes, the search is
        performed in all of them and the results are combined.
        :param limit: number of results to return.
        :param kwargs: query parameters to restrict the search.
        :return:
        """
        if len(kwargs) != 1:
            raise ValueError("Only single field indexes are supported at the moment.")

        field_name, field_value = next(iter(kwargs.items()))
        vector_index = next(
            index for index in self.cls.meta.indexes if index.is_for_field(field_name)
        )
        if vector_index is None:
            raise ValueError(f"No index found for field {field_name}")

        query_embedding = vector_index.get_query_embedding(field_value)
        document_ids = self.cls.backend.search(
            vector_index.index_name, query_embedding, limit=limit
        )
        if not document_ids:
            return self.cls.meta.model.objects.none()

        preserved_ids = models.Case(
            *[models.When(pk=pk, then=pos) for pos, pk in enumerate(document_ids)]
        )
        queryset = self.cls.meta.model.objects.filter(pk__in=document_ids).order_by(
            preserved_ids
        )
        return queryset

    def index(self, qs: QuerySet[T]):
        """
        Index the queryset of the model instances.
        :param qs: queryset of the model instances to index.
        """
        # TODO: this is the most basic implementation, it should be optimized
        for instance in qs:
            self.cls(instance).save()


class DocumentManagerDescriptor(Generic[T]):
    """
    A descriptor to store the document manager on the document class.
    """

    def __get__(self, instance, owner):
        if not hasattr(owner, "_document_manager"):
            setattr(owner, "_document_manager", DocumentManager[T](owner))
        return getattr(owner, "_document_manager")


class Document(abc.ABC, Generic[T]):
    """
    Base class for all the documents. There is a one-to-one mapping between the document subclass and the model class,
    to configure how a specific model instances should be converted to a document.

    **Usage**:

    ```python title="products/models.py"
    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=255)
        description = models.TextField()

    ```

    ```python title="products/documents.py"
    from django_semantic_search import Document, VectorIndex
    from django_semantic_search.decorators import register_document

    @register_document
    class ProductDocument(Document):
        class Meta:
            model = Product
            indexes = [
                VectorIndex("name"),
                VectorIndex("description"),
            ]
    ```

    `django-semantic-search` will automatically handle all the configuration in the backend. The `register_document`
    decorator will register the model signals to update the documents in the vector store when the model is updated
    or deleted. As a user you don't have to manually call the `save` or `delete` methods on the document instances.

    **Search example:**

    ```python title="products/views.py"
    from django.http import JsonResponse
    from products.documents import ProductDocument

    def my_view(request):
        query = "this is a query"
        results = ProductDocument.objects.find(name=query)
        return JsonResponse(
            {
                "results": list(name_results.values())
            }
        )
    ```

    The `find` method on the `objects` attribute of the document class will return the queryset of the model instances
    that are similar to the query. The search is performed using the selected vector index passed as a keyword argument
    to the `find` method. In our case, we are searching for the query in the `name` field of the `Product` model. If we
    want to search in the `description` field, we would call `ProductDocument.objects.find(description=query)`.
    """

    # Important:
    # The following descriptors have to be defined in the specific order, as they depend on each other
    # and the order of the descriptors is the order in which they are executed.
    meta = MetaManager()
    index_configuration = IndexConfigurationManager()
    backend = BackendManager()
    objects = DocumentManagerDescriptor[T]()

    def __init__(self, instance: T):
        self._instance = instance

    def save(self) -> None:
        """
        Save the document in the vector store.
        """
        if not self._instance.pk:
            raise ValueError(
                "The model instance has to be saved before creating a document."
            )
        self.backend.save(self)

    def delete(self) -> None:
        """
        Delete the document from the vector store.
        """
        self.backend.delete(self.id)

    @property
    def id(self) -> DocumentID:
        if not self._instance.pk:
            raise ValueError(
                "The model instance has to be saved before accessing the ID."
            )
        return self._instance.pk

    def vectors(self) -> Dict[str, Vector]:
        """
        Return the vectors for the document.
        :return: dictionary of the vectors.
        """
        return {
            index.index_name: index.get_model_embedding(self._instance)
            for index in self.meta.indexes
        }

    def metadata(self) -> Dict[str, MetadataValue]:
        """
        Return the metadata for the document.
        :return: dictionary of the metadata.
        """
        include_fields = getattr(
            self.meta, "include_fields", Document.Meta.include_fields
        )
        if "*" in include_fields:
            include_fields = [field.name for field in self._instance._meta.fields]
        return {field: getattr(self._instance, field) for field in include_fields}

    class Meta:
        # The model this document is associated with
        model: Optional[Type[models.Model]] = None
        # Namespace for the documents in the vector store, defaults to the model name
        namespace: Optional[str] = None
        # List of vector indexes created out of the model fields
        indexes: Iterable[VectorIndex] = []
        # Model fields that should be included in the metadata
        include_fields: List[str] = ["*"]
        # Flag to disable signals on the model, so the documents are not updated on model changes
        disable_signals: bool = False
