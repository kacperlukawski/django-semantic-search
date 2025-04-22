import pytest
from django.conf import settings
from django.db import models

from django_semantic_search import Document, VectorIndex, register_document


class TestModel(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        app_label = "test_vector_index"


@pytest.mark.integration
class TestVectorIndexEmbeddings:
    @pytest.fixture(autouse=True)
    def setup_settings(self):  # Remove the settings parameter
        settings.SEMANTIC_SEARCH = {
            "vector_store": {
                "backend": "django_semantic_search.backends.qdrant.QdrantBackend",
                "configuration": {"location": ":memory:"},
            },
            "default_embeddings": {
                "model": "django_semantic_search.embeddings.SentenceTransformerModel",
                "configuration": {
                    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                },
            },
            "embedding_models": {
                "title_model": {
                    "model": "django_semantic_search.embeddings.SentenceTransformerModel",
                    "configuration": {
                        "model_name": "sentence-transformers/all-mpnet-base-v2",
                        "document_prompt": "Title: ",
                    },
                },
                "content_model": {
                    "model": "django_semantic_search.embeddings.SentenceTransformerModel",
                    "configuration": {
                        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                        "document_prompt": "Content: ",
                    },
                },
            },
        }

    def test_different_models_for_indexes(self):
        @register_document
        class TestDocument(Document):
            class Meta:
                model = TestModel
                indexes = [
                    VectorIndex("title", embedding_model="title_model"),
                    VectorIndex("content", embedding_model="content_model"),
                ]

        # Create test instances
        instance = TestModel(title="Test Title", content="Test Content")

        # Get embeddings for both fields
        title_embedding = TestDocument.meta.indexes[0].get_model_embedding(instance)
        content_embedding = TestDocument.meta.indexes[1].get_model_embedding(instance)

        # Embeddings should be different sizes due to different models
        assert len(title_embedding) != len(content_embedding)

    def test_default_model_fallback(self):
        @register_document
        class TestDocument(Document):
            class Meta:
                model = TestModel
                indexes = [
                    VectorIndex("title"),  # Uses default model
                    VectorIndex("content", embedding_model="content_model"),
                ]

        instance = TestModel(title="Test Title", content="Test Content")

        # Both embeddings should work
        title_embedding = TestDocument.meta.indexes[0].get_model_embedding(instance)
        content_embedding = TestDocument.meta.indexes[1].get_model_embedding(instance)

        assert isinstance(title_embedding, (list, tuple))
        assert isinstance(content_embedding, (list, tuple))

    def test_invalid_model_name(self):
        with pytest.raises(ValueError) as exc_info:
            VectorIndex("title", embedding_model="non_existent_model")
        assert "Embedding model non_existent_model not found in settings" in str(
            exc_info.value
        )
