import io
from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # reject uploads larger than 1 MB

MAX_TEXT_CHARS = 5000


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Accept text (form field or .txt file) and return an MP3 audio stream."""
    text = ''

    uploaded = request.files.get('file')
    if uploaded and uploaded.filename:
        if not uploaded.filename.lower().endswith('.txt'):
            return jsonify({'error': 'Only .txt files are supported.'}), 400
        try:
            text = uploaded.read().decode('ascii')
        except UnicodeDecodeError:
            return jsonify({'error': 'File must contain plain ASCII text.'}), 400
    else:
        text = request.form.get('text', '').strip()

    if not text:
        return jsonify({'error': 'No text provided.'}), 400

    if len(text) > MAX_TEXT_CHARS:
        return jsonify({'error': f'Text exceeds the {MAX_TEXT_CHARS}-character limit.'}), 400

    # Convert to speech entirely in memory — no temp files written to disk
    audio_buffer = io.BytesIO()
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return send_file(audio_buffer, mimetype='audio/mpeg', download_name='speech.mp3')


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
