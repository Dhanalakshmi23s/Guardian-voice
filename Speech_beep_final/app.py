from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import re
from gtts import gTTS
import os

app = Flask(__name__)

# Predefined list of bad words
bad_words = ["shit", "bastard", "fuck", "asshole","bastard","bitch","bloody",
"bollocks","brotherfucker","bugger","bullshit"]  # Add more bad words as needed

# Create output directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def beep_bad_words(text):
    for word in bad_words:
        if word in text:
            # Replace bad word with beeps
            text = re.sub(r'\b' + re.escape(word) + r'\b', "*BEEP*", text, flags=re.IGNORECASE)
    return text

def text_to_speech(text_with_beeps):
    tts = gTTS(text=text_with_beeps, lang='en', slow=False)
    tts.save(os.path.join(output_dir, "output.mp3"))

@app.route('/')
def index():
    return render_template('ind.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        text_with_beeps = beep_bad_words(text)
        text_to_speech("You said: " + text_with_beeps)
        return jsonify({"result": text_with_beeps})
    except sr.UnknownValueError:
        return jsonify({"result": "Could not understand audio."})
    except sr.RequestError as e:
        return jsonify({"result": "Could not request results; {0}".format(e)})

if __name__ == "__main__":
    app.run(debug=True)
