---
title: "Usage"
---

This section focuses on specific usage examples of the `django-semantic-search` library. If you are looking for
a step-by-step introduction, please refer to the [Quickstart](quickstart.md) guide.

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

All the library configuration is done in the `settings.py` file of the project, via the `SEMANTIC_SEARCH`
dictionary. Here is a full example of the configuration:

```python title="settings.py"
--8<-- "src/django_semantic_search/default_settings.py"
```

### Using Different Embedding Models

You can define multiple embedding models in the settings and use them for different fields in your documents:

```python title="settings.py"
SEMANTIC_SEARCH = {
    "default_embeddings": {
        "model": "django_semantic_search.embeddings.SentenceTransformerModel",
        "configuration": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        },
    },
    "embedding_models": {
        "title_model": {
            "model": "django_semantic_search.embeddings.SentenceTransformerModel",
            "configuration": {
                "model_name": "sentence-transformers/all-mpnet-base-v2",
                "document_prompt": "Title: ",
            },
        },
        "content_model": {
            "model": "django_semantic_search.embeddings.OpenAIEmbeddingModel",
            "configuration": {
                "model": "text-embedding-3-small",
            },
        },
    }
}
```

Then reference these models in your document definitions:

```python title="books/documents.py"
@register_document
class BookDocument(Document):
    class Meta:
        model = Book
        indexes = [
            VectorIndex("title", embedding_model="title_model"),  # Uses title_model
            VectorIndex("content", embedding_model="content_model"),  # Uses content_model
            VectorIndex("description"),  # Uses default_embeddings
        ]
```

If no specific embedding model is specified for a `VectorIndex`, it will use the model defined in `default_embeddings`.

## Frequently Asked Questions

This section describes some common questions and answers related to the `django-semantic-search` library.

### How to define which fields are searchable?

To define the search fields for a model, you need to create a document class that inherits from
`django_semantic_search.Document`. There is no strict requirement for the document class to be put in a specific
package, but it is recommended to put it in the `documents.py` file in the app package.

Assuming, we have a `Book` model with the `title`, `author`, and `description` fields:

```python title="books/models.py"
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
```

Here is an example of a document class for the `Book` model, with the `title` and `description` fields defined as
searchable:

```python title="books/documents.py"
from django_semantic_search import Document, VectorIndex
from books.models import Book

class BookDocument(Document):
    class Meta:
        model = Book
        indexes = [
            VectorIndex("title"),
            VectorIndex("description"),
        ]
```

Currently, the default embedding model is used for all the fields.

### How to search for documents?

To search for documents, you can use the `search` method of the document class. The method returns a Django queryset
with the search results.

Here is an example of searching for books with the title containing the word "Django":

```python title="books/views.py"
from books.documents import BookDocument

def search_books(request):
    query = "Django"
    books = BookDocument.objects.search(title=query)
    return render(request, "books/search_results.html", {"books": books})
```

Using the named arguments in the `search` method allows you to search for documents with specific fields.

### How to index the existing data?

If you are adding the `django-semantic-search` library to an existing project, you may want to index the existing
instances of the models. To do this, you can use the `index` method of the document class.

Here is an example of indexing all the existing instances of the `Book` model:

```python title="index_models.py"
from books.models import Book
from books.documents import BookDocument

def index_books(request):
    all_books = Book.objects.all()
    BookDocument.objects.index(all_books)
    return HttpResponse("Books indexed successfully.")
```

!!!Warning
    Indexing all the instances of the model can be resource-intensive, as each instance of the model has to be converted
    to the vector representation. It is recommended to run the indexing process in a background task or a separate
    management command.
