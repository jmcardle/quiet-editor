import time
import threading
import sqlite3
import zlib

updates = {}
in_memory_text = {}
unsaved_changes = {}
minimum_time_between_saves = 10
DATABASE_NAME = "storage.db"

def add_revision(database_name, file_name, contents):

    database = sqlite3.connect(database_name)
    cursor = database.cursor()

    # Create tables if they don't exist.
    cursor.execute('CREATE TABLE IF NOT EXISTS file_names (id INTEGER PRIMARY KEY, name TEXT, UNIQUE(name));')
    cursor.execute('CREATE TABLE IF NOT EXISTS file_revisions (id INTEGER PRIMARY KEY, file_id INTEGER, '
                   'Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, compressed_contents BLOB, '
                   'FOREIGN KEY (file_id_exists) REFERENCES file_names(id));')

    # Store the file name if it doesn't exist.
    cursor.execute('INSERT OR IGNORE INTO file_names(name) VALUES(?)', (file_name,))

    # Get the row ID for the file name.
    cursor.execute('SELECT id FROM file_names WHERE name=?', (file_name,))
    file_id = cursor.fetchone()[0]

    # Store the compressed text.
    compressed_text = zlib.compress(contents)
    cursor.execute('INSERT INTO file_revisions (file_id, compressed_contents) VALUES (?, ?)',
                   (file_id, compressed_text))

    # Save changes and close.
    database.commit()
    database.close()



def check_unsaved():
    for file_name in unsaved_changes:
        if unsaved_changes[file_name]:
            print("%s has unsaved changes" % (file_name))
            update(file_name, in_memory_text[file_name])
    threading.Timer(5, check_unsaved).start()

check_unsaved()

def get(file_name):
    print("Loaded %s" % (file_name))
    try:
        with open(file_name) as file:
            contents = file.read()
            in_memory_text[file_name] = contents
            return contents
    except IOError:
        return ""


def update(file_name, text):
    print("I got %s" % text)
    current_time = time.time()
    previous_update = None

    if file_name in updates:
        previous_update = updates[file_name]

    if not previous_update or current_time - previous_update > minimum_time_between_saves:

        with open(file_name, "w") as file:
            file.write(text)

        print("Saved %s" % (file_name))
        updates[file_name] = current_time
        unsaved_changes[file_name] = False

    else:

        unsaved_changes[file_name] = True
        print("Difference not saved to %s as %i seconds elapsed" % (file_name, current_time - previous_update))

    in_memory_text[file_name] = text
