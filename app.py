# Import necessary libraries
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
from pygame import mixer
from pydub.playback import play
from flask import Flask, request, render_template, make_response, jsonify
from pydub import AudioSegment  # Import the AudioSegment class
from gtts import gTTS
from googletrans import Translator
from bs4 import BeautifulSoup
import time
import random


# Use a dummy audio segment
dummy_audio = AudioSegment.silent(duration=1000)  # Adjust duration as needed
pygame.mixer.Sound(dummy_audio).play()


# Initialize Pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)


app = Flask(__name__)


dummy_audio = AudioSegment.silent(duration=1000)

play(dummy_audio)


try:
    import pygame
except ImportError:
    pygame = None



try:
    import pygame
except ImportError:
    pygame = None

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

mixer.init()
playing_music = False  # Variable to track whether music is currently playing

def play_background_music():
    try:
        music_path = os.path.join("static", "audio", "music6.mp3")
        mixer.music.load(music_path)
        mixer.music.play(-1)  # -1 indicates loop indefinitely
    except Exception as e:
        print(f"Error playing background music: {e}")

def stop_music():
    mixer.music.stop()

@app.route('/')
def index():
    return render_template('index.html', languages=languages, alert_message="")

@app.route('/play_background_music')
def play_background_music_route():
    global playing_music
    if not playing_music:
        playing_music = True
        play_background_music()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'already playing'})

@app.route('/stop_music')
def stop_music_route():
    global playing_music
    playing_music = False
    stop_music()
    return jsonify({'status': 'success'})

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

    # Call this function to play background music after translation
    play_background_music_route()

    response = make_response(render_template('result.html', input_text=input_text,
                                             translated_text=translated_text, audio_file=audio_file,
                                             random_number=random_number))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response

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

if __name__ == "__main__":
    app.run(debug=True)
