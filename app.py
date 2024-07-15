"""
pip install flask
"""

from flask import Flask, request, jsonify, render_template, Response
from transcribe import extract_text
from tts import get_tts_audio_bytes

app = Flask(__name__)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    video_url = request.data.get("video_url", "")
    if video_url.strip() == "":
        return jsonify({"error": "no url provided"})
    data = extract_text(video_url)
    return jsonify({"data": data})


@app.route('/tts', methods=['POST'])
def tts():
    segment = request.data.get("segment", {})
    for key in ["text", "start", "end"]:
        if key not in segment:
            return jsonify({"error": "wrong format"})
    return get_tts_audio_bytes(segment)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
