# ff:type feature=http type=constant
# ff:what HTTP version enum (HTTP/1.1, HTTP/3)

from enum import IntEnum


class HTTP(IntEnum):
    """Enum for representing HTTP versions"""

    VERSION_1 = 1
    VERSION_3 = 3

    def display(self) -> str:
        value = 1.1 if self.value == 1 else self.value
        return f"HTTP/{value}"
