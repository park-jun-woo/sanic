# ff:type feature=worker type=exception
# ff:what Exception raised for daemon configuration and runtime errors
class DaemonError(Exception):
    pass
