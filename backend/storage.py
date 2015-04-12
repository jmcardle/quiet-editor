import os.path
import base64

files = {}
file_directory = "../files"

def get(file_name):

    # Copy exists in memory.
    if file_name in files:
        return files[file_name]

    # Copy exists on disk. Load it in memory.
    elif file_exists(file_name):
        text = read_file(file_name)
        files[file_name] = text
        return text

    # No copy exists.
    else:
        return ""

def update(file_name, text):

    # File doesn't exist or isn't in database.
    if not file_exists(file_name) or file_name not in files:
        write_file(file_name, text)

    # Just text is appended.
    elif text.startswith(files[file_name]):
        append_file(file_name, text[len(files[file_name]):])

    # Just text is removed.
    elif files[file_name].startswith(text):
        truncate_file(file_name, len(text))

    # Content added elsewhere.
    else:
        write_file(file_name, text)

    # Update memory.
    files[file_name] = text

def write_file(file_name, content, mode="w"):
    with open(to_safe_filename(file_name), mode) as file:
        file.write(content)

def append_file(file_name, content):
    write_file(file_name, content, "a")

def read_file(file_name):
    with open(to_safe_filename(file_name), "r") as file:
        return file.read()

def truncate_file(file_name, size):
    with open(to_safe_filename(file_name), "w") as file:
        file.truncate(size)

def file_exists(file_name):
    return os.path.isfile(to_safe_filename(file_name))

def to_safe_filename(file_name):
    return os.path.join(file_directory, base64.urlsafe_b64encode(file_name.encode()).decode())

def from_safe_filename(file_name):
    return base64.urlsafe_b64decode(os.path.basename(file_name)).decode()