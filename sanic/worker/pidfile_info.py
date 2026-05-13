# ff:type feature=worker type=model
# ff:what Immutable data class holding parsed PID file metadata
from dataclasses import dataclass


@dataclass(frozen=True)
class PidfileInfo:
    pid: int
    started: int | None = None
    name: str | None = None
