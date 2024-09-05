# [django-semantic-search](https://kacperlukawski.github.io/django-semantic-search/)

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
