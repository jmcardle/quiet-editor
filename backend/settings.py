import os

class Settings:

    file_directory = "files"

    trash_directory = os.path.join(file_directory, "trash")

    git_directory = os.path.join(file_directory, ".git")

    author = "Maelys McArdle"

    timezone = "-0400"

    file_permissions = 0o100644

    git_branch = 'refs/heads/master'