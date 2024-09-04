import django
from mocks import MockTextEmbeddingModel, MockVectorSearchBackend


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        SEMANTIC_SEARCH={
            "vector_store": {
                "backend": MockVectorSearchBackend,
                "configuration": {},
            },
            "default_embeddings": {
                "model": MockTextEmbeddingModel,
                "configuration": {},
            },
        },
    )

    django.setup()
