import django_semantic_search as dss

from .models import Product


@dss.register_document
class ProductDocument(dss.Document):
    """
    Maps the Product model to a document for the semantic search engine.
    """

    class Meta:
        model = Product
        indexes = [
            # One vector index is created for the description field
            dss.VectorIndex("description"),
            # Another vector index is created just for the name field
            dss.VectorIndex("name"),
        ]
