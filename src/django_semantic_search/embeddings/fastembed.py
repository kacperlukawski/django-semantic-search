from typing import Optional

from django_semantic_search.embeddings.base import (
    DenseTextEmbeddingModel,
    SparseTextEmbeddingModel,
)
from django_semantic_search.types import (
    DenseVector,
    DocumentContent,
    Query,
    SparseVector,
)


class FastEmbedDenseModel(DenseTextEmbeddingModel):
    """
    FastEmbed dense embedding model that uses the FastEmbed library to generate dense embeddings.

    **Requirements:**

    ```shell
    pip install django-semantic-search[fastembed]
    ```

    **Usage:**

    ```python title="settings.py"
    SEMANTIC_SEARCH = {
        "default_embeddings": {
            "model": "django_semantic_search.embeddings.FastEmbedDenseModel",
            "configuration": {
                "model_name": "BAAI/bge-small-en-v1.5",
            },
        },
        ...
    }
    ```
    """

    def __init__(
        self,
        model_name: str,
        **kwargs,
    ):
        """
        Initialize the FastEmbed dense model.

        :param model_name: name of the model to use
        :param kwargs: additional kwargs passed to FastEmbed
        """
        from fastembed import TextEmbedding

        self._model = TextEmbedding(
            model_name=model_name,
            **kwargs,
        )
        # Cache the vector size after first call
        self._vector_size: Optional[int] = None

    def vector_size(self) -> int:
        """
        Return the size of the individual embedding.
        :return: size of the embedding.
        """
        if self._vector_size is None:
            # Get vector size by embedding a test string
            vector = next(self._model.embed(["test"]))
            self._vector_size = len(vector)
        return self._vector_size

    def embed_document(self, document: str) -> DenseVector:
        """
        Embed a document into a vector.
        :param document: document to embed.
        :return: document embedding.
        """
        vector = next(self._model.passage_embed([document]))
        return vector.tolist()

    def embed_query(self, query: str) -> DenseVector:
        """
        Embed a query into a vector.
        :param query: query to embed.
        :return: query embedding.
        """
        vector = next(self._model.query_embed([query]))
        return vector.tolist()


class FastEmbedSparseModel(SparseTextEmbeddingModel):
    """
    FastEmbed sparse embedding model that uses the FastEmbed library to generate sparse embeddings.

    **Requirements:**

    ```shell
    pip install django-semantic-search[fastembed]
    ```

    **Important:** For now, there is no way to use the model in django-semantic-search, but it's on the way.
    """

    def __init__(
        self,
        model_name: str,
        **kwargs,
    ):
        """
        Initialize the FastEmbed sparse model.

        :param model_name: name of the model to use
        :param kwargs: additional kwargs passed to FastEmbed
        """
        from fastembed import SparseTextEmbedding

        self._model = SparseTextEmbedding(
            model_name=model_name,
            **kwargs,
        )

    def embed_document(self, document: DocumentContent) -> SparseVector:
        vector = next(self._model.passage_embed([document]))
        return dict(zip(vector.indices.tolist(), vector.values.tolist()))

    def embed_query(self, query: Query) -> SparseVector:
        vector = next(self._model.query_embed([query]))
        return dict(zip(vector.indices.tolist(), vector.values.tolist()))
