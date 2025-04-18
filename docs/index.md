---
title: Django semantic search
---

# django-semantic-search

[![Latest PyPI version](https://img.shields.io/pypi/v/django-semantic-search.svg?style=flat-square)](https://pypi.python.org/pypi/django-semantic-search/)
[![GitHub License](https://img.shields.io/github/license/kacperlukawski/django-semantic-search)](https://github.com/kacperlukawski/django-semantic-search/LICENSE)

!!! Note ""
    Bringing semantic search to Django. Integrates seamlessly with Django ORM.

Django built-in search capabilities are rather limited. Finding a relevant instance of a model relies on the relational
database's search capabilities, like SQL `LIKE` queries. This is not ideal for high-quality search results. This library
aims to provide a semantic search capability to Django, allowing for more relevant search results. All this is done in
a Django-friendly way, integrating with Django ORM.

The library does not aim to provide all the features of search engines, but rather to provide a simple way to integrate
Django applications with semantic search capabilities, using existing vector search engines, a.k.a. vector databases,
and embedding models.

## Installation

The `django-semantic-search` library can be installed via your favorite package manager. For example, using `pip`:

```shell
pip install django-semantic-search
```

The current version is still experimental, and the API may change in the future.

## Supported tools

`django-semantic-search` has to cooperate with other tools to provide semantic search capabilities. You have to choose
a vector search engine and an embedding model to use with the library, and configure them in the Django settings.

### Vector search engines

The library supports the following vector search engines:

- [Qdrant](api/backends.md#qdrant)

If you would like to contribute support for another vector search engine, feel free to create a pull request.

### Embedding models

Choosing the right embedding model is crucial for the quality of the search results. The current version of the library
focuses on bringing the semantic search capabilities to Django, and provides integrations with the following vector embedding models:

- [Sentence Transformers](api/embeddings.md#sentence-transformers)
- [OpenAI](api/embeddings.md#openai)
- [FastEmbed](api/embeddings.md#fastembed) (currently supports dense embeddings, sparse embeddings coming soon)

In web-based applications, it makes a lot of sense to choose an external service for the embedding model, as it can be
resource-intensive. Please do expect that the library will support more embedding models in the future, and will provide
a way to integrate them with Django.

Again, if you would like to contribute support for another embedding model, feel free to create a pull request.

## Configuration

As with any Django application, you need to add the library to the `INSTALLED_APPS` list in the `settings.py` file of
your project:

```python title="settings.py"
INSTALLED_APPS = [
    ...,  # external apps, such as Django Rest Framework
    'django_semantic_search',
    ...,  # your custom apps, using django-semantic-search
]
```

All the library configuration is also done in the `settings.py` file of the project, via the `SEMANTIC_SEARCH`
dictionary. Here is a full example of the configuration:

```python title="settings.py"
--8<-- "src/django_semantic_search/default_settings.py"
```

## Quickstart

If you would like to be guided step-by-step through the installation and configuration process, please refer to the
[Quickstart](quickstart.md) guide.

## Examples

If you prefer going straight to the code, you can check the `examples` folder. In the future it will contain more
examples of how to use the library, but for the time being, it contains just a simple Django project with a single
app that demonstrates how to use the library.

### Simple Django App

The `examples` folder contains a minimal Django `simple_django_app` project using the `django-semantic-search` library.
It shows how to configure semantic search in a Django project. The application defines a simple model and a document
class for it, and demonstrates how to search for instances of the model using the library.

#### Prerequisites

By default, the `simple_django_app` project uses the `Qdrant` vector search engine and the `all-MiniLM-L6-v2` Sentence
Transformers model. You have to install the `django-semantic-search` library with the `qdrant` and `sentence-transformers`
extras to run the project. The dependencies might be installed from the requirements file:

```shell
pip install -r examples/simple_django_app/requirements.txt
```

The default configuration assumes that the Qdrant service is running on `localhost:6333`. Please refer to the Qdrant
documentation on [how to set up the service](https://qdrant.tech/documentation/quickstart/#download-and-run).
