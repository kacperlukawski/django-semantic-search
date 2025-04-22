import numpy as np
import pytest

from django_semantic_search.embeddings.fastembed import (
    FastEmbedDenseModel,
    FastEmbedSparseModel,
)


@pytest.mark.integration
class TestFastEmbedDenseModel:
    @pytest.fixture(autouse=True)
    def setup_model(self):
        self.model = FastEmbedDenseModel(model_name="BAAI/bge-small-en-v1.5")

    def test_initialization(self):
        model = FastEmbedDenseModel(model_name="BAAI/bge-small-en-v1.5")
        assert isinstance(model._model, object)  # Check model is initialized
        assert model._vector_size is None  # Size should be initially uncached

    def test_vector_size(self):
        size = self.model.vector_size()
        assert isinstance(size, int)
        assert size > 0
        # Check that size is cached
        assert self.model._vector_size == size
        # Get it again to test cached path
        assert self.model.vector_size() == size

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


@pytest.mark.integration
class TestFastEmbedSparseModel:
    @pytest.fixture(autouse=True)
    def setup_model(self):
        self.model = FastEmbedSparseModel(model_name="Qdrant/bm25")

    def test_initialization(self):
        model = FastEmbedSparseModel(model_name="Qdrant/bm25")
        assert isinstance(model._model, object)  # Check model is initialized

    def test_embed_document(self):
        vector = self.model.embed_document("This is a test document")
        assert isinstance(vector, dict)
        # Sparse vectors should have indices and values
        assert len(vector) > 0
        assert all(
            isinstance(k, int) and isinstance(v, float) for k, v in vector.items()
        )

    def test_embed_query(self):
        vector = self.model.embed_query("test query")
        assert isinstance(vector, dict)
        # Sparse vectors should have indices and values
        assert len(vector) > 0
        assert all(
            isinstance(k, int) and isinstance(v, (int, float))
            for k, v in vector.items()
        )

    def test_consistent_embeddings(self):
        text = "This is a test document"
        vector1 = self.model.embed_document(text)
        vector2 = self.model.embed_document(text)
        # Vectors should be identical for same input
        assert vector1 == vector2

    def test_sparse_vector_format(self):
        vector = self.model.embed_document("This is a test document")
        # Check that indices are unique
        assert len(vector.keys()) == len(set(vector.keys()))
        # Values should be non-negative for BM25-like models
        assert all(v >= 0 for v in vector.values())
