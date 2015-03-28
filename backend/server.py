#!flask/bin/python
from flask import Flask, request, jsonify
from flask_cors import CORS
import markdown
import storage

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

    if "text" in content:
        storage.update(file_name, content["text"])
        rendered_text = markdown.markdown(content["text"], output_format="html5")
        return jsonify(html=rendered_text)
    else:
        initial_text = storage.get(file_name)
        rendered_text = markdown.markdown(initial_text, output_format="html5")
        return jsonify(text=initial_text, html=rendered_text)


if __name__ == '__main__':
    app.run(debug=True)