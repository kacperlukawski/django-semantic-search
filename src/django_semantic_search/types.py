from typing import Dict, List, Union

# Dense vector is a list of floats
DenseVector = List[float]

# Sparse vector is a dictionary of the form {index: value}
# where index is a unique token identifier and value is the weight of the token.
# Different backends may store the sparse vector in a different way.
SparseVector = Dict[int, float]

# Vector is either a dense or a sparse vector for now, but that might
# change in the future, for example, to support multi-vector representations.
Vector = Union[DenseVector, SparseVector]

# Document ID uniquely identifies a document.
DocumentID = Union[int, str]

# Document content might be any supported modality. Currently just text, but that
# might change in the future, when we support images, audio, etc.
DocumentContent = Union[str]

# Each document may have metadata associated with it, that can be used for filtering.
# For now, we support only a few basic types, but that might change in the future.
# TODO: support more types in the metadata value, preferably the same as in the database
MetadataValue = Union[int, str, float, bool]

# Queries may have the same format as the documents, but we keep a separate type for
# them for better readability.
Query = DocumentContent
