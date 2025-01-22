from flask import Flask, request, jsonify, send_file
from podcastfy.client import generate_podcast
from podcastfy.utils.logger import setup_logger

import os
import logging

logger = setup_logger(__name__)

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text')

    try:
        audio_file = generate_podcast(
            text=text,
        )
        logger.info(f"Podcast generated, file: {audio_file}")
        audio_path =  os.path.join('..', audio_file)
        #audio_path =  os.path.join('..', './data/audio/podcast_e476515de50d494c83edee15f7943fd8.mp3')

        return send_file(audio_path, as_attachment=True, mimetype='audio/mpeg')
    except Exception as e:
        logger.error(f'Error generating podcast: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
