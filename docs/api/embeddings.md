---
title: Embedding models
---

An embedding model is a tool that converts text data into a vector representation. The quality of the embedding model
is crucial for the quality of the search results. Currently, `django-semantic-search` supports just a single integration
with the vector embedding models:

## Sentence Transformers

The [Sentence Transformers](https://www.sbert.net) library provides a way to convert text data into a vector
representation. There are [over 5,000 pre-trained models
available](https://huggingface.co/models?library=sentence-transformers), and you can choose the one that fits your needs the
best.

One of the available models is `all-MiniLM-L6-v2`, which is a lightweight model that provides a good balance between the
quality of the search results and the resource consumption.

::: django_semantic_search.embeddings.SentenceTransformerModel
    options:
        members:
            - __init__
            - embed_document
            - embed_query
            - vector_size

## OpenAI

[OpenAI](https://platform.openai.com/docs/guides/embeddings) provides powerful embedding models through their API. The default model is `text-embedding-3-small`, which offers a good balance between quality and cost.

To use OpenAI embeddings, first install the required dependencies:

```bash
pip install django-semantic-search[openai]
```

Then configure it in your Django settings:

```python title="settings.py"
SEMANTIC_SEARCH = {
    "default_embeddings": {
        "model": "django_semantic_search.embeddings.OpenAIEmbeddingModel",
        "configuration": {
            "model": "text-embedding-3-small",
            "api_key": "your-api-key",  # Optional if set in env
        },
    },
    ...
}
```

The API key can also be provided through the `OPENAI_API_KEY` environment variable.

::: django_semantic_search.embeddings.OpenAIEmbeddingModel
    options:
        members:
            - __init__
            - embed_document
            - embed_query
            - vector_size
