# Re-export all argument groups for backward compatibility
from sanic.cli.application_group import ApplicationGroup
from sanic.cli.daemon_group import DaemonGroup
from sanic.cli.development_group import DevelopmentGroup
from sanic.cli.general_group import GeneralGroup
from sanic.cli.group import Group
from sanic.cli.http_version_group import HTTPVersionGroup
from sanic.cli.output_group import OutputGroup
from sanic.cli.socket_group import SocketGroup
from sanic.cli.tls_group import TLSGroup
from sanic.cli.worker_group import WorkerGroup

__all__ = (
    "ApplicationGroup",
    "DaemonGroup",
    "DevelopmentGroup",
    "GeneralGroup",
    "Group",
    "HTTPVersionGroup",
    "OutputGroup",
    "SocketGroup",
    "TLSGroup",
    "WorkerGroup",
)
