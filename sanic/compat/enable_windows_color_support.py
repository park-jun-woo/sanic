# ff:func feature=compat type=util control=sequence
# ff:what Enables color output support on Windows console
def enable_windows_color_support():
    import ctypes

    kernel = ctypes.windll.kernel32
    kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
