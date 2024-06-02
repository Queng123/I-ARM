"""IHM"""

import logging

import streamlit as st
from dotenv import load_dotenv
from audiorecorder import audiorecorder

from prompt import ask_question
from prompt import sentiment_analysis
from prompt import categorize_urgency
from prompt import summarize_call_informations

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
st.set_page_config(
     page_title='🚑Pimpon🚨',
     layout="wide",
     initial_sidebar_state="expanded",
)

if st.sidebar.button('Nouvelle conversation'):
    st.session_state.clear()

intro = "Bonjour, ici le Samu, Je suis un assistant IA et je suis là pour vous aider. Est-ce une urgence vitale ?"
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

            concat_discussions = ""
            for message in st.session_state.messages:
                concat_discussions += message["content"] + "; \n"

            sentiment = sentiment_analysis(concat_discussions)
            st.session_state.sentiment_history.append(sentiment)

            urgency = categorize_urgency(concat_discussions)
            response, sources = ask_question(prompt, urgency,concat_discussions)
            summary_of_information = summarize_call_informations(concat_discussions)

            st.markdown("**Ma réponse :**")
            st.write(response)
            parler(response)

            st.sidebar.success(f"{summary_of_information}")
            st.sidebar.info(f"Urgence détectée: {urgency}")
            st.sidebar.info(f"Sentiment détecté: {sentiment}")

            with st.expander("📚 Documents utilisés"):
                unique_sources = set()
                for source in sources:
                    unique_sources.add((source.metadata['source'], source.metadata['page']))

                for source in unique_sources:
                    st.markdown(f"* Doc: {source[0]}, Page: {source[1]}")
    message = {"role": "assistant", "content": response, "sources": sources}
    st.session_state.messages.append(message)
