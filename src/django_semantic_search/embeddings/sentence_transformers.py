from typing import Optional

from django_semantic_search.embeddings.base import DenseTextEmbeddingModel
from django_semantic_search.types import DenseVector


class SentenceTransformerModel(DenseTextEmbeddingModel):
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

    Some models accept prompts to be used for the document and query. These prompts are used as additional
    instructions for the model to generate embeddings. For example, if the `document_prompt` is set to `"Doc: "`, the
    model will generate embeddings with the prompt `"Doc: "` followed by the document text. Similarly, the
    `query_prompt` is used for the query, if set.

    ```python title="settings.py"
    SEMANTIC_SEARCH = {
        "default_embeddings": {
            "model": "django_semantic_search.embeddings.SentenceTransformerModel",
            "configuration": {
                "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                "document_prompt": "Doc: ",
                "query_prompt": "Query: ",
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
        Initialize the sentence-transformers model.

        Some models accept prompts to be used for the document and query. These prompts are used as additional
        instructions for the model to generate embeddings. For example, if the `document_prompt` is set to "Doc: ", the
        model will generate embeddings with the prompt "Doc: " followed by the document text.

        :param model_name: name of the model to use.
        :param document_prompt: prompt to use for the document, defaults to None.
        :param query_prompt: prompt to use for the query, defaults to None.
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

    def embed_document(self, document: str) -> DenseVector:
        """
        Embed a document into a vector.
        :param document: document to embed.
        :return: document embedding.
        """
        return self._model.encode(document, prompt=self._document_prompt).tolist()

    def embed_query(self, query: str) -> DenseVector:
        """
        Embed a query into a vector.
        :param query: query to embed.
        :return: query embedding.
        """
        return self._model.encode(query, prompt=self._query_prompt).tolist()
