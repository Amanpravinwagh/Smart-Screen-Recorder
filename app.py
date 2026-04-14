from flask import Flask, render_template, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "videos"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', videos=files)


@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".webm"
    path = os.path.join(UPLOAD_FOLDER, filename)
    
    video.save(path)
    
    return "Uploaded"


@app.route('/videos/<filename>')
def get_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)