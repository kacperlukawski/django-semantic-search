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
    # This model will be used when no specific embedding_model is specified for a VectorIndex.
    "default_embeddings": {
        # Either the path to the embeddings model class or the class itself
        "model": "django_semantic_search.embeddings.SentenceTransformerModel",
        # Configuration is passed directly to the embeddings model class during initialization.
        "configuration": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        },
    },
    # Optional named embedding models that can be referenced by VectorIndex instances.
    # This allows using different embedding models for different fields in your documents.
    "embedding_models": {
        # Each key is a unique identifier for the embedding model
        "title_model": {
            # Either the path to the embeddings model class or the class itself
            "model": "django_semantic_search.embeddings.SentenceTransformerModel",
            # Configuration is passed directly to the embeddings model class during initialization.
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
    },
}
