# ff:func feature=worker type=util control=sequence
# ff:what Get current UTC datetime for worker process timestamps
from datetime import datetime, timezone


def get_now():
    now = datetime.now(tz=timezone.utc)
    return now
