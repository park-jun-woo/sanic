# ff:type feature=touchup type=model
# ff:what Touchup scheme that checks and optimizes alt-svc header generation

from __future__ import annotations

from ast import NodeTransformer
from typing import TYPE_CHECKING

from .base import BaseScheme
from .remove_alt_svc import RemoveAltSvc

if TYPE_CHECKING:
    pass


class AltSvcCheck(BaseScheme):
    ident = "ALTSVC"

    def visitors(self) -> list[NodeTransformer]:
        return [RemoveAltSvc(self.app, self.app.state.verbosity)]
