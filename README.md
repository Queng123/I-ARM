# I-ARM ( Medi call) 


## Installation

Pré-requis :

* Python 3.10 minimum
* Pip installé

Installer les dépendances du projet :

```sh
pip install -r requirements.txt
```

## Ingestion des documents

Déposer des PDFs dans le répertoire `documents` à la racine de ce repository puis lancer la
commande suivante :

```sh
python ingest.py
```

## Interrogation avec le modèle

Lancer la commande suivante :

```sh
python prompt.py
```

Après chargement de la base de données, vous devriez pouvoir lancer une question.

## Chatter avec les documents

Vous pouvez aussi lancer l'IHM pour converser avec les documents :

```sh
streamlit run chat.py
```

## Image Docker

Disponible sous forme d'image Docker.

Construire l'image :

```sh
docker build -t pimpon .
```

Générer la base de données :

```sh
docker run --entrypoint=python3 -v $(pwd)/database:/app/database -v $(pwd)/documents:/app/documents pimpon ingest.py
```

Exécuter une instance Web :

```sh
docker run -p 8080:8501 -v $(pwd)/database:/app/database -v $(pwd)/documents:/app/documents pimpon
```

## Upgrade to python 3.12

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12
pip3.12 install -r requirements.txt
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python3.12 ingest.py 
streamlit run chat.py
