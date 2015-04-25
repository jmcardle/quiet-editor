import pygit2
from settings import Settings
from time import time

class Revisions:

    def __init__(self):

        self.repo = self.open_or_create_repository(Settings.repository)

    def open_or_create_repository(self, repository):

        try:
            return pygit2.Repository(repository)
        except KeyError:
            return pygit2.init_repository(repository)

    def commit_file(self, message, filename, contents):

        id  = self.repo.create_blob(contents)
        blob = self.repo[id]

        tree = self.repo.TreeBuilder()
        tree.insert(filename, blob.id, pygit2.GIT_FILEMODE_BLOB)
        tree = tree.write()

        author = pygit2.Signature(Settings.author, Settings.email)
        committer = pygit2.Signature(Settings.author, Settings.email)

        self.repo.create_commit(Settings.branch, author, committer, message, tree, [])