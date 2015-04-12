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


@app.route('/api/text/<file_name>', methods=['POST'])
def text(file_name):
    """
    Either updates or retrieves a text file, depending on the query.
    :param file_name:The text file to update/get.
    :return: The rendered text, as HTML.
    """

    content = request.get_json()

    authorized, reason = validate_auth_key(content)
    if not authorized:
        return jsonify(error=reason)

    input_text = content["text"] if "text" in content else ""
    action = content["action"] if "action" in content else "get"

    if action == "get":
        initial_text = files.get(file_name)
        rendered_text = markdown.markdown(initial_text, output_format="html5")
        return jsonify(text=initial_text, html=rendered_text)

    elif action == "set":
        files.update(file_name, input_text)
        rendered_text = markdown.markdown(input_text, output_format="html5")
        return jsonify(html=rendered_text)

    elif action == "list":
        file_names_in_markdown = str().join(["* " + file_name + "\n" for file_name in files.list()])
        markdown_output = "# Available Files\n" + file_names_in_markdown
        rendered_text = markdown.markdown(markdown_output, output_format="html5")
        return jsonify(html=rendered_text)

    else:
        return jsonify(error="Unknown action")


if __name__ == '__main__':
    app.run(debug=True)