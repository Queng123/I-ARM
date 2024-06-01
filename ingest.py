"""
Ingestion des documents
=======================

Etapes à réaliser:

1. Charger les documents PDF avec PyPDF
2. Splitter les textes
3. Calculer les embeddings
4. Les stocker dans une base vecteur
"""

import logging

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import constants

# Configure le logger
logging.basicConfig(format='%(levelname)s: %(message)s',
                    encoding='utf-8', level=logging.INFO)

# Base de données vectorielle
DB = Chroma(embedding_function=OpenAIEmbeddings(model=constants.EMBEDDINGS_MODEL),
            persist_directory=constants.DATABASE_DIR)


def ingest(directory):
    """Fonction principale d'ingestion des documents"""
    # Charge les documents PDF depuis un répertoire
    documents = read_pdfs(directory)
    # Calcule les embeddings et les stocke dans une base vectorielle
    store_embeddings(documents)
    logging.info("Nombre de documents chargés: %i", len(documents))


def store_embeddings(documents):
    """Stocke les embeddings à partir de text-embedding-ada-002 par défaut"""
    DB.add_documents(documents=documents)


def read_pdfs(directory):
    """Lit les documents PDF depuis un répertoire"""
    logging.info("Chargement des fichiers depuis le répertoire %s", directory)
    return PyPDFDirectoryLoader(directory).load_and_split()


def read_words(directory):
    """Lit des documents Words depuis un répertoire"""
    raise NotImplementedError


def read_ppts(directory):
    """Lit des documents Powerpoints depuis un répertoire"""
    raise NotImplementedError


if __name__ == "__main__":
    ingest(directory=constants.DOCUMENTS_DIR)
