# ff:type feature=compat type=util
# ff:what Case-insensitive string enum base class for uppercase values
import sys

from enum import Enum

# Python 3.11 changed the way Enum formatting works for mixed-in types.
if sys.version_info < (3, 11, 0):

    class StrEnum(str, Enum):
        pass

else:
    from enum import StrEnum  # type: ignore # noqa


class UpperStrEnum(StrEnum):
    """Base class for string enums that are case insensitive."""

    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

    def __eq__(self, value: object) -> bool:
        value = str(value).upper()
        return super().__eq__(value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value
