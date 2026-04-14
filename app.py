from flask import Flask, render_template, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Folder to store videos
UPLOAD_FOLDER = "videos"

# Ensure folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Home route
@app.route('/')
def index():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        files = sorted(files, reverse=True)  # latest first
    except:
        files = []
    return render_template('index.html', videos=files)


# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return "No file uploaded", 400

    video = request.files['video']

    if video.filename == '':
        return "Empty file", 400

    # Unique filename using timestamp
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    video.save(filepath)

    return "Uploaded successfully"


# Serve videos
@app.route('/videos/<filename>')
def get_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# Run app (Render-compatible)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
