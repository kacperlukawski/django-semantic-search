from functools import cache
from typing import Optional

from django.conf import settings
from django.utils.module_loading import import_string

from django_semantic_search.backends.types import IndexConfiguration
from django_semantic_search.embeddings.base import DenseTextEmbeddingModel


@cache
def load_embedding_model(model_name: Optional[str] = None) -> DenseTextEmbeddingModel:
    """
    Load the embedding model specified in settings.
    :param model_name: name of the model configuration to use from settings
    :return: embedding model instance
    """
    semantic_search_settings = settings.SEMANTIC_SEARCH

    if model_name is None:
        model_config = semantic_search_settings["default_embeddings"]
    else:
        if "embedding_models" not in semantic_search_settings:
            raise ValueError("No embedding_models defined in settings")
        if model_name not in semantic_search_settings["embedding_models"]:
            raise ValueError(f"Embedding model {model_name} not found in settings")
        model_config = semantic_search_settings["embedding_models"][model_name]

    model_cls = model_config["model"]
    if isinstance(model_cls, str):
        model_cls = import_string(model_cls)
    model_configuration = model_config["configuration"]
    return model_cls(**model_configuration)


@cache
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
