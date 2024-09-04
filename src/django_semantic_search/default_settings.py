# This is a reference file for the settings.py file in the django_semantic_search app.
# It contains the default settings for the app.

# TODO: fill the gaps and document each property with inline comments

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
