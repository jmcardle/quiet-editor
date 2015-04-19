#!flask/bin/python
from flask import Flask, request, jsonify
from flask_cors import CORS
import markdown
import files

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


@app.route('/api/text/<file_parameter>', methods=['POST'])
def text(file_parameter):
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
    print("Action \"%s\" on file \"%s\"" % (action, file_parameter))

    if action == "get":
        initial_text = files.get(file_parameter)
        rendered_text = markdown.markdown(initial_text, output_format="html5")
        return jsonify(text=initial_text, html=rendered_text, info=str("Loaded \"%s\"" % file_parameter))

    elif action == "set":
        input_text = content["text"] if "text" in content else ""
        files.update(file_parameter, input_text)
        rendered_text = markdown.markdown(input_text, output_format="html5")
        return jsonify(html=rendered_text)

    elif action == "list":
        markdown_output = ""

        if ( file_parameter == "trash" ):
            markdown_output = "# Trash Bin\n"
            markdown_output += str().join(["* " + single_file + "\n" for single_file in files.list_trash()])
        else:
            markdown_output = "# Available Files\n"
            markdown_output += str().join(["* " + single_file + "\n" for single_file in files.list()])

        rendered_text = markdown.markdown(markdown_output, output_format="html5")
        return jsonify(html=rendered_text)

    elif action == "trash":
        success = files.trash(file_parameter)
        return jsonify(info="File Deleted") if success else jsonify(error="File Could Not Be Deleted")

    elif action == "restore":
        success = files.restore(file_parameter)
        return jsonify(info="File Restored") if success else jsonify(error="File Could Not Be Restored")

    else:
        return jsonify(error="Unknown action")


if __name__ == '__main__':
    app.run(debug=True)