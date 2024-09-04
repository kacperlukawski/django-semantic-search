from typing import List, Union

Vector = List[float]
DocumentID = Union[int, str]
# TODO: support more types in the metadata value, preferably the same as in the database
MetadataValue = Union[int, str, float, bool]
