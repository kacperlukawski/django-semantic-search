---
title: API Reference
---

`django-semantic-search` was designed to mimic some of the patterns used in popular Django libraries, such as
`django-import-export` to reduce the learning curve for new users.

The base concept of the library is a `Document` subclass that represents a single searchable entity. The library
provides a way to define a document class for a selected model. The document class is responsible for converting
the model instances into the vector representation and storing them in the vector search engine, as well as for
performing the search queries.

## Documents

::: django_semantic_search.Document
    options:
        members: false
