# ff:type feature=logging type=filter
# ff:what Log filter that suppresses records exceeding the configured verbosity


import logging


class VerbosityFilter(logging.Filter):
    """
    Filter log records based on verbosity level.
    """

    verbosity: int = 0

    def filter(self, record: logging.LogRecord) -> bool:
        verbosity = getattr(record, "verbosity", 0)
        return verbosity <= self.verbosity
