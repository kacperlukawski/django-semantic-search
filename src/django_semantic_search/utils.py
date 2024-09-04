from functools import cache

from django.conf import settings
from django.utils.module_loading import import_string

from django_semantic_search.backends.types import IndexConfiguration
from django_semantic_search.embeddings.base import BaseEmbeddingModel


@cache
def load_embedding_model() -> BaseEmbeddingModel:
    """
    Load the default embedding model, as specified in the settings.
    :return: default embedding model instance.
    """
    semantic_search_settings = settings.SEMANTIC_SEARCH
    model_cls = semantic_search_settings["default_embeddings"]["model"]
    if isinstance(model_cls, str):
        model_cls = import_string(model_cls)
    model_config = semantic_search_settings["default_embeddings"]["configuration"]
    return model_cls(**model_config)


def load_backend(index_configuration: IndexConfiguration):
    """
    Load the backend, as specified in the settings.
    :return: backend instance.
    """
    semantic_search_settings = settings.SEMANTIC_SEARCH
    backend_cls = semantic_search_settings["vector_store"]["backend"]
    if isinstance(backend_cls, str):
        backend_cls = import_string(backend_cls)
    backend_config = semantic_search_settings["vector_store"]["configuration"]
    return backend_cls(index_configuration, **backend_config)
