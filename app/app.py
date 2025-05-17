from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, jsonify
import os

app = Flask(__name__)
UPLOAD_DIR = "/mnt/file-server"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            save_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
            uploaded_file.save(save_path)
            message = f"Uploaded: {uploaded_file.filename}"
    
    try:
        files = os.listdir(UPLOAD_DIR)
    except Exception as e:
        files = [f"Error: {e}"]

    html = """
    <!doctype html>
    <title>File Manager</title>
    <h1>Files in FileShare</h1>
    {% if message %}
    <p><strong>{{ message }}</strong></p>
    {% endif %}
    <ul>
      {% for file in files %}
        <li>
          {{ file }} |
          <a href="{{ url_for('download_file', filename=file) }}">Download</a>
        </li>
      {% endfor %}
    </ul>

    <h2>Upload New File</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
    return render_template_string(html, files=files, message=message)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify(status="OK"), 200

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
