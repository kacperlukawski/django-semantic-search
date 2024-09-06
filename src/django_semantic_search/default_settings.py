SEMANTIC_SEARCH = {
    # Vector store is a backend that stores the vectors and provides the search functionality.
    "vector_store": {
        # Either the path to the backend class or the class itself
        "backend": "django_semantic_search.backends.qdrant.QdrantBackend",
        # Configuration is passed directly to the backend class during initialization.
        "configuration": {
            "location": "http://localhost:6333",
        },
    },
    # Default embeddings are used to generate the embeddings for the documents if no embeddings are provided.
    # For the time being, there is no way to provide embeddings for the documents, so the default embeddings
    # are used for all the documents.
    "default_embeddings": {
        # Either the path to the embeddings model class or the class itself
        "model": "django_semantic_search.embeddings.SentenceTransformerModel",
        # Configuration is passed directly to the embeddings model class during initialization.
        "configuration": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        },
    },
}
