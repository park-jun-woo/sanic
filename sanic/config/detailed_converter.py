# ff:type feature=core type=config
# ff:what Abstract base class for environment variable converters with full con
from abc import ABC, abstractmethod
from typing import Any


class DetailedConverter(ABC):
    """Base class for detailed converters that need additional context.

    DetailedConverter provides access to the full environment variable key,
    the raw value, and the current config defaults. This allows for more
    sophisticated conversion logic that can take into account the variable
    name pattern, perform validation, or use default values for fallback.

    Examples:
        ```python
        # Example of a converter that casts values to the type of the default
        class DefaultsCastConverter(DetailedConverter):
            def __call__(self, full_key: str, config_key: str, value: str,
                                                        defaults: dict) -> Any:
                try:
                    if config_key in defaults:
                        return type(defaults[config_key])(value)
                except (ValueError, TypeError):
                    raise ValueError
        ```
    """

    @abstractmethod
    def __call__(
        self, full_key: str, config_key: str, value: str, defaults: dict
    ) -> Any:
        """Convert an environment variable to a Python value.

        Args:
            full_key: The full environment variable name (with prefix)
                            (e.g., "SANIC_DATABASE_URL")
            config_key: The environment variable name (without prefix)
                            (e.g., "DATABASE_URL")
            value: The raw string value from the environment
            defaults: The current default configuration values

        Returns:
            The converted Python value

        Raises:
            ValueError: If the value cannot be converted by this converter
        """
