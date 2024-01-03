from datetime import datetime

_debug = True


def __get_time() -> str:
    now = datetime.now()
    return "%02d:%02d:%02d" % (now.hour, now.minute, now.second)


# Pass all args to print function
def debug(*args):
    """Log a debug message to the console if debug mode is enabled

    All arguments are passed as-is to the print function.
    """
    if _debug:
        time = __get_time()
        print(f"[DEBUG]   [{time}]", *args)


def error(*args):
    """Log an error message to the console if debug mode is enabled

    All arguments are passed as-is to the print function.
    """
    time = __get_time()
    print(f"[ERROR]   [{time}]", *args)


def critical(*args):
    """Log a critical message to the console if debug mode is enabled

    All arguments are passed as-is to the print function.
    """
    time = __get_time()
    print(f"[CRITICAL] [{time}]", *args)
