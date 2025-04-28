from mocks import test_settings

import django_semantic_search
from django_semantic_search import default_settings
from django_semantic_search.apps import DjangoSemanticSearchConfig


def test_custom_settings_are_not_overwritten_on_ready():
    from django.conf import settings

    # Save the initial settings and set custom settings
    init_semantic_search_settings = getattr(settings, "SEMANTIC_SEARCH")
    setattr(settings, "SEMANTIC_SEARCH", test_settings)

    # Run ready and check that the settings are not overwritten
    config = DjangoSemanticSearchConfig(
        "django_semantic_search", django_semantic_search
    )
    config.ready()

    assert hasattr(settings, "SEMANTIC_SEARCH")
    assert settings.SEMANTIC_SEARCH == test_settings

    # Restore the initial settings
    setattr(settings, "SEMANTIC_SEARCH", init_semantic_search_settings)


def test_default_settings_are_set_on_ready():
    from django.conf import settings

    # Save the initial settings and delete them so that the default settings are set
    init_semantic_search_settings = getattr(settings, "SEMANTIC_SEARCH")
    delattr(settings, "SEMANTIC_SEARCH")

    # Run ready and check that the settings are not overwritten
    config = DjangoSemanticSearchConfig(
        "django_semantic_search", django_semantic_search
    )
    config.ready()

    assert hasattr(settings, "SEMANTIC_SEARCH")
    assert settings.SEMANTIC_SEARCH == default_settings.SEMANTIC_SEARCH

    # Restore the initial settings
    setattr(settings, "SEMANTIC_SEARCH", init_semantic_search_settings)
