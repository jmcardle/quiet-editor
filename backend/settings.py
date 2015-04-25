import os

class Settings:

    file_directory = "files"

    trash_directory = os.path.join(file_directory, "trash")

    repository = os.path.join(file_directory, ".git")

    author = "Maëlys McArdle"

    email = ""

    timezone = "-0400"

    file_permissions = 0o100644

    branch = 'refs/heads/master'