import os
from typing import Optional

from openai import OpenAI

from django_semantic_search.embeddings.base import DenseTextEmbeddingModel
from django_semantic_search.types import DenseVector


class OpenAIEmbeddingModel(DenseTextEmbeddingModel):
    """
    OpenAI text embedding model that uses the OpenAI API to generate dense embeddings.

    **Requirements**:

    ```bash
    pip install django-semantic-search[openai]
    ```

    **Usage**:

    ```python title="settings.py"
    SEMANTIC_SEARCH = {
        "default_embeddings": {
            "model": "django_semantic_search.embeddings.OpenAIEmbeddingModel",
            "configuration": {
                "model": "text-embedding-3-small",
                "api_key": "your-api-key",  # Optional if set in env
            },
        },
        ...
    }
    ```
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize the OpenAI embedding model.

        :param model: OpenAI model to use for embeddings
        :param api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env variable
        :param kwargs: Additional kwargs passed to OpenAI client
        """
        self._model = model
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key must be provided either through api_key parameter or OPENAI_API_KEY environment variable"
            )
        self._client = OpenAI(api_key=api_key, **kwargs)
        # Cache the vector size after first call
        self._vector_size: Optional[int] = None

    def vector_size(self) -> int:
        if self._vector_size is None:
            response = self._client.embeddings.create(
                model=self._model,
                input="test",
            )
            self._vector_size = len(response.data[0].embedding)
        return self._vector_size

    def embed_document(self, document: str) -> DenseVector:
        response = self._client.embeddings.create(
            model=self._model,
            input=document,
        )
        return response.data[0].embedding

    def embed_query(self, query: str) -> DenseVector:
        return self.embed_document(query)
