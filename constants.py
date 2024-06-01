"""Constantes applicatives"""

import os

from dotenv import load_dotenv

# Charge les fichiers .env
load_dotenv()

DATABASE_DIR = os.environ.get("DATABASE_DIR", "./database")
"""Répertoire de la base de données"""
DOCUMENTS_DIR = os.environ.get("DOCUMENTS_DIR", "./documents")
"""Répertoire des documents à charger"""
EMBEDDINGS_MODEL = os.environ.get("EMBEDDINGS_MODEL", "text-embedding-ada-002")
"""Modèle d'embeddings à utiliser"""
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo-16k")
"""Nom du modèle à utiliser"""

# Hyperparamètres
TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.5))
"""Température du modèle"""

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

OPENAI_ORGANIZATION = os.environ.get("OPENAI_ORGANIZATION")
"""Organization OpenAI (pour Azure)"""
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
"""Baseurl de l'API OpenAI"""
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION", "2020-11-07")
"""Version de l'API"""
OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE")
"""Type d'API OpenAI"""
OPENAI_DEPLOYMENT_NAME = os.environ.get("OPENAI_DEPLOYMENT_NAME", EMBEDDINGS_MODEL)
"""Nom du déploiement OpenAI (pour Azure)"""

# os.environ["HTTP_PROXY"] = "ntes.proxy.corp.sopra:8080"
# os.environ["HTTPS_PROXY"] = "ntes.proxy.corp.sopra:8080"
"""Configuration du proxy"""
