"""
Prompter
========

Module permettant de poser les questions
"""

import logging
import os

from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Charge les variables d'environnement
load_dotenv()

# Configure le logger
logging.basicConfig(format='%(levelname)s: %(message)s',
                    encoding='utf-8', level=logging.INFO)

# Constantes de l'application
DATABASE_DIR = os.environ.get("DATABASE_DIR", "./database")
EMBEDDINGS_MODEL = os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002")

# Base de données vectorielle
DB = Chroma(embedding_function=OpenAIEmbeddings(model=EMBEDDINGS_MODEL),
            persist_directory=DATABASE_DIR)


if __name__ == "__main__":
    # print(DB.get())
    search = input("Search input: ")
    # Here we just print the 5 top results
    documents = DB.as_retriever(search_type="similarity", search_kwargs={
        'k': 5, 'fetch_k': 50
    }).get_relevant_documents(search)

    for doc in documents:
        print(f"Doc: {doc.metadata['source']}, Page: {doc.metadata['page']}")
