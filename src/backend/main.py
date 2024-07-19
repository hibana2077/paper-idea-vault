from langchain_community.vectorstores.faiss import FAISS
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
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware

ollama_server = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
redis_server = os.getenv("REDIS_SERVER", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
HOST = os.getenv("HOST", "127.0.0.1")
# embeddings = OllamaEmbeddings(base_url=ollama_server)

class ExpMethod(BaseModel):
    exp_method: str = Field(description="Describes the specific procedures and techniques used in the experiment to achieve the objectives. This includes the experimental setup, the data collection methods, and the analytical techniques used.")

class ExpMerits(BaseModel):
    exp_merits: str = Field(description="Highlights the benefits and advantages of the experimental approach, including how it contributes to the field of study, its efficacy in addressing the research question, and its potential for broader impact.")

class Experiment(BaseModel):
    exp_objective: str = Field(description="Defines the primary goal or outcome the experiment seeks to achieve. It specifies what question the experiment aims to answer, which hypothesis it intends to test, or what effect it aims to measure.")
    exp_method: list[ExpMethod] = Field(description="list of the experimental methods")
    exp_merits: list[ExpMerits] = Field(description="list of the experimental merits")

class ExperimentSketch(BaseModel):
    experiments: list[Experiment] = Field(description="The experiments")

class ResearchQuestion(BaseModel):
    research_question: str = Field(description="The research question")

class Hypothesis(BaseModel):
    hypothesis: str = Field(description="The hypothesis")

class Objectives_sketch(BaseModel):
    objectives_sketch: str = Field(description="The objectives sketch")

class Sketch(BaseModel):

    Research_questions:list[ResearchQuestion] = Field(description="The research questions")
    Hypotheses:list[Hypothesis] = Field(description="The hypotheses")
    Objectives_sketches:list[Objectives_sketch] = Field(description="The objectives sketches")

class Suggestions(BaseModel):

    # suggestions: list[Suggestion] = Field(description="The suggestions of new paper topics from the related work")
    seggestion_A_title: str = Field(description="The title of the suggestion of new paper topic A from the related work")
    seggestion_A: str = Field(description="The suggestion of new paper topic A from the related work")
    seggestion_A_detail: str = Field(description="The suggestion of new paper topic A detail from the related work")
    seggestion_B_title: str = Field(description="The title of the suggestion of new paper topic B from the related work")
    seggestion_B: str = Field(description="The suggestion of new paper topic B from the related work")
    seggestion_B_detail: str = Field(description="The suggestion of new paper topic B detail from the related work")
    seggestion_C_title: str = Field(description="The title of the suggestion of new paper topic C from the related work")
    seggestion_C: str = Field(description="The suggestion of new paper topic C from the related work")
    seggestion_C_detail: str = Field(description="The suggestion of new paper topic C detail from the related work")

class RelatedWork(BaseModel):

    is_related_work: bool = Field(description="Whether the summary is related to the description")

class Keywords(BaseModel):

    keywords: list = Field(description="The keywords generated from the description")

counter_db = redis.Redis(host=redis_server, port=redis_port, db=0) # string
user_rec_db = redis.Redis(host=redis_server, port=redis_port, db=1) # hash
idea_db = redis.Redis(host=redis_server, port=redis_port, db=2) # hash
suggest_db = redis.Redis(host=redis_server, port=redis_port, db=3) # hash
paper_sketch_db = redis.Redis(host=redis_server, port=redis_port, db=4) # hash

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     _ = requests.post(f"{ollama_server}/api/pull", json={"name": "nomic-embed-text"})
#     _ = requests.post(f"{ollama_server}/api/pull", json={"name": "jina/jina-embeddings-v2-snall-en"})

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
        keywords (str): The keywords.
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
    keywords_str = " ".join(keywords.split(","))
    print(f"Function name: get_related_work, keywords_str: {keywords_str}")

    # get related works
    related_works = selfarxiv.Search_paper(keywords_str)

    for related_work in related_works:
        related.append({'title': related_work['title'], 'summary': related_work['summary'], 'arxiv_id': related_work['arxiv_id'], 'authors': related_work['authors']})
    print(f"Function name: get_related_work, related: {related}")
    return {"related_work": related}

@app.post("/suggest_topic")
async def suggest_topic(data:dict):
    """
    A function that handles the suggest_idea endpoint.

    Args:
        api_key (str): The API key.
        related_works (list): The related works.

    Returns:
        list[str]: A list of dictionaries representing the suggestions of new paper topics from the related work.
    """
    return_data = []
    api_key = data["api_key"]
    related_works = data["related_works"]
    chat = ChatGroq(
        temperature=0,
        model="mixtral-8x7b-32768",
        groq_api_key=api_key # Optional if not set as an environment variable
    )

    related_works_str = "\n".join([f"{work['title']} {work['summary']}" for work in related_works])

    structured_llm = chat.with_structured_output(Suggestions)
    out_put = structured_llm.invoke(f"Generate a new paper topic based on the related works of a paper and must be new topic. Related works: {related_works_str}")
    print(f"Function name: suggest_topic, out_put: {out_put}")
    return_data.append({"suggestion": str(out_put.seggestion_A), "suggestion_detail": str(out_put.seggestion_A_detail), "suggestion_title": str(out_put.seggestion_A_title)})
    return_data.append({"suggestion": str(out_put.seggestion_B), "suggestion_detail": str(out_put.seggestion_B_detail), "suggestion_title": str(out_put.seggestion_B_title)})
    return_data.append({"suggestion": str(out_put.seggestion_C), "suggestion_detail": str(out_put.seggestion_C_detail), "suggestion_title": str(out_put.seggestion_C_title)})
    return {"suggestions": return_data}

@app.post("/save_suggestion")
async def save_suggestion(data:dict):
    """
    A function that handles the save_suggestion endpoint.

    Args:
        suggestion (str): The suggestion of new paper topic.
        suggestion_detail (str): The suggestion of new paper topic detail.
        suggestion_title (str): The title of the suggestion of new paper topic.

    Returns:
        dict: A dictionary with the message "Suggestion saved".
    """
    suggestion = data["suggestion"]
    suggestion_detail = data["suggestion_detail"]
    suggestion_title = data["suggestion_title"]
    suggestion_id = counter_db.incr("suggestion_counter")
    suggest_db.hmset(suggestion_id, {"suggestion": suggestion, "suggestion_detail": suggestion_detail, "suggestion_title": suggestion_title})
    return {"status": "Suggestion saved"}

@app.get("/suggestions")
async def get_suggestions():
    """
    A function that handles the suggestions endpoint.

    Returns:
        dict: A dictionary with the suggestions.
    """
    suggestions = {}
    for key in suggest_db.keys():
        suggestions[key] = suggest_db.hgetall(key)
    return {"suggestions": suggestions}

@app.post("/generate_paper_sketch")
async def generate_paper_sketch(data:dict):
    """
    A function that handles the generate_paper_sketch endpoint.

    Args:

    Returns:
    """
    suggest_title = data["suggestion_title"]
    suggest = data["suggestion"]
    suggest_detail = data["suggestion_detail"]
    api_key = data["api_key"]
    chat = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        groq_api_key=api_key
    )

    structured_llm = chat.with_structured_output(Sketch)
    out_put = structured_llm.invoke(f"suggest title: {suggest_title}\n\nsuggest {suggest}\n\nsuggest detail {suggest_detail} Based on these, generate research questions, hypotheses, and objectives.")
    return out_put

