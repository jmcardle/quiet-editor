import sqlite3
import zlib


class Storage:

    def __init__(self, database_path="files.db"):

        self._database_path = database_path


    def __enter__(self):

        self._database = sqlite3.connect(self._database_path)
        self._cursor = self._database.cursor()

        # Create tables if they don't exist.
        self._cursor.execute(Query.initialize_files_table)
        self._cursor.execute(Query.initialize_revisions_table)

        return self


    def __exit__(self, exception_type, exception_value, traceback):

        # If no errors, commit.
        if not exception_type:

            # Save changes.
            self._database.commit()

        else:

            # Inform of failure.
            print((exception_type, exception_value))
            print(traceback)

        # Close.
        self._database.close()


    def list(self):

        self._cursor.execute(Query.list_files)
        return self._cursor.fetchall()


    def list_deleted(self):

        self._cursor.execute(Query.list_deleted_files)
        return self._cursor.fetchall()


    def rename(self, file_name, new_file_name):

        self._cursor.execute(Query.rename_file, (new_file_name, file_name))


    def delete(self, file_name):

        self._cursor.execute(Query.delete_file, (file_name,))


    def restore_deleted(self, file_id, new_file_name):

        self._cursor.execute(Query.restore_deleted_file, (new_file_name, file_id))


    def collect_garbage(self):

        self._cursor.execute(Query.collect_garbage)


    def read(self, file_name):

        # Get the revision.
        self._cursor.execute(Query.get_latest_revision, (file_name,))
        result = self._cursor.fetchone()

        if result:

            # Return the data with decompressed text.
            time_stamp, compressed_content = result
            return zlib.decompress(compressed_content).decode()

        else:

            return ()

    def write(self, file_name, contents):

        # Store the file name if it doesn't exist.
        self._cursor.execute(Query.initialize_file, (file_name,))

        # Get the row ID for the file name.
        self._cursor.execute(Query.get_file_id, (file_name,))
        file_id = self._cursor.fetchone()[0]

        # Store the compressed text.
        compressed_text = zlib.compress(contents.encode())
        self._cursor.execute(Query.insert_revision, (file_id, compressed_text))


    def list_revisions(self, file_name):

        self._cursor.execute(Query.get_revisions_list, (file_name,))
        return self._cursor.fetchall()


    def get_revision(self, revision_id):

        # Get the revision.
        self._cursor.execute(Query.get_revision, (revision_id,))
        time_stamp, compressed_content = self._cursor.fetchone()

        # Return the data with decompressed text.
        return time_stamp, zlib.decompress(compressed_content).decode()


class Query:

    initialize_files_table = """
        CREATE TABLE IF NOT EXISTS files (
            id   INTEGER PRIMARY KEY,
            name TEXT,
            deleted INTEGER,
            UNIQUE(name)
        );
        """

    initialize_revisions_table = """
        CREATE TABLE IF NOT EXISTS revisions (
            id                  INTEGER PRIMARY KEY,
            file_id             INTEGER,
            timestamp           DATETIME DEFAULT CURRENT_TIMESTAMP,
            compressed_contents BLOB,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        );
        """

    initialize_file = """
        INSERT OR IGNORE INTO files (
            name,
            deleted
        ) VALUES (
            ?,
            0
        );
        """

    delete_file = """
        UPDATE
            files
        SET
            name = printf("deleted_%s_%s", ?, lower(hex(randomblob(16)))),
            deleted = 1
        WHERE
            name = ?
        """

    restore_deleted_file = """
         UPDATE
            files
        SET
            name = ?
            deleted = 0
        WHERE
            id = ?
        """

    collect_garbage = """
        DELETE FROM
            files
        WHERE
            deleted = 1;
        """

    rename_file = """
        UPDATE
            files
        SET
            name = ?
        WHERE
            name = ?
        """

    list_files = """
        SELECT
            name
        FROM
            files
        WHERE
            deleted = 0;
        """

    list_deleted_files = """
        SELECT
            id,
            name
        FROM
            files
        WHERE
            deleted = 1;
        """

    get_file_id = """
        SELECT
            id
        FROM
            files
        WHERE
            name = ?;
        """

    insert_revision = """
        INSERT INTO revisions (
            file_id,
            compressed_contents
        ) VALUES (
            ?,
            ?
        )
        """

    get_latest_revision = """
        SELECT
            r.timestamp,
            r.compressed_contents
        FROM
            revisions AS r
        JOIN
            files AS f
        ON
            f.id = r.file_id
        WHERE
            f.name = ?
        AND
            f.deleted = 0
        ORDER BY
            f.id
        DESC
        LIMIT
            1;
        """

    get_revisions_list = """
        SELECT
            r.id,
            r.timestamp
        FROM
            revisions AS r
        JOIN
            files AS f
        ON
            f.id = r.file_id
        WHERE
            f.name = ?
        AND
            f.deleted = 0
    """

    get_revision = """
        SELECT
            timestamp,
            compressed_contents
        FROM
            revisions
        WHERE
            id = ?;
    """
