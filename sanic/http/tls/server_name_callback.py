# ff:func feature=http type=handler control=sequence
# ff:what Store the received SNI as sslobj.sanic_server_name for later certific
import ssl


def server_name_callback(
    sslobj: ssl.SSLObject, server_name: str, ctx: ssl.SSLContext
) -> None:
    """Store the received SNI as sslobj.sanic_server_name."""
    sslobj.sanic_server_name = server_name  # type: ignore
