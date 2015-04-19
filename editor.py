#!flask/bin/python
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import html
import markdown
import backend.files as files
import backend.help as help

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
auth_key = "3ul4VME1iusE8f5t4C3Fx7m39xOmJ49q"

def validate_auth_key(content):
    """
    Indicates whether a session is authenticated.
    :param content: The original request from the user.
    :return: A boolean indicating success and an optional message explaining the reason for a failure.
    """

    try:
        user_supplied_key = content["auth"]
    except KeyError:
        return False, "Authorization Key Missing"

    if user_supplied_key == auth_key:
        return True, ""
    else:
        return False, "Unauthorized Request"


@app.route('/editor/')
def serve_frontend_default():
    return send_from_directory('frontend/', "index.htm")


@app.route('/editor/<path:path>')
def serve_frontend(path):
    return send_from_directory('frontend/', path)


@app.route('/api', methods=['POST'])
def text():
    """
    Either updates or retrieves a text file, depending on the query.
    :param file_parameter:The text file to update/get.
    :return: The rendered text, as HTML.
    """

    content = request.get_json()

    authorized, reason = validate_auth_key(content)
    if not authorized:
        return jsonify(error=reason)

    action = content["action"] if "action" in content else "get"
    file_name = content["file"] if "file" in content else False
    input_text = content["text"] if "text" in content else ""
    mode = content["mode"] if "mode" in content else ""

    if action == "help":
        rendered_text = markdown.markdown(help.help, output_format="html5")
        return jsonify(html=rendered_text)

    elif action == "load" and file_name:
        initial_text = files.get(file_name)
        rendered_text = markdown.markdown(initial_text, output_format="html5")
        safe_file_name = html.escape(file_name)
        return jsonify(text=initial_text, html=rendered_text, info=str("Loaded \"%s\"" % safe_file_name))

    elif action == "store" and file_name:
        files.set(file_name, input_text)
        rendered_text = markdown.markdown(input_text, output_format="html5")
        return jsonify(html=rendered_text)

    elif action == "list":
        markdown_output = ""

        if ( mode == "trash" ):
            markdown_output = "# Trash Bin\n"
            markdown_output += str().join(["* " + single_file + "\n" for single_file in files.list_trash()])
        else:
            markdown_output = "# Available Files\n"
            markdown_output += str().join(["* " + single_file + "\n" for single_file in files.list()])

        rendered_text = markdown.markdown(markdown_output, output_format="html5")
        return jsonify(html=rendered_text)

    elif action == "trash" and file_name:
        success = files.trash(file_name)
        return jsonify(info="File Trashed") if success else jsonify(error="File Could Not Be Trashed")

    elif action == "restore" and file_name:
        success = files.restore(file_name)
        return jsonify(info="File Restored") if success else jsonify(error="File Could Not Be Restored")

    elif action == "delete" and file_name:
        success = files.delete(file_name)
        return jsonify(info="Trashed File Deleted") if success else jsonify(error="Could Not Delete Trashed File")

    elif action == "export":
        markdown_text = files.get(file_name)

        if mode == "html":
            return jsonify(name="exported-file.html", exported=markdown.markdown(markdown_text, output_format="html5"))

        else:
            return jsonify(name="exported-file.md", exported=markdown_text)

    else:
        return jsonify(error="Unknown action")


if __name__ == '__main__':
    app.run(debug=True)