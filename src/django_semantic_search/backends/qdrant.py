import logging
import uuid
from typing import List

from django_semantic_search import Document
from django_semantic_search.backends.base import BaseVectorSearchBackend
from django_semantic_search.backends.types import Distance, IndexConfiguration
from django_semantic_search.types import DocumentID

logger = logging.getLogger(__name__)


class QdrantBackend(BaseVectorSearchBackend):
    """
    Backend that integrates with Qdrant vector database.

    It handles the configuration of separate collections per each model we want to enable search for. Users rarely
    interact with this backend directly, as backend is usually configured via Django settings.

    **Requirements**:

    ```bash
    pip install django-semantic-search[qdrant]
    ```

    **Usage**:

    ```python title="settings.py"
    SEMANTIC_SEARCH = {
        "vector_store": {
            "backend": "django_semantic_search.backends.qdrant.QdrantBackend",
            "configuration": {
                "host": "http://localhost:6333",
            },
        },
        ...
    }
    ```
    """

    from qdrant_client import models

    DISTANCE_MAPPING = {
        Distance.COSINE: models.Distance.COSINE,
        Distance.EUCLIDEAN: models.Distance.EUCLID,
        Distance.DOT_PRODUCT: models.Distance.DOT,
    }

    def __init__(self, index_configuration: IndexConfiguration, *args, **kwargs):
        from qdrant_client import QdrantClient

        self.client = QdrantClient(*args, **kwargs)
        super().__init__(index_configuration)

    def configure(self):
        from qdrant_client import models

        try:
            collection_info = self.client.get_collection(  # noqa
                collection_name=self.index_configuration.namespace
            )
            # TODO: validate if all the vectors are present and with correct types
        except Exception:
            logger.warning(
                f"Collection {self.index_configuration.namespace} does not exist. Creating a new one."
            )
            self.client.create_collection(
                collection_name=self.index_configuration.namespace,
                vectors_config={
                    vector_name: models.VectorParams(
                        size=vector_config.size,
                        distance=self.DISTANCE_MAPPING.get(vector_config.distance),
                    )
                    for vector_name, vector_config in self.index_configuration.vectors.items()
                },
            )
            self.client.create_payload_index(
                collection_name=self.index_configuration.namespace,
                field_name=self.index_configuration.id_field,
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

    def search(
        self, vector_name: str, query: List[float], limit: int = 10
    ) -> List[DocumentID]:
        results = self.client.query_points(
            collection_name=self.index_configuration.namespace,
            query=query,
            using=vector_name,
            limit=limit,
            with_vectors=False,
            with_payload=True,
        )
        return [
            result.payload.get(self.index_configuration.id_field)
            for result in results.points
        ]

    def save(self, document: Document):
        from qdrant_client import models

        vectors = document.vectors()
        payload = {
            self.index_configuration.id_field: document.id,
            **document.metadata(),
        }
        self.client.upsert(
            collection_name=self.index_configuration.namespace,
            points=[
                models.PointStruct(
                    id=uuid.uuid4().hex,
                    vector=vectors,
                    payload=payload,
                )
            ],
        )

    def delete(self, document_id: DocumentID):
        from qdrant_client import models

        self.client.delete(
            collection_name=self.index_configuration.namespace,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key=self.index_configuration.id_field,
                        match=models.MatchValue(
                            value=document_id,
                        ),
                    )
                ]
            ),
        )
