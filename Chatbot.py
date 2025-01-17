from io import BytesIO
import speech_recognition as sr
from transformers import pipeline
import pronouncing
import language_tool_python
from gtts import gTTS
import os
import sys
import tempfile
from pydub import AudioSegment
import random
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the grammar model and language tool
grammar_model = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")
language_tool = language_tool_python.LanguageTool('en-US')

os.environ["PATH"] += os.pathsep + os.path.join(sys.prefix, "Scripts")

def convert_audio_to_wav(file):
    try:
        audio = AudioSegment.from_file(file)
        wav_file = BytesIO()
        audio.export(wav_file, format="wav")
        wav_file.seek(0)
        return wav_file
    except Exception as e:
        logging.error(f"Error converting audio: {str(e)}")
        return None

def speech_to_text(file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Audio not clear"
    except sr.RequestError:
        return "Error with speech recognition service"
    except Exception as e:
        logging.error(f"Error in speech_to_text: {str(e)}")
        return f"Error processing audio: {str(e)}"

def correct_grammar(text):
    corrected_text = grammar_model(text)[0]['generated_text']
    return corrected_text

def provide_detailed_feedback(text):
    matches = language_tool.check(text)
    corrections = language_tool.correct(text)
    feedback = []
    for match in matches:
        feedback.append({
            'rule': match.ruleId,
            'message': match.message,
            'incorrect': match.context,
            'suggestions': match.replacements,
            'correct_statement': match.replacements[0] if match.replacements else ''
        })
    return corrections, feedback

def check_pronunciation(text):
    words = text.split()
    incorrect_words = [word for word in words if not pronouncing.phones_for_word(word)]
    return incorrect_words

def generate_pronunciation_audio(text, pronunciation_issues):
    feedback_text = f"Here is your corrected content: {text}. "
    feedback_text += "Please pay attention to the pronunciation of these words: " + ", ".join(pronunciation_issues) if pronunciation_issues else "Your pronunciation was excellent!"
    tts = gTTS(feedback_text)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        tts.save(temp_file.name)
        return temp_file.name

def get_greeting():
    greetings = [
        "Hello! How can I assist you today?",
        "Hi there! Welcome to the chatbot. How may I help you?",
        "Greetings! I'm here to help. What would you like to talk about?",
        "Welcome! I'm your friendly chatbot assistant. What can I do for you?",
        "Hey there! It's great to see you. How can I be of service today?"
    ]
    return random.choice(greetings)

def process_text_input(input_text, is_feedback_request=False):
    if is_feedback_request:
        corrected_text = correct_grammar(input_text)
        final_text, detailed_feedback = provide_detailed_feedback(corrected_text)
        pronunciation_issues = check_pronunciation(corrected_text)
        return input_text, final_text, detailed_feedback, pronunciation_issues
    else:
        return input_text, handle_conversation(input_text), [], []

def process_audio_input(audio_file, is_feedback_request=False):
    transcribed_text = speech_to_text(audio_file)
    if transcribed_text.startswith("Error:"):
        return transcribed_text, transcribed_text, [], []
    if is_feedback_request:
        corrected_text = correct_grammar(transcribed_text)
        final_text, detailed_feedback = provide_detailed_feedback(corrected_text)
        pronunciation_issues = check_pronunciation(corrected_text)
        return transcribed_text, final_text, detailed_feedback, pronunciation_issues
    else:
        return transcribed_text, handle_conversation(transcribed_text), [], []

def process_file_input(file_content, is_feedback_request=False):
    if is_feedback_request:
        corrected_text = correct_grammar(file_content)
        final_text, detailed_feedback = provide_detailed_feedback(corrected_text)
        pronunciation_issues = check_pronunciation(corrected_text)
        return file_content, final_text, detailed_feedback, pronunciation_issues
    else:
        return file_content, handle_conversation(file_content), [], []

def handle_conversation(input_text):
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(greeting in input_text.lower() for greeting in greetings):
        return random.choice([
            "Hello! How can I assist you today?",
            "Hi there! What can I help you with?",
            "Greetings! What would you like to talk about?",
            "Hey! How can I be of service?"
        ])
    return "I'm here to help. If you'd like feedback on your language, please start your message with 'Feedback:'"
