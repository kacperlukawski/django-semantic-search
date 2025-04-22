---
title: Quickstart
---

This quickstart guide will help you to get started with the `django-semantic-search` library. It will guide you through
the installation process, the configuration of the vector search engine and the embedding model, and the definition of
documents for the selected model.

Assuming you already have a Django project set up, let's get started.

## 1. Install django-semantic-search

The `django-semantic-search` library can be installed via your favorite package manager. For example, using `pip`:

```shell
pip install django-semantic-search
```

The default installation does not include any vector search engine or embedding model, so you typically have to install
the package with the desired support. For example, to install the package with [Qdrant](https://qdrant.tech) and
[Sentence Transformers](https://www.sbert.net) support, you can run:

```shell
pip install django-semantic-search[qdrant,sentence-transformers]
```

## 2. Modify the Django settings

Add the library to the `INSTALLED_APPS` list in the `settings.py` file of your project:

```python title="settings.py"
INSTALLED_APPS = [
    ...,  # external apps, such as Django Rest Framework
    'django_semantic_search',
    ...,  # your custom apps, using django-semantic-search
]
```

## 3. Choose the vector search engine and the embedding model

Do not close the `settings.py` file yet. You need to configure the vector search engine and the embedding model. Add the
`SEMANTIC_SEARCH` dictionary to the `settings.py` file of the project. Here is a basic example:

```python title="settings.py"
SEMANTIC_SEARCH = {
    "vector_store": {
        "backend": "django_semantic_search.backends.qdrant.QdrantBackend",
        "configuration": {
            "location": "http://localhost:6333",
        },
    },
    "default_embeddings": {
        "model": "django_semantic_search.embeddings.SentenceTransformerModel",
        "configuration": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        },
    },
}
```

For more advanced configurations, including using different embedding models for different fields, see the [Embedding Models](api/embeddings.md) documentation.

## 4. Create a model class (skip if you already have one)

Our example will use a simple model class, `Book`, with the `title`, `author`, and `description` fields. Here is the
model definition:

```python title="books/models.py"
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
```

A newly created model means we need to create a migration and apply it to the database:

```shell
python manage.py makemigrations
python manage.py migrate
```

## 5. Define document class for the selected model

Once the model is defined, you need to create a document class that inherits from `django_semantic_search.Document`.

Assuming we have a `Book` model with the `title`, `author`, and `description` fields, here is an example of a document
class for the `Book` model, with the `title` and `description` fields defined as searchable. Please do not forget to
use the `register_document` decorator to register the document class with the library.

```python title="books/documents.py"
from django_semantic_search import Document, VectorIndex, register_document
from books.models import Book

@register_document
class BookDocument(Document):
    class Meta:
        model = Book
        indexes = [
            VectorIndex("title"),
            VectorIndex("description"),
        ]
```

Currently, only single fields can be used for the vector index.

The decorator `register_document` takes care of creating the signals for the model, so all the created/updated/deleted
instances of the model will be automatically indexed in the vector search engine.

## 6. Create and store the instances of the model

From now on, whenever you create or update an instance of the `Book` model, the instance will be automatically indexed
in the vector search engine. Here is an example of creating a new instance of the `Book` model:

```python title="books/views.py"
from books.models import Book

def create_book(request):
    book = Book.objects.create(
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        description="The Lord of the Rings is an epic high-fantasy novel by the English author and scholar J. R. R. Tolkien."
    )
    return book
```

The `create_book` function creates a new instance of the `Book` model with the title, author, and description fields
filled in. The instance is then returned. Under the hood, a corresponding document is created and indexed in the vector
search engine. It ignores the `author` field, as it is not defined as a searchable field in the `BookDocument` class.

## 7. Search for the instances of the model

The `BookDocument` class serves as a bridge between the Django model and the vector search engine. You can use the
`search` method to find the most relevant instances of the model. Here is an example of searching for the instances of
the `Book` model:

```python title="books/views.py"
from books.documents import BookDocument

results = BookDocument.objects.search(title=query)
```

We specifically chose the `title` field to search for the instances of the `Book` model. The `search` method returns a
queryset of the most relevant instances of the model, based on the search query. Alternatively, you can search for the
instances using the `description` field:

```python title="books/views.py"
results = BookDocument.objects.search(description=query)
```

Currently, only a single field can be used for the search query, but we plan to extend this functionality in the future.

!!!Info
    This tutorial covers the happy path of using the `django-semantic-search` library. If you encounter any issues or
    have any questions, feel free to create an issue in the project's repository. Please make sure to check the list of
    [Frequency Asked Questions](usage.md#frequently-asked-questions) before creating a new issue.
