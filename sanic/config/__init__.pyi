from collections.abc import Sequence
from pathlib import Path
from typing import Any, Callable, Literal

from sanic.config.descriptor_meta import DescriptorMeta as DescriptorMeta
from sanic.config.detailed_converter import (
    DetailedConverter as DetailedConverter,
)
from sanic.constants import LocalCertCreator
from sanic.helpers import Default

FilterWarningType = (
    Literal["default"]
    | Literal["error"]
    | Literal["ignore"]
    | Literal["always"]
    | Literal["module"]
    | Literal["once"]
)

SANIC_PREFIX: str
DEFAULT_CONFIG: dict[str, Any]

class Config(dict, metaclass=DescriptorMeta):
    ACCESS_LOG: bool
    AUTO_EXTEND: bool
    AUTO_RELOAD: bool
    EVENT_AUTOREGISTER: bool
    DEPRECATION_FILTER: FilterWarningType
    FORWARDED_FOR_HEADER: str
    FORWARDED_SECRET: str | None
    GRACEFUL_SHUTDOWN_TIMEOUT: float
    GRACEFUL_TCP_CLOSE_TIMEOUT: float
    INSPECTOR: bool
    INSPECTOR_HOST: str
    INSPECTOR_PORT: int
    INSPECTOR_TLS_KEY: Path | str | Default
    INSPECTOR_TLS_CERT: Path | str | Default
    INSPECTOR_API_KEY: str
    KEEP_ALIVE_TIMEOUT: int
    KEEP_ALIVE: bool
    LOCAL_CERT_CREATOR: str | LocalCertCreator
    LOCAL_TLS_KEY: Path | str | Default
    LOCAL_TLS_CERT: Path | str | Default
    LOCALHOST: str
    LOG_EXTRA: Default | bool
    MOTD: bool
    MOTD_DISPLAY: dict[str, str]
    NO_COLOR: bool
    NOISY_EXCEPTIONS: bool
    PROXIES_COUNT: int | None
    REAL_IP_HEADER: str | None
    REQUEST_BUFFER_SIZE: int
    REQUEST_MAX_HEADER_SIZE: int
    REQUEST_ID_HEADER: str
    REQUEST_MAX_SIZE: int
    REQUEST_TIMEOUT: int
    RESPONSE_TIMEOUT: int
    SERVER_NAME: str
    TLS_CERT_PASSWORD: str
    TOUCHUP: Default | bool
    USE_UVLOOP: Default | bool
    WEBSOCKET_MAX_SIZE: int
    WEBSOCKET_PING_INTERVAL: int
    WEBSOCKET_PING_TIMEOUT: int
    def __init__(
        self,
        defaults: dict[str, str | bool | int | float | None] | None = None,
        env_prefix: str | None = ...,
        keep_alive: bool | None = None,
        *,
        converters: Sequence[Callable[[str], Any]] | None = None,
    ): ...
    def __getattr__(self, attr: Any) -> Any: ...
    def __setattr__(self, attr: str, value: Any) -> None: ...
    def __setitem__(self, attr: str, value: Any) -> None: ...
    def update(self, *other: Any, **kwargs: Any) -> None: ...
    @property
    def FALLBACK_ERROR_FORMAT(self) -> str: ...
    @FALLBACK_ERROR_FORMAT.setter
    def FALLBACK_ERROR_FORMAT(self, value: Any) -> None: ...
    def load_environment_vars(self, prefix: str = ...) -> None: ...
    def update_config(
        self, config: bytes | str | dict[str, Any] | Any
    ) -> None: ...
    def register_type(self, converter: Callable[[str], Any]) -> None: ...

__all__: list[str]
