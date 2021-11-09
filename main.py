from fastapi import FastAPI
from models import Query
from modules.search import search

app = FastAPI()

@app.get("/")
def root():
    return {
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/model")
def ask_to_model(query: Query):
    question = query.content
    response = search(question)
    urls = [{
        "url": site
    } for site in response]
    return {
        "question": question,
        "results": urls
    }

