# ff:func feature=http type=parser control=iteration dimension=1
# ff:what Parses authentication credentials from a header value
from __future__ import annotations


def parse_credentials(
    header: str | None,
    prefixes: list | tuple | set | None = None,
) -> tuple[str | None, str | None]:
    """Parses any header with the aim to retrieve any credentials from it.

    Args:
        header (Optional[str]): The header to parse.
        prefixes (Optional[Union[List, Tuple, Set]], optional): The prefixes to look for. Defaults to None.

    Returns:
        Tuple[Optional[str], Optional[str]]: The prefix and the credentials.
    """  # noqa: E501
    if not prefixes or not isinstance(prefixes, (list, tuple, set)):
        prefixes = ("Basic", "Bearer", "Token")
    if header is None:
        return None, header
    for prefix in prefixes:
        if prefix in header:
            return prefix, header.partition(prefix)[-1].strip()
    return None, header
