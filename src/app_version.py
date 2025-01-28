"""Module providing a function printing python version."""
import sys
import os

def get_version_from_file(file_path="version.txt"):
    """Reads the version from the specified version file using a relative path."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_dir, file_path)
    
    if not os.path.isfile(file_path):
        return "Version file not found"
    
    with open(file_path, "r") as file:
        version = file.read().strip()
    return version


def print_version():
    """Function printing the project version."""
    version = get_version_from_file()
    print(f"Current app version: {version}")
    sys.exit(0)

if __name__ == "__main__":
    print_version()