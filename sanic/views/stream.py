# ff:func feature=routing type=util control=sequence
# ff:what Decorator to mark a function as a stream handler
def stream(func):
    """Decorator to mark a function as a stream handler."""
    func.is_stream = True
    return func
