from flask import Flask, request, jsonify, send_file
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("medium")  

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
TRANSCRIPTION_FILE = os.path.join(UPLOAD_FOLDER, "transcription.txt")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        result = model.transcribe(filepath)
        transcription_text = result["text"]

        with open(TRANSCRIPTION_FILE, "w") as f:
            f.write(transcription_text)

        os.remove(filepath)  # Cleanup after transcription

        return jsonify({"transcription": transcription_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download_transcription", methods=["GET"])
def download_transcription():
    try:
        return send_file(TRANSCRIPTION_FILE, as_attachment=True, download_name="transcription.txt")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
