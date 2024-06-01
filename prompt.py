"""
Prompt "Pimpon"
=======================

Module permettant de poser les questions.

Le fonctionnement est le suivant :
1. Chargement de la base vectorielle locale dans le dossier adéquat
2. Recherche par similarité des documents d'intérêt
2. Constitution du template du prompt avec le contexte des docs d'intérêt
3. Interrogation avec le modèle d'OpenAI à 16k tokens
4. Affichage de la réponse et des sources
"""

import logging

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.vectorstores import Chroma

import constants

# Import conditionnel selon si on est sur les API officielles d'OpenAI
# ou sur Azure.
if constants.OPENAI_API_TYPE == "azure":
    from langchain.chat_models import AzureChatOpenAI as Chat
else:
    from langchain.chat_models import ChatOpenAI as Chat

# Configure le logger
logging.basicConfig(format='%(levelname)s: %(message)s',
                    encoding='utf-8', level=logging.INFO)

# template du prompt Système
SYSTEM_PROMPT = """
Tu es un ARM et à compléter
===========
CONTEXTE:
{context}
===========
"""

CHAT = Chat(model_name=constants.MODEL_NAME, temperature=constants.TEMPERATURE)
DB = Chroma(persist_directory=constants.DATABASE_DIR,
            embedding_function=OpenAIEmbeddings(
                deployment=constants.OPENAI_DEPLOYMENT_NAME,
                model=constants.EMBEDDINGS_MODEL,
                openai_organization=constants.OPENAI_ORGANIZATION,
                openai_api_base=constants.OPENAI_API_BASE,
                openai_api_version=constants.OPENAI_API_VERSION))


def ask_question(question):
    """Poser une question au modèle."""

    # Cherche de chunks de textes similaires à la question
    results = DB.as_retriever(search_type="similarity", search_kwargs={
        'k': 10
    }).get_relevant_documents(query=question)

    logging.debug("Sources: %s", results)

    # Constitue la séquence de chat avec le conditionnement du bot et la question
    # de l'utilisateur
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        SYSTEM_PROMPT)
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        "QUESTION: {question}")
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    messages = chat_prompt.format_prompt(
        context=results, question=question
    ).to_messages()

    # Pose la question au LLM
    response = CHAT(messages).content

    return response, results


if __name__ == "__main__":
    print("""
👨‍💼👩‍💼 ARM 💬

Posez simplement votre question:
""")
    print("----------------------------------------------------")
    print("💬 Votre question: ")

    answer, sources = ask_question(input())

    print("----------------------------------------------------")
    print("🤖 Réponse de l'expert: ")
    print(answer)
    print("----------------------------------------------------")
    print("📚 Documents utilisés: ")
    unique_sources = set()
    for source in sources:
        unique_sources.add((source.metadata['source'], source.metadata['page']))

    for source in unique_sources:
        print(f"- Document: {source[0]}, Page: {source[1]}")
    print("----------------------------------------------------")
