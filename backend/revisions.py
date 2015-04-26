import pygit2
import datetime
from settings import Settings

class Revisions:

    def __init__(self):

        self.repo = self.open_or_create_repository(Settings.repository)

    def open_or_create_repository(self, repository):

        try:
            return pygit2.Repository(repository)

        except KeyError:
            return pygit2.init_repository(repository)

    def commit(self, message, filename, contents):

        id  = self.repo.create_blob(contents)
        blob = self.repo[id]

        tree = self.repo.TreeBuilder()
        tree.insert(filename, blob.id, pygit2.GIT_FILEMODE_BLOB)
        tree = tree.write()

        self.apply_commit(tree, message)

    def apply_commit(self, tree, message):

        author = pygit2.Signature(Settings.author.encode('utf-8'), Settings.email)
        committer = pygit2.Signature(Settings.author.encode('utf-8'), Settings.email)

        if self.repo.head_is_unborn:

            # First commit.
            self.repo.create_commit(Settings.branch, author, committer, message, tree, [])

        else:

            # Second commit onwards.
            last_commit = self.head()
            self.repo.create_commit(Settings.branch, author, committer, message, tree, [last_commit.id])

    def delete(self, filename):

        tree = self.repo.TreeBuilder()
        tree.remove(filename)
        tree = tree.write()

        self.apply_commit(tree, "Deleted " + filename)

    def head(self):
        return self.repo.revparse_single('HEAD')

    def log(self):
        return [[commit.id, datetime.datetime.fromtimestamp(commit.commit_time).isoformat(),
                 commit.committer.name, commit.message]
                for commit in self.repo.walk(self.head().oid, pygit2.GIT_SORT_TIME | pygit2.GIT_SORT_REVERSE)]

    def get(self, commit_id, filename):

        commit = self.repo.get(commit_id)
        if filename in commit.tree:
             return self.repo.get(commit.tree[filename].oid).data

        return None