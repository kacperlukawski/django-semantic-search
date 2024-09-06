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

## Usage

Please refer to the [Usage](https://kacperlukawski.github.io/django-semantic-search/usage/) section in the documentation.

## Features

- Define the search fields for a model.
- Reflect the configuration in your vector search engine.
- Auto-populate the vector search engine with the data from the Django models.

For the latest documentation, visit [https://kacperlukawski.github.io/django-semantic-search/](https://kacperlukawski.github.io/django-semantic-search/).

## Roadmap

This is a general roadmap for the project. The list is not exhaustive and may change over time.

[ ] Allow using multiple fields for a single vector index.

[ ] Define overriding the default embedding model for each `VectorIndex`.

[ ] Implement wrappers for embedding models.

[ ] Add support for modalities other than text.

[ ] Improve the test coverage.

[ ] Add metadata filtering to the search method.

If you have any suggestions or feature requests, feel free to create an issue in the project's repository.
