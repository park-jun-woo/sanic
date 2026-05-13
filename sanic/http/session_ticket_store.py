# ff:type feature=http type=handler
# ff:what Simple in-memory store for QUIC session tickets
from __future__ import annotations

from typing import TYPE_CHECKING

try:
    from aioquic.tls import SessionTicket

    HTTP3_AVAILABLE = True
except ModuleNotFoundError:  # no cov
    HTTP3_AVAILABLE = False

if TYPE_CHECKING:
    from aioquic.tls import SessionTicket


class SessionTicketStore:
    """
    Simple in-memory store for session tickets.
    """

    def __init__(self) -> None:
        self.tickets: dict[bytes, SessionTicket] = {}

    def add(self, ticket: SessionTicket) -> None:
        self.tickets[ticket.ticket] = ticket

    def pop(self, label: bytes) -> SessionTicket | None:
        return self.tickets.pop(label, None)