@app.post("/save_paper_sketch")
async def save_paper_sketch(data:dict):
    """
    A function that handles the save_paper_sketch endpoint.

    Args:

    Returns:
    """
    paper_sketch = data['paper_sketch']
    research_questions:list = paper_sketch["Research_questions"]
    hypotheses:list = paper_sketch["Hypotheses"]
    objectives_sketches:list = paper_sketch["Objectives_sketches"]
    research_questions_str = "<block>".join([question['research_question'] for question in research_questions])
    hypotheses_str = "<block>".join([hypothesis['hypothesis'] for hypothesis in hypotheses])
    objectives_sketches_str = "<block>".join([objectives_sketch['objectives_sketch'] for objectives_sketch in objectives_sketches])
    paper_sketch_id = counter_db.incr("paper_sketch_counter")
    paper_sketch_db.hset(paper_sketch_id, mapping={"research_questions": research_questions_str, "hypotheses": hypotheses_str, "objectives_sketches": objectives_sketches_str})
    return {"status": "Paper sketch saved"}

@app.get("/paper_sketches")
async def get_paper_sketches():
    """
    A function that handles the paper_sketches endpoint.

    Returns:
    """
    paper_sketches = {}
    for key in paper_sketch_db.keys():
        temp_dict = paper_sketch_db.hgetall(key)
        new_dict = {}
        new_dict["research_questions"] = temp_dict[b"research_questions"].decode('utf-8').split("<block>")
        new_dict["hypotheses"] = temp_dict[b"hypotheses"].decode('utf-8').split("<block>")
        new_dict["objectives_sketches"] = temp_dict[b"objectives_sketches"].decode('utf-8').split("<block>")
        paper_sketches[key] = new_dict
    return {"paper_sketches": paper_sketches}

@app.get("/paper_sketch/{paper_sketch_id}")
async def get_paper_sketch(paper_sketch_id:int):
    """
    A function that handles the paper_sketch endpoint.

    Args:
    """
    return paper_sketch_db.hgetall(paper_sketch_id)

@app.post("/generate_experiment_design")
async def generate_experiment_design(data:dict):
    """
    A function that handles the generate_experiment_design endpoint.

    Args:
    """
    paper_sketch = data["paper_sketch"]
    research_questions = paper_sketch['research_questions']
    hypotheses = paper_sketch['hypotheses']
    objectives_sketches = paper_sketch['objectives_sketches']
    api_key = data["api_key"]
    use_openai = data["use_openai"]
    if not use_openai:
        # gemma2 9b can't handle the structured output
        chat = ChatGroq(
            temperature=0,
            model="mixtral-8x7b-32768",
            # model="llaama3-70b-8192",
            groq_api_key=api_key
        )
    else:
        from langchain_openai import ChatOpenAI
        chat = ChatOpenAI(
            temperature=0,
            model="gpt-4-turbo",
            openai_api_key=api_key
        )
    research_questions_str = "\n- ".join(research_questions)
    hypotheses_str = "\n- ".join(hypotheses)
    objectives_sketches_str = "\n- ".join(objectives_sketches)
    structured_llm = chat.with_structured_output(ExperimentSketch)
    out_put = structured_llm.invoke(f"Research questions:\n- {research_questions_str}\n\nHypotheses:\n- {hypotheses_str}\n\nObjectives:\n- {objectives_sketches_str}\n\nBased on these, design the experiment.")
    return out_put

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8081) # In docker need to change to 0.0.0.0