# ff:type feature=server type=model
# ff:what Dataclass holding server instance settings, stage, and async server r

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sanic.application.constants import ServerStage
from sanic.server.async_server import AsyncioServer


@dataclass
class ApplicationServerInfo:
    """Information about a server instance."""

    settings: dict[str, Any]
    stage: ServerStage = field(default=ServerStage.STOPPED)
    server: AsyncioServer | None = field(default=None)
