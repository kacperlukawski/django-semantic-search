import logging
from typing import Any, Type

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.dispatch import receiver

from django_semantic_search.documents import Document
from django_semantic_search.utils import load_backend

logger = logging.getLogger(__name__)


def register_document(document_cls: Type[Document]) -> Type[Document]:
    """
    Register the document class to be used for the specified model.
    :param document_cls: document class to register
    """
    default_meta = Document.Meta
    meta = getattr(document_cls, "meta", None)
    if meta is None:
        raise ImproperlyConfigured(
            f"Document class {document_cls.__name__} does not have a Meta class."
        )

    # Get the model class from the Meta class of the document
    model_cls = getattr(meta, "model", default_meta.model)
    if not model_cls:
        raise ImproperlyConfigured(
            f"Meta class for {document_cls.__name__} does not have a model attribute."
        )

    # Validate all the indexes for the document
    indexes = getattr(meta, "indexes", default_meta.indexes)
    for index in indexes:
        index.validate(model_cls)

    # Register the model handlers
    register_model_handlers(document_cls)

    # Set up the document class to initialize vector store
    index_configuration = document_cls.index_configuration
    backend = load_backend(index_configuration)
    logger.info(
        f"Initializing vector store for {document_cls.meta.model} with backend {backend}"
    )

    return document_cls


def register_model_handlers(document_cls: Type[Document]) -> Type[Document]:
    """
    Register all the model signals to update the documents in the vector store.
    """
    logger.info(f"Registering handlers for {document_cls.meta.model}")

    disable_signals = getattr(
        document_cls.meta, "disable_signals", Document.Meta.disable_signals
    )
    if disable_signals:
        logger.warning(
            f"Signals are disabled for {document_cls.meta.model}. Model changes "
            f"will not be reflected in the vector store."
        )
        return document_cls

    if hasattr(document_cls.meta, "__signals_registered__"):
        logger.warning(f"Signals are already registered for {document_cls.meta.model}.")
        return document_cls

    model = document_cls.meta.model

    @receiver(models.signals.post_save, sender=model, weak=False)
    def save_model(
        sender: Type[models.Model], instance: models.Model, created: bool, **kwargs: Any
    ) -> None:
        logger.debug(f"Saving document for {instance}")
        # TODO: detect the changes in the model and determine if the document should be updated

        # Create the document instance out of the model instance and save it
        document = document_cls(instance)
        document.save()

    @receiver(models.signals.post_delete, sender=model, weak=False)
    def delete_model(
        sender: Type[models.Model], instance: models.Model, **kwargs: Any
    ) -> None:
        logger.debug(f"Deleting document for {instance}")
        # Create the document instance out of the model instance and delete it
        document = document_cls(instance)
        document.delete()

    # Mark the signals as registered
    setattr(document_cls.meta, "__signals_registered__", True)

    return document_cls
