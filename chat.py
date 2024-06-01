"""IHM"""

import logging

import streamlit as st
from dotenv import load_dotenv

from prompt import ask_question

# Charge les variables d'environnement
load_dotenv()

# Configure le logger
logging.basicConfig(format='%(levelname)s: %(message)s',
                    encoding='utf-8', level=logging.INFO)

# Configuration de l'application
st.set_page_config(layout="wide", page_title="POC")

# Titre de l'application
st.title("👨‍💼👩‍💼 ARM 💬")
st.divider()
st.markdown("""
            
* Posez vos questions en **français** pour interroger les documents en français
* Posez vos questions en **anglais** pour interroger les documents en anglais
""")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Posez-moi des questions !"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="images/" + message['role'] + ".png"):
        if message.get("sources"):
            st.markdown("**Ma réponse :**")
            st.write(message["content"])

            st.markdown("**📚 Documents utilisés :**")
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
            response, sources = ask_question(prompt)
            st.markdown("**Ma réponse :**")
            st.write(response)
            st.markdown("**📚 Documents utilisés :**")
            unique_sources = set()
            for source in sources:
                unique_sources.add((source.metadata['source'], source.metadata['page']))

            for source in unique_sources:
                st.markdown(f"* Doc: {source[0]}, Page: {source[1]}")
    message = {"role": "assistant", "content": response, "sources": sources}
    st.session_state.messages.append(message)
