"""Module providing a function printing python version."""
import sys

def print_version():
    """Function printing project version."""
    version = "v0.0.1"
    print(f"Current app version: {version}")
    sys.exit(0)

if __name__ == "__main__":
    print_version()