# ff:type feature=error type=exception
# ff:what Exception raised when the Sanic server process is killed unexpectedly
class ServerKilled(Exception):
    """Exception Sanic server uses when killing a server process for something unexpected happening."""  # noqa: E501

    quiet = True
