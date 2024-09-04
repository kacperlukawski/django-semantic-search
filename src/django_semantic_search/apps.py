from django.apps import AppConfig
from django.conf import settings

from django_semantic_search import default_settings


class DjangoSemanticSearchConfig(AppConfig):
    name = "django_semantic_search"
    verbose_name = "Django Semantic Search"

    def ready(self):
        # Load the default settings
        # TODO: verify whether the settings are already loaded, and not overwrite them
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(settings, setting, getattr(default_settings, setting))
