from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import textract
from chatbot import process_text_input, process_audio_input, process_file_input, generate_pronunciation_audio, get_greeting
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'rtf', 'mp3', 'wav', 'ogg', 'm4a'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_greeting', methods=['GET'])
def greeting():
    return jsonify({'greeting': get_greeting()})

@app.route('/process', methods=['POST'])
def process_input():
    input_type = request.form.get('input_type')
    is_feedback_request = request.form.get('is_feedback_request', 'false').lower() == 'true'
    app.logger.info(f"Processing input type: {input_type}, Feedback request: {is_feedback_request}")

    try:
        if input_type in ['text', 'mic']:
            input_text = request.form.get('text_input')
            if not input_text:
                return jsonify({'error': 'No text input provided'}), 400
            original_text, result, detailed_feedback, pronunciation_issues = process_text_input(input_text, is_feedback_request)

        elif input_type == 'audio':
            if 'audio_input' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            file = request.files['audio_input']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                app.logger.info(f"Saved audio file: {filepath}")
                original_text, result, detailed_feedback, pronunciation_issues = process_audio_input(filepath, is_feedback_request)
                os.remove(filepath)  # Clean up the uploaded file
            else:
                return jsonify({'error': 'Audio file type not allowed'}), 400

        elif input_type == 'file':
            if 'file_input' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            file = request.files['file_input']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                app.logger.info(f"Saved file: {filepath}")
                file_content = textract.process(filepath).decode('utf-8')
                original_text, result, detailed_feedback, pronunciation_issues = process_file_input(file_content, is_feedback_request)
                os.remove(filepath)  # Clean up the uploaded file
            else:
                return jsonify({'error': 'File type not allowed'}), 400

        else:
            return jsonify({'error': 'Invalid input type'}), 400

        audio_feedback_path = None
        if is_feedback_request:
            audio_feedback_path = generate_pronunciation_audio(result, pronunciation_issues)

        return jsonify({
            'original_text': original_text,
            'result': result,
            'feedback': detailed_feedback,
            'pronunciation_issues': pronunciation_issues,
            'audio_feedback_path': audio_feedback_path,
            'is_feedback_request': is_feedback_request
        })

    except Exception as e:
        app.logger.error(f"Error processing input: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/audio_feedback/<path:filename>')
def audio_feedback(filename):
    return send_file(filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
