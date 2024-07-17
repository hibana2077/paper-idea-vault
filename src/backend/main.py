from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.pydantic_v1 import BaseModel, Field
from contextlib import asynccontextmanager
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import selfarxiv
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
# embeddings = OllamaEmbeddings(base_url=ollama_server)

class Suggestion(BaseModel):

    topic: str = Field(description="The suggestion of a new paper topic from the related work")
    details: str = Field(description="The details of the suggestion")

class Suggestions(BaseModel):

    suggestions: list[Suggestion] = Field(description="The suggestions of new paper topics from the related work")

class RelatedWork(BaseModel):

    is_related_work: bool = Field(description="Whether the summary is related to the description")

class Keywords(BaseModel):

    keywords: list = Field(description="The keywords generated from the description")

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
def new_idea(data:dict):
    """
    A function that handles the new_idea endpoint.

    Args:
        title (str): The title of the idea.
        description (str): The description of the idea.
        tags (str): The tags of the idea.

    Returns:
        dict: A dictionary with the message "Idea created".
    """
    title = data["title"]
    description = data["description"]
    tags = data["tags"]
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

@app.post("/generate_keywords")
def generate_keywords(data:dict):
    """
    A function that handles the generate_keywords endpoint.

    Args:
        description (str): The description of the idea.
        api_key (str): The API key.

    Returns:
        dict: A dictionary with the keywords.
    """
    description = data["description"]
    api_key = data['api_key']
    chat = ChatGroq(
        temperature=0,
        model="gemma2-9b-it",
        groq_api_key=api_key # Optional if not set as an environment variable
    )
    structured_llm = chat.with_structured_output(Keywords)

    out_put = structured_llm.invoke(f"Generate keywords from the description: {description}")
    return out_put

@app.get("/idea/{idea_id}")
def get_idea(idea_id:int):
    """
    A function that handles the idea endpoint.

    Args:
        idea_id (int): The idea ID.

    Returns:
        dict: A dictionary with the idea.
    """
    return idea_db.hgetall(idea_id)

@app.post('/related_work')
def get_related_work(data:dict):
    """
    A function that handles the related_work endpoint.

    Args:
        keywords (list): The keywords.
        description (str): The description of your idea.
        api_key (str): The API key.

    Returns:
        dict: A dictionary with the related work.
    """
    keywords = data.get("keywords")
    description = data.get("description")
    api_key = data.get("api_key")

    related = []

    chat = ChatGroq(
        temperature=0,
        model="gemma2-9b-it",
        groq_api_key=api_key # Optional if not set as an environment variable
    )

    # make keywords into a string
    keywords_str = " ".join(keywords)

    # get related work
    related_works = []
    start_list = [0,10,20]
    for start in start_list:
        related_works.extend(selfarxiv.Search_paper(keywords_str,start=start))

    for related_work in related_works:
        structured_llm = chat.with_structured_output(RelatedWork)
        out_put = structured_llm.invoke(f"Is the summary related to the description: {description}, summary: {related_work['summary']}")
        print(f"Function name: get_related_work, out_put: {out_put}")
        if out_put.is_related_work:
            related.append(related_work)
    
    return {"related_work": related}

@app.post("/suggest_topic")
def suggest_topic(data:dict)->list[str]:
    """
    A function that handles the suggest_idea endpoint.

    Args:
        api_key (str): The API key.
        related_works (list): The related works.

    Returns:
        list[str]: A list of suggestions.
    """
    api_key = data["api_key"]
    related_works = data["related_works"]
    chat = ChatGroq(
        temperature=0,
        model="mixtral-8x7b-32768",
        groq_api_key=api_key # Optional if not set as an environment variable
    )

    related_works_str = "\n".join([f"{work['title']} {work['summary']}" for work in related_works])

    structured_llm = chat.with_structured_output(Suggestions)
    out_put = structured_llm.invoke(f"Generate a new paper topic based on the related works of a paper. Related works: {related_works_str}")
    return out_put

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8081) # In docker need to change to 0.0.0.0