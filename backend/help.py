
help = """# Help

## Listing Available Files

### list
Lists files that can be loaded.

### list trash
Lists contents of the trash bin. Use *restore* to retrieve files from the trash.

## Opening / Saving Files

### load _file_
Retrieves the contents of a text file. A blank file is provided if it does not exist.

Files in the trash must be restored before they can be loaded.

### store _file_
Sets or updates the contents of a file. The file is created if it does not exist.

_Storing to files is automatically handled in the editor. This command is for the API.
Running it in the editor will have the equivalent effect of making a copy._

## Trash Bin

### trash _file_
Moves a file to the trash bin.

### delete _file_
Deletes a file from the trash bin. Once deletion occurs, the file can no longer be restored.

### restore _file_
Takes a file out of the trash bin and makes it usable again.

## Misc.

### help
Outputs the help information.

"""