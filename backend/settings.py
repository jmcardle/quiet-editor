import os

class Settings:

    @property
    def file_directory(self):
        return "files"

    @property
    def trash_directory(self):
        return os.path.join(self.file_directory, "trash")

    @property
    def author(self):
        return "Maëlys McArdle"

    @property
    def timezone(self):
        return "-0400"

    @property
    def file_permissions(self):
        return 0o100644

    @property
    def git_branch(self):
        return 'refs/heads/master'