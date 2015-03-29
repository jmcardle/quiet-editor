import time
import threading


updates = {}
in_memory_text = {}
unsaved_changes = {}
minimum_time_between_saves = 10

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
