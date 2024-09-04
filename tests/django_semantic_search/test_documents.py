import pytest
from django.db import models

import django_semantic_search as dss


class DummyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ignored_field = models.CharField(max_length=255)

    class Meta:
        app_label = "test_documents"


@dss.register_document
class DummyDocument(dss.Document):
    class Meta:
        model = DummyModel
        namespace = "dummy"
        indexes = [
            dss.VectorIndex("name"),
            dss.VectorIndex("description"),
        ]


@pytest.fixture(scope="function")
def django_test_database():
    """
    Create a test database for Django with the dummy model.
    :return:
    """
    from django.db import connection

    with connection.schema_editor() as schema_editor:
        yield schema_editor.create_model(DummyModel)
        schema_editor.delete_model(DummyModel)


def test_dummy_document_produces_vectors():
    """
    Test that the document produces the correct vectors.
    """
    dummy = DummyModel(
        name="test", description="test description", ignored_field="ignored"
    )
    document = DummyDocument(dummy)
    vectors = document.vectors()
    assert len(vectors) == 2
    assert "name" in vectors
    assert "description" in vectors
    assert "name_description" not in vectors


def test_dummy_document_produces_metadata():
    """
    Test that the document produces the correct metadata.
    """
    dummy = DummyModel(
        name="test", description="test description", ignored_field="ignored"
    )
    document = DummyDocument(dummy)
    metadata = document.metadata()
    assert "name" in metadata
    assert "description" in metadata
    assert metadata["name"] == "test"
    assert metadata["description"] == "test description"


def test_document_signals_work_correctly(django_test_database):
    """
    Test that the search manager returns an empty queryset.
    """
    dummy = DummyModel(
        name="test", description="test description", ignored_field="ignored"
    )
    queryset = DummyDocument.objects.find(name="test")
    assert queryset.count() == 0
    dummy.save()
    queryset = DummyDocument.objects.find(name="test")
    assert queryset.count() == 1
    dummy.delete()
    queryset = DummyDocument.objects.find(name="test")
    assert queryset.count() == 0
