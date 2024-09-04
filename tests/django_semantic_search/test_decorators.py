import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db import models

import django_semantic_search as dss


class DummyModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "test_decorators"


def test_register_document_fails_on_missing_meta():
    """
    Test that the register_document decorator fails when the document class does not have a Meta class.
    """

    try:

        @dss.register_document
        class InvalidDocument:  # noqa
            pass
    except ImproperlyConfigured as e:
        assert str(e) == "Document class InvalidDocument does not have a Meta class."


def test_register_document_fails_on_duplicate_registration():
    """
    Test that the register_document decorator fails when the document class is registered for the same model twice.
    """

    @dss.register_document
    class Document1(dss.Document):  # noqa
        class Meta:
            model = DummyModel

    try:

        @dss.register_document
        class Document2(dss.Document):  # noqa
            class Meta:
                model = DummyModel
    except ImproperlyConfigured as e:
        assert str(e) == "Document class for model DummyModel is already registered."


@pytest.mark.integration
def test_register_document_creates_update_delete_signals():
    """
    Test that the document registers the post_save and post_delete signals for the model.
    """

    class SingleUseDummyModel(DummyModel):
        """Single use model for testing the document registration in this test only."""

        class Meta:
            app_label = "test_decorators"

    assert not models.signals.post_save.has_listeners(SingleUseDummyModel)
    assert not models.signals.post_delete.has_listeners(SingleUseDummyModel)

    @dss.register_document
    class AnotherDummyDocument(dss.Document):  # noqa
        class Meta:
            model = SingleUseDummyModel
            namespace = "dummy"
            indexes = (dss.VectorIndex("name"),)

    assert models.signals.post_save.has_listeners(SingleUseDummyModel)
    assert models.signals.post_delete.has_listeners(SingleUseDummyModel)
