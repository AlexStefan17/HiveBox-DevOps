"""Module providing a function printing python version."""
import sys

VERSION = "v0.2.0"

def print_version():
    """Function printing project version."""
    print(f"Current app version: {VERSION}")
    sys.exit(0)

if __name__ == "__main__":
    print_version()