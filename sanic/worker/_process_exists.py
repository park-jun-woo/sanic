# ff:func feature=worker type=util control=sequence
# ff:what Check if a process with the given PID exists
import os


def _process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
