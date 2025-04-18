# [django-semantic-search](https://kacperlukawski.github.io/django-semantic-search/)

[![Latest PyPI version](https://img.shields.io/pypi/v/django-semantic-search.svg?style=flat-square)](https://pypi.python.org/pypi/django-semantic-search/)
[![GitHub License](https://img.shields.io/github/license/kacperlukawski/django-semantic-search)](LICENSE)

> Bringing semantic search to Django. Integrates seamlessly with Django ORM.

**Full documentation for the project is available at https://kacperlukawski.github.io/django-semantic-search/**

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

## Quickstart

Assuming, you already have a `Book` model defined in your Django application, you can define a corresponding subclass
of the `Document` class from the `django_semantic_search` package. The `Document` class maps the Django model to the
vector search engine. The document has to be registered with the `register_document` function.

```python
from django_semantic_search import Document, VectorIndex, register_document
from myapp.models import Book

@register_document
class BookDocument(Document):
    class Meta:
        model = Book
        indexes = [
            VectorIndex("title"),
            VectorIndex("description"),
        ]
```

The `BookDocument` class defines the fields that will be indexed in the vector search engine. In this case, the `title`
and `description` fields are indexed as separate vectors. The `VectorIndex` class is used to define the fields that
should be indexed.

A more detailed guide is available in the [Quickstart](https://kacperlukawski.github.io/django-semantic-search/quickstart/)
section of the documentation.

## Usage

Please refer to the [Usage](https://kacperlukawski.github.io/django-semantic-search/usage/) section in the documentation.

## Features

- Define the search fields for a model.
- Reflect the configuration in your vector search engine.
- Auto-populate the vector search engine with the data from the Django models.
- Support for multiple embedding models:
  - Sentence Transformers
  - OpenAI
  - FastEmbed (both dense and sparse embeddings)

For the latest documentation, visit [https://kacperlukawski.github.io/django-semantic-search/](https://kacperlukawski.github.io/django-semantic-search/).

## Roadmap

This is a general roadmap for the project. The list is not exhaustive and may change over time.

- [ ] Allow using multiple fields for a single vector index.
- [ ] Define overriding the default embedding model for each `VectorIndex`.
- [ ] Implement wrappers for embedding models.
- [ ] Add support for modalities other than text.
- [ ] Improve the test coverage.
- [ ] Add metadata filtering to the search method.

If you have any suggestions or feature requests, feel free to create an issue in the project's repository.
