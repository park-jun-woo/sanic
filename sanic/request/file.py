# ff:type feature=request type=model
# ff:what NamedTuple representing an uploaded file with type, body, and name

from typing import NamedTuple


class File(NamedTuple):
    """Model for defining a file.

    It is a `namedtuple`, therefore you can iterate over the object, or
    access the parameters by name.

    Args:
        type (str, optional): The mimetype, defaults to "text/plain".
        body (bytes): Bytes of the file.
        name (str): The filename.
    """

    type: str
    body: bytes
    name: str
