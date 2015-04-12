import os.path

files = {}

def get(file_name):

    # Copy exists in memory.
    if file_name in files:
        return files[file_name]

    # Copy exists on disk. Load it in memory.
    elif os.path.isfile(file_name):
        with open(file_name, "r") as file:
            text = file.read()
            files[file_name] = text
            return text

    # No copy exists.
    else:
        return ""

def update(file_name, text):

    # File doesn't exist or isn't in database.
    if not os.path.isfile(file_name) or file_name not in files:
        with open(file_name, "w") as file:
            file.write(text)

    # Just text is appended.
    elif text.startswith(files[file_name]):
        with open(file_name, "a") as file:
            file.write(text[len(files[file_name]):])

    # Just text is removed.
    elif files[file_name].startswith(text):
        with open(file_name, "w") as file:
            file.truncate(len(text))

    # Content added elsewhere.
    else:
        with open(file_name, "w") as file:
            file.write(text)

    # Update memory.
    files[file_name] = text