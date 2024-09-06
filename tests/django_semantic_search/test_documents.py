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


@pytest.fixture(scope="module")
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


def test_two_documents_have_different_backends():
    """
    Test that two documents with different indexes have different backends.
    """

    class AnotherModel(models.Model):
        name = models.CharField(max_length=255)
        description = models.TextField()

        class Meta:
            app_label = "test_documents"

    @dss.register_document
    class AnotherDocument(dss.Document):
        class Meta:
            model = AnotherModel
            namespace = "another"
            indexes = [
                dss.VectorIndex("name"),
            ]

    dummy_index_configuration = DummyDocument.backend.index_configuration
    another_index_configuration = AnotherDocument.backend.index_configuration
    assert dummy_index_configuration.namespace == "dummy"
    assert another_index_configuration.namespace == "another"


def test_document_signals_work_correctly(django_test_database):
    """
    Test that the search manager returns an empty queryset.
    """
    dummy = DummyModel(
        name="test", description="test description", ignored_field="ignored"
    )
    queryset = DummyDocument.objects.search(name="test")
    assert queryset.count() == 0
    dummy.save()
    queryset = DummyDocument.objects.search(name="test")
    assert queryset.count() == 1
    dummy.delete()
    queryset = DummyDocument.objects.search(name="test")
    assert queryset.count() == 0


def test_model_has_more_entries_than_vector_backend():
    from django.db import connection

    class JustAnotherModel(models.Model):
        name = models.CharField(max_length=255)
        description = models.TextField()

        class Meta:
            app_label = "test_documents"

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(JustAnotherModel)

        # Create some instances of the model, which won't be in the vector store yet (document is created later)
        JustAnotherModel(name="test1", description="test description 1").save()
        JustAnotherModel(name="test2", description="test description 2").save()

        @dss.register_document
        class JustAnotherDocument(dss.Document):
            class Meta:
                model = JustAnotherModel
                namespace = "just_another"
                indexes = [
                    dss.VectorIndex("name"),
                ]

        assert JustAnotherModel.objects.count() == 2
        assert JustAnotherDocument.objects.search(name="a").count() == 0

        JustAnotherModel(name="test3", description="test description 3").save()

        assert JustAnotherModel.objects.count() == 3
        assert JustAnotherDocument.objects.search(name="a").count() == 1

        JustAnotherDocument.objects.index(JustAnotherModel.objects.all())

        assert JustAnotherModel.objects.count() == 3
        assert JustAnotherDocument.objects.search(name="a").count() == 3

        schema_editor.delete_model(JustAnotherModel)
