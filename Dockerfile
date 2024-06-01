FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt -yqq update                     && \
    # nécessaire pour chromadb
    apt -yqq install build-essential    && \
    pip install -r requirements.txt

VOLUME ["/app/database", "/app/documents"]
EXPOSE 8501
CMD ["streamlit", "run", "chat.py"]
