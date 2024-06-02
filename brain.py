from flask import Flask, request, jsonify
from prompt import ask_question, sentiment_analysis, categorize_urgency
from gtts import gTTS
import pygame
from datetime import datetime

app = Flask(__name__)
pygame.mixer.init()

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def parler(texte):
    nom_fichier = f"audio/response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    tts = gTTS(texte, lang='fr', slow=False)
    tts.save(nom_fichier)
    play_mp3(nom_fichier)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    sentiment = sentiment_analysis(question)
    urgency = categorize_urgency(question)
    response, sources = ask_question(question, urgency)
    parler(response)
    return jsonify({
        'response': response,
        'sentiment': sentiment,
        'urgency': urgency,
        'sources': [(source.metadata['source'], source.metadata['page']) for source in sources]
    })

if __name__ == '__main__':
    app.run(debug=True)
