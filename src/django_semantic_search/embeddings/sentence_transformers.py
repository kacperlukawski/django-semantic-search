from typing import Optional

from django_semantic_search.embeddings.base import (
    BaseEmbeddingModel,
    TextEmbeddingMixin,
)
from django_semantic_search.types import Vector


class SentenceTransformerModel(BaseEmbeddingModel, TextEmbeddingMixin):
    """
    Sentence-transformers model for embedding text.

    It is a wrapper around the sentence-transformers library. Users would rarely need to use this class directly, but
    rather specify it in the Django settings.

    **Requirements:**

    ```shell
    pip install django-semantic-search[sentence-transformers]
    ```

    **Usage:**

    ```python title="settings.py"
    SEMANTIC_SEARCH = {
        "default_embeddings": {
            "model": "django_semantic_search.embeddings.SentenceTransformerModel",
            "configuration": {
                "model_name": "sentence-transformers/all-MiniLM-L6-v2",
            },
        },
        ...
    }
    ```
    """

    def __init__(
        self,
        model_name: str,
        document_prompt: Optional[str] = None,
        query_prompt: Optional[str] = None,
    ):
        """
        Initialize the sentence-transformers _model.
        :param model_name: name of the model to use.
        """
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)
        self._document_prompt = document_prompt
        self._query_prompt = query_prompt

    def vector_size(self) -> int:
        """
        Return the size of the individual embedding.
        :return: size of the embedding.
        """
        return self._model.get_sentence_embedding_dimension()

    def embed_document(self, document: str) -> Vector:
        """
        Embed a document into a vector.
        :param document: document to embed.
        :return: document embedding.
        """
        return self._model.encode(document, prompt=self._document_prompt).tolist()

    def embed_query(self, query: str) -> Vector:
        """
        Embed a query into a vector.
        :param query: query to embed.
        :return: query embedding.
        """
        return self._model.encode(query, prompt=self._query_prompt).tolist()
