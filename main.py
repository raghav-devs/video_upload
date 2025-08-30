from flask import Flask, request
from video_utils.upload import upload_video
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_upload():
    file_path = request.json.get("file_path") or os.environ.get("VIDEO_FILE")
    if not file_path:
        return "No file path provided", 400

    upload_video(file_path)
    return "Upload complete", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
