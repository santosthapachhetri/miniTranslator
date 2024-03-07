# Import necessary libraries
import os
from flask import Flask, request, render_template, make_response, jsonify
from gtts import gTTS
from googletrans import Translator
from bs4 import BeautifulSoup
import time
import random

app = Flask(__name__)

languages = {
    'en': 'English',
    'es': 'Spanish',
    'ne': 'Nepali',
    'hi': 'Hindi',
    'ur': 'Pakistani',
    'ja': 'Japanese',
    'ko': 'Korean',
}

translator = Translator()

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_directory = 'static/audio'
    timestamp = str(int(time.time()))
    random_number = random.randint(1, 1000)
    audio_path = os.path.join(audio_directory, f'output_{timestamp}_{random_number}.mp3')
    os.makedirs(audio_directory, exist_ok=True)
    tts.save(audio_path)
    return audio_path, random_number

def translate_webpage(url, target_lang):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        body_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        translated_text = translator.translate(body_text, dest=target_lang).text
    except requests.RequestException as e:
        print(f"Request error: {e}")
        translated_text = "Request error"

    return translated_text

@app.route('/')
def index():
    return render_template('index.html', languages=languages, alert_message="")

@app.route('/translate', methods=['POST'])
def translate_text_route():
    source_lang = request.form.get('source_lang')
    target_lang = request.form.get('target_lang')
    input_text = request.form.get('input_text')

    if not input_text.strip():
        return render_template('index.html', languages=languages, alert_message="Please speak or write something to translate.")

    if input_text.startswith("http://") or input_text.startswith("https://"):
        translated_text = translate_webpage(input_text, target_lang)
    else:
        translated_text = translator.translate(input_text, dest=target_lang).text

    audio_file, random_number = text_to_speech(translated_text, target_lang)

    response = make_response(render_template('result.html', input_text=input_text,
                                             translated_text=translated_text, audio_file=audio_file,
                                             random_number=random_number))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response

if __name__ == "__main__":
    app.run(debug=True)
