from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit, parse_timezone
import dulwich.errors
from settings import Settings
from time import time
import os

class Revisions:

    def __init__(self):

        self.repo = self.open_or_create_repository(Settings.file_directory)

    def open_or_create_repository(self, repository):

        try:
            return Repo(repository)

        except dulwich.errors.NotGitRepository:
            return Repo.init(repository)

    def commit_file(self, message, filename, contents):

        blob = Blob.from_string(contents)

        tree = Tree()
        if filename in tree:
            tree[filename] = (Settings.file_permissions, blob.id)
        else:
            tree.add(filename, Settings.file_permissions, blob.id)

        commit = Commit()
        commit.tree = tree.id
        commit.author = commit.committer = Settings.author
        commit.commit_time = commit.author_time = int(time())
        commit.commit_timezone = commit.author_timezone = parse_timezone(Settings.timezone)[0]
        commit.encoding = "UTF-8"
        commit.message = message

        if Settings.git_branch in self.repo.refs:
            commit.parents = self.repo.refs[Settings.git_branch]

        object_store = self.repo.object_store
        object_store.add_object(blob)
        object_store.add_object(tree)
        object_store.add_object(commit)

        self.repo.refs[Settings.git_branch] = commit.id
        head = self.repo.refs['HEAD']