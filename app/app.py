from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, jsonify, flash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

UPLOAD_DIR = "/mnt/file-server"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            save_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
            uploaded_file.save(save_path)
            flash(f"Uploaded: {uploaded_file.filename}")
        return redirect(url_for('index'))  # ✅ Redirect to avoid resubmission
    
    try:
        files = os.listdir(UPLOAD_DIR)
    except Exception as e:
        files = [f"Error: {e}"]

    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FileShare</title>
        <style>
            /* Same modern premium style as before */
            body {
                margin: 0;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                background-color: #121212;
                color: #e0e0e0;
                padding: 40px;
            }
            h1, h2 {
                color: #f5f5f5;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                background-color: #1e1e1e;
                border: 1px solid #2e2e2e;
                padding: 16px;
                margin-bottom: 12px;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
            }
            a {
                color: #C0A36E;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            form {
                margin-top: 30px;
                background-color: #1e1e1e;
                padding: 24px;
                border-radius: 8px;
                border: 1px solid #2e2e2e;
            }
            input[type="submit"] {
                background-color: #C0A36E;
                color: #000;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #a68b5a;
            }
            .message {
                color: #C0A36E;
                margin-bottom: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>FileShare</h1>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="message">{{ messages[0] }}</div>
          {% endif %}
        {% endwith %}

        <ul>
            {% for file in files %}
                <li>
                    {{ file }}
                    <a href="{{ url_for('download_file', filename=file) }}">Download</a>
                </li>
            {% endfor %}
        </ul>

        <h2>Upload New File</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    """
    return render_template_string(html, files=files)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify(status="OK"), 200

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
