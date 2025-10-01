import pytest
from django.db import models

import django_semantic_search as dss


class FilterDummyModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "test_documents"


@dss.register_document
class FilterDummyDocument(dss.Document):
    class Meta:
        model = FilterDummyModel
        namespace = "filter_dummy"
        indexes = [
            dss.VectorIndex("name"),
        ]


@pytest.fixture(scope="module")
def django_test_database():
    from django.db import connection

    with connection.schema_editor() as schema_editor:
        yield schema_editor.create_model(FilterDummyModel)
        schema_editor.delete_model(FilterDummyModel)


def test_metadata_filter_is_passed_to_backend(django_test_database):
    instance = FilterDummyModel.objects.create(name="alpha")
    FilterDummyDocument(instance).save()

    from qdrant_client import models

    my_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="A"),
            )
        ]
    )

    list(FilterDummyDocument.objects.search(name="alpha", metadata_filter=my_filter))

    backend = FilterDummyDocument.backend
    assert getattr(backend, "last_metadata_filter", None) is my_filter


def test_metadata_filter_default_none(django_test_database):
    instance = FilterDummyModel.objects.create(name="beta")
    FilterDummyDocument(instance).save()

    list(FilterDummyDocument.objects.search(name="beta"))

    backend = FilterDummyDocument.backend
    assert getattr(backend, "last_metadata_filter", "__unset__") is None
