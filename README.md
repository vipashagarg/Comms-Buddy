# Comms-Buddy

Comms-Buddy is an AI-powered chatbot built using Flask. It provides language feedback and pronunciation guidance through text, audio, and file inputs. The bot is enhanced with various NLP tools and speech recognition features to assist users with their communication skills.

## Features
- **Text Feedback**: Get language and grammar corrections for text inputs.
- **Audio Feedback**: Transcribe and analyze audio for pronunciation feedback.
- **File Processing**: Extract and analyze text from uploaded files (.txt, .pdf, .doc, etc.).
- **Pronunciation Guidance**: Offers audio feedback to help improve pronunciation.

## Project Structure
- `App.py`: Main Flask application, handles routes, and processes inputs.
- `Chatbot.py`: Contains core functions for text, audio, and file processing, grammar correction, and pronunciation checks.
- `templates/index.html`: Frontend interface for interacting with the chatbot.

## Getting Started

### Prerequisites
- Python 3.6+
- Recommended to use a virtual environment for package management

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/comms-buddy.git
   cd comms-buddy
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Folders**
   - Ensure that an `uploads/` folder is created in the project root for file uploads. This folder will store temporary audio and file uploads processed by the app.

### Running the Application

1. **Start the Flask Server**
   ```bash
   python App.py
   ```

2. **Access the Chatbot Interface**
   - Open your browser and go to `http://127.0.0.1:5000` to start using the chatbot.

### Usage

1. **Text Input**: Enter text in the text area and submit for language feedback.
2. **Audio Input**: Upload an audio file (.mp3, .wav, etc.) to receive transcription and pronunciation feedback.
3. **File Upload**: Upload a text file (.txt, .pdf, etc.) for grammar analysis and correction.
4. **Feedback**: The bot provides real-time feedback and, if requested, audio guidance to improve pronunciation.

## Dependencies

The project relies on several libraries for NLP, audio processing, and speech recognition:
- **Flask**: Web framework for serving the chatbot interface
- **Transformers**: NLP model for grammar correction
- **Textract**: Text extraction from files
- **SpeechRecognition**: Audio-to-text conversion
- **gTTS**: Text-to-speech for audio feedback
- **Language Tool**: Grammar checking and correction
- **Pydub**: Audio processing library
- **Pronouncing**: For identifying word pronunciation issues

See `requirements.txt` for specific versions.

## Contributing
1. **Fork the Repository**
2. **Create a new branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

## License
This project is licensed under the MIT License.

## Contact
For questions or collaboration, reach out to Vipasha Garg (mailto:gargvipasha@gmail.com).
