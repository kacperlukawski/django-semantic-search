import django
from mocks import test_settings


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
        SEMANTIC_SEARCH=test_settings,
    )

    django.setup()
