from os import path


def get_root_directory(current_directory: str) -> str:
    while not path.isfile(path.join(current_directory, "main.py")):
        current_directory = path.dirname(current_directory)
    return current_directory
