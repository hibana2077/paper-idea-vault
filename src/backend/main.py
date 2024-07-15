from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from contextlib import asynccontextmanager
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import redis
import os
import time
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware

ollama_server = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
redis_server = os.getenv("REDIS_SERVER", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
HOST = os.getenv("HOST", "127.0.0.1")
embeddings = OllamaEmbeddings(base_url=ollama_server)

counter_db = redis.Redis(host=redis_server, port=redis_port, db=0) # string
user_rec_db = redis.Redis(host=redis_server, port=redis_port, db=1) # hash
idea_db = redis.Redis(host=redis_server, port=redis_port, db=2) # hash

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # pull model from ollama
    _ = requests.post(f"{ollama_server}/api/pull", json={"name": "nomic-embed-text"})
    _ = requests.post(f"{ollama_server}/api/pull", json={"name": "jina/jina-embeddings-v2-snall-en"})

@app.get("/")
def read_root():
    """
    A function that handles the root endpoint.

    Returns:
        dict: A dictionary with the message "Hello: World".
    """
    return {"Hello": "World"}

@app.post("/new_idea")
def new_idea(title: str, description: str, tags: str):
    """
    A function that handles the new_idea endpoint.

    Args:
        title (str): The title of the idea.
        description (str): The description of the idea.
        tags (str): The tags of the idea.

    Returns:
        dict: A dictionary with the message "Idea created".
    """
    idea_id = counter_db.incr("idea_counter")
    idea_db.hmset(idea_id, {"title": title, "description": description, "tags": tags})
    return {"status": "Idea created"}

@app.get("/ideas")
def get_ideas():
    """
    A function that handles the ideas endpoint.

    Returns:
        dict: A dictionary with the ideas.
    """
    ideas = {}
    for key in idea_db.keys():
        ideas[key] = idea_db.hgetall(key)
    return {"ideas": ideas}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8081) # In docker need to change to 0.0.0.0