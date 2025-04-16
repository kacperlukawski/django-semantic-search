import os

import pytest

from django_semantic_search.embeddings.openai import OpenAIEmbeddingModel


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set in environment"
)
class TestOpenAIEmbeddingModel:
    def test_initialization(self):
        model = OpenAIEmbeddingModel()
        assert model._model == "text-embedding-3-small"

    def test_initialization_fails_without_api_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError) as exc_info:
            OpenAIEmbeddingModel()
        assert "OpenAI API key must be provided" in str(exc_info.value)

    def test_vector_size(self):
        model = OpenAIEmbeddingModel()
        size = model.vector_size()
        assert isinstance(size, int)
        assert size > 0
        # Check that size is cached
        assert model._vector_size == size

    def test_embed_document(self):
        model = OpenAIEmbeddingModel()
        vector = model.embed_document("This is a test document")
        assert isinstance(vector, list)
        assert len(vector) == model.vector_size()
        assert all(isinstance(x, float) for x in vector)

    def test_embed_query(self):
        model = OpenAIEmbeddingModel()
        vector = model.embed_query("test query")
        assert isinstance(vector, list)
        assert len(vector) == model.vector_size()
        assert all(isinstance(x, float) for x in vector)

    def test_consistent_embeddings(self):
        model = OpenAIEmbeddingModel()
        text = "This is a test document"
        vector1 = model.embed_document(text)
        vector2 = model.embed_document(text)
        # Vectors should be identical for same input
        assert vector1 == vector2
