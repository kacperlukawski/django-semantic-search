from django.apps import AppConfig
from django.conf import settings

from django_semantic_search import default_settings


class DjangoSemanticSearchConfig(AppConfig):
    name = "django_semantic_search"
    verbose_name = "Django Semantic Search"

    def ready(self):
        # Load the default settings
        for setting in dir(default_settings):
            if setting.isupper() and not hasattr(settings, setting):
                setattr(settings, setting, getattr(default_settings, setting))
