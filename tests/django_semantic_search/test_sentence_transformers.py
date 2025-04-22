import numpy as np
import pytest

from django_semantic_search.embeddings.sentence_transformers import (  # noqa
    SentenceTransformerModel,
)


@pytest.mark.integration
class TestSentenceTransformerModel:
    @pytest.fixture(autouse=True)
    def setup_model(self):
        self.model = SentenceTransformerModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def test_initialization(self):
        model = SentenceTransformerModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        assert isinstance(model._model, object)  # Check model is initialized
        assert model._document_prompt is None
        assert model._query_prompt is None

    def test_initialization_with_prompts(self):
        model = SentenceTransformerModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            document_prompt="Doc: ",
            query_prompt="Query: ",
        )
        assert model._document_prompt == "Doc: "
        assert model._query_prompt == "Query: "

    def test_vector_size(self):
        size = self.model.vector_size()
        assert isinstance(size, int)
        assert size > 0
        # Common size for all-MiniLM-L6-v2 model
        assert size == 384

    def test_embed_document(self):
        vector = self.model.embed_document("This is a test document")
        assert isinstance(vector, list)
        assert len(vector) == self.model.vector_size()
        assert all(isinstance(x, float) for x in vector)

    def test_embed_query(self):
        vector = self.model.embed_query("test query")
        assert isinstance(vector, list)
        assert len(vector) == self.model.vector_size()
        assert all(isinstance(x, float) for x in vector)

    def test_consistent_embeddings(self):
        text = "This is a test document"
        vector1 = self.model.embed_document(text)
        vector2 = self.model.embed_document(text)
        # Vectors should be nearly identical for same input
        assert np.allclose(vector1, vector2, rtol=1e-5, atol=1e-8)

    def test_document_prompt_affects_embedding(self):
        model_with_prompt = SentenceTransformerModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            document_prompt="Doc: ",
        )
        text = "This is a test document"
        vector1 = self.model.embed_document(text)
        vector2 = model_with_prompt.embed_document(text)
        # Vectors should be different when using a prompt
        assert not np.allclose(vector1, vector2, rtol=1e-5, atol=1e-8)

    def test_query_prompt_affects_embedding(self):
        model_with_prompt = SentenceTransformerModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            query_prompt="Query: ",
        )
        text = "test query"
        vector1 = self.model.embed_query(text)
        vector2 = model_with_prompt.embed_query(text)
        # Vectors should be different when using a prompt
        assert not np.allclose(vector1, vector2, rtol=1e-5, atol=1e-8)
