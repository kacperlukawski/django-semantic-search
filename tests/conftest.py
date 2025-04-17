import django
from mocks import MockDenseTextEmbeddingModel, MockVectorSearchBackend


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
                "AUTOCOMMIT": True,
            }
        },
        SEMANTIC_SEARCH={
            "vector_store": {
                "backend": MockVectorSearchBackend,
                "configuration": {},
            },
            "default_embeddings": {
                "model": MockDenseTextEmbeddingModel,
                "configuration": {},
            },
        },
    )

    django.setup()
