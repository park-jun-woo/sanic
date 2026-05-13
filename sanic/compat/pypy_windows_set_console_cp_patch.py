# ff:func feature=compat type=util control=sequence
# ff:what Patches PyPy on Windows to set console code page to UTF-8
def pypy_windows_set_console_cp_patch() -> None:
    """
    A patch function for PyPy on Windows that sets the console code page to
    UTF-8 encodingto allow for proper handling of non-ASCII characters. This
    function uses ctypes to call the Windows API functions SetConsoleCP and
    SetConsoleOutputCP to set the code page.
    """
    from ctypes import windll  # type: ignore

    code: int = windll.kernel32.GetConsoleOutputCP()
    if code != 65001:
        windll.kernel32.SetConsoleCP(65001)
        windll.kernel32.SetConsoleOutputCP(65001)
