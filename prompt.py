import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.vectorstores import Chroma
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import constants

# Import conditionnel selon si on est sur les API officielles d'OpenAI ou sur Azure.
if constants.OPENAI_API_TYPE == "azure":
    from langchain.chat_models import AzureChatOpenAI as Chat
else:
    from langchain.chat_models import ChatOpenAI as Chat

# Configure le logger
logging.basicConfig(format='%(levelname)s: %(message)s',
                    encoding='utf-8', level=logging.INFO)

# template du prompt Système
SYSTEM_PROMPT = """
Tu es un ARM. Assistant médical de régulation. Ton rôle est de répondre au mieux aux urgences des demandeurs.
Tu ne doit JAMAIS dire « mais il est important de noter que » ou « en tant que modèle de langage d'IA ».

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

# Liste pour stocker l'historique des messages
message_history = []

def format_context(results):
    """Formate les résultats de la recherche pour les inclure dans le contexte."""
    context = ""
    for result in results:
        context += f"{result.page_content}\n"
    return context

def ask_question(question):
    """Poser une question au modèle."""

    # Cherche des chunks de textes similaires à la question
    results = DB.as_retriever(search_type="similarity", search_kwargs={'k': 10}).get_relevant_documents(query=question)

    logging.debug("Sources: %s", results)

    # Formate le contexte à partir des résultats
    context = format_context(results)

    # Constitue la séquence de chat avec le conditionnement du bot et la question de l'utilisateur
    system_message_prompt = SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT)
    human_message_prompt = HumanMessagePromptTemplate.from_template("QUESTION: {question}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Ajouter l'historique des messages
    messages = message_history + chat_prompt.format_prompt(context=context, question=question).to_messages()

    # Log messages pour débogage
    logging.debug("Messages: %s", messages)

    # Pose la question au LLM
    response = CHAT(messages).content

    # Ajouter la question et la réponse à l'historique
    message_history.extend(messages)
    message_history.append(AIMessage(content=response))

    return response, results

if __name__ == "__main__":
    print("""
👨‍💼👩‍💼 ARM 💬

Posez simplement votre question:
""")
    print("----------------------------------------------------")
    print("💬 Votre question: ")

    while True:
        question = input()
        if question.lower() in ["exit", "quit"]:
            break

        answer, sources = ask_question(question)

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
        print("Posez une autre question ou tapez 'exit' pour quitter.")
