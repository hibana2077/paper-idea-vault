'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-05-06 21:09:40
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-06-13 15:49:11
FilePath: \Digital-TA\src\backend\main.py
Description: Here is the main file for the FastAPI server.
'''
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
    _ = requests.post(f"{ollama_server}/api/pull", json={"name": "llama2"})
    _ = requests.post(f"{ollama_server}/api/pull", json={"name": "nomic-embed-text"})

@app.get("/")
def read_root():
    """
    A function that handles the root endpoint.

    Returns:
        dict: A dictionary with the message "Hello: World".
    """
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8081) # In docker need to change to 0.0.0.0