from datetime import datetime

_debug = True


# Pass all args to print function
def debug(*args):
    """Log a debug message to the console if debug mode is enabled

    All arguments are passed as-is to the print function.
    """
    if _debug:
        time = datetime.now().strftime("%H:%M:%S")
        print(f"[DEBUG]   [{time}]", *args)


def error(*args):
    """Log an error message to the console if debug mode is enabled

    All arguments are passed as-is to the print function.
    """
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[ERROR]   [{time}]", *args)


def critical(*args):
    """Log a critical message to the console if debug mode is enabled

    All arguments are passed as-is to the print function.
    """
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[CRITICAL] [{time}]", *args)
