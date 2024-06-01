"""IHM"""

import logging

import streamlit as st
from dotenv import load_dotenv
from audiorecorder import audiorecorder

from prompt import ask_question
from prompt import sentiment_analysis
from prompt import categorize_urgency

from gtts import gTTS
import pygame
from datetime import datetime

# Charge les variables d'environnement
load_dotenv()
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

# Configure le logger
logging.basicConfig(format='%(levelname)s: %(message)s',
                    encoding='utf-8', level=logging.INFO)

# Configuration de l'application
st.set_page_config(layout="wide", page_title="POC")

# Titre de l'application
st.title("👨‍💼👩‍💼 ARM 💬")
st.divider()


audio = audiorecorder("Click to record", "Click to stop recording",pause_prompt="", show_visualizer=True, key=None)

if len(audio) > 0:
    st.audio(audio.export().read())

    audio.export("audio.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

# Charger l'audio
# r = sr.Recognizer()
# with sr.AudioFile('audio.wav') as source:
#     audio_data = r.record(source)
#    text = r.recognize_google(audio_data, language='fr-FR')  # Utilisez 'en-US' pour l'anglais
#   st.write(text)

if st.button('Clear cache'):
    st.session_state.clear()

intro = "Bonjour, ici le Samu, Je suis un chatbot et je suis là pour vous aider. Est-ce une urgence vitale ?"
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant",
         "content": intro}]
    parler(intro)

if "sentiment_history" not in st.session_state.keys():
    st.session_state.sentiment_history = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="images/" + message['role'] + ".png"):
        if message.get("sources"):
            st.markdown("**Ma réponse :**")
            st.write(message["content"])

            with st.expander("📚 Documents utilisés"):
                unique_sources = set()

                for source in message["sources"]:
                    unique_sources.add((source.metadata['source'], source.metadata['page']))

                for source in unique_sources:
                    st.markdown(f"* Doc: {source[0]}, Page: {source[1]}")
        else:
            st.write(message["content"])

# Display the prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="images/user.png"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar="images/assistant.png"):
        with st.spinner("Réponse en cours de génération..."):
            sentiment = sentiment_analysis(prompt)
            st.session_state.sentiment_history.append(sentiment)
            urgency = categorize_urgency(prompt)
            response, sources = ask_question(prompt, urgency)
            st.markdown("**Ma réponse :**")
            st.write(response)
            parler(response)
            st.info(f"Sentiment détecté: {sentiment}")
            st.info(f"Urgence détectée: {urgency}")
            with st.expander("📚 Documents utilisés"):
                unique_sources = set()
                for source in sources:
                    unique_sources.add((source.metadata['source'], source.metadata['page']))

                for source in unique_sources:
                    st.markdown(f"* Doc: {source[0]}, Page: {source[1]}")
    message = {"role": "assistant", "content": response, "sources": sources}
    st.session_state.messages.append(message)
