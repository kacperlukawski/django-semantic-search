import pytest
from django.conf import settings

from django_semantic_search import utils


def test_load_embedding_model_raises_on_missing_models_section(monkeypatch):
    settings.SEMANTIC_SEARCH = {
        "vector_store": {"backend": object, "configuration": {}},
        "default_embeddings": {"model": lambda **k: object(), "configuration": {}},
    }
    with pytest.raises(ValueError):
        utils.load_embedding_model("missing_section")


def test_load_embedding_model_raises_on_unknown_model(monkeypatch):
    settings.SEMANTIC_SEARCH = {
        "vector_store": {"backend": object, "configuration": {}},
        "default_embeddings": {"model": lambda **k: object(), "configuration": {}},
        "embedding_models": {},
    }
    with pytest.raises(ValueError):
        utils.load_embedding_model("does_not_exist")
