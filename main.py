from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Query
from modules.search import search
from modules.bert import question_answer
from modules.scrapper import get_data

origins = ['*']
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/model")
def ask_to_model(query: Query):
    question = query.question
    print("user question:", question)
    response = search(question)
    sites = []
    # response = [site for site in response if not "www.tripadvisor.es" in site]
    for site in response:
        data = get_data(site)
        if (data):
            sites.append({
                "context": "\n".join(data["paragraphs"]),
                "url": site
            })
    answers = []
    for site in sites: 
        answer = question_answer(question, site["context"])
        if answer: 
            answers.append({
                "answer": answer,
                "url": site["url"]
            })

    ordered = sorted(answers, key=lambda x: x["answer"]["score"], reverse=True)
    return ordered
