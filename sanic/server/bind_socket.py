# ff:func feature=server type=builder control=sequence
# ff:what Create and bind a TCP server socket for the given host and port
import socket

from ipaddress import ip_address


def bind_socket(host: str, port: int, *, backlog=100) -> socket.socket:
    """Create TCP server socket.
    :param host: IPv4, IPv6 or hostname may be specified
    :param port: TCP port number
    :param backlog: Maximum number of connections to queue
    :return: socket.socket object
    """
    location = (host, port)
    # socket.share, socket.fromshare
    try:  # IP address: family must be specified for IPv6 at least
        ip = ip_address(host)
        host = str(ip)
        sock = socket.socket(
            socket.AF_INET6 if ip.version == 6 else socket.AF_INET
        )
    except ValueError:  # Hostname, may become AF_INET or AF_INET6
        sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(location)
    sock.listen(backlog)
    sock.set_inheritable(True)
    return sock
