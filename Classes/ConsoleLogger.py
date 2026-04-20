# The ConsoleLogger class is a simple class that logs messages to the console. It is used as a default logger in the RaceState class.
# It is a simple class that has a single method, log, which takes a title and a message and logs the message to the console.


class ConsoleLogger:
    def __init__(self):
        pass

    def log(self, message, title=None, verbose=True):
        if not verbose:
            return

        if title is None:
            print(message)
        else:
            print(f"[{title}] {message}")
