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

countries = {
    "bo": "bolivia"
}

@app.post("/model")
def ask_to_model(query: Query):
    try:
        question = query.question
        country = query.country
        language = query.language
        print("> question:", question, "language:", language, "country:", country, "\n")




        c = countries[country] if country in countries else None
        question_filtered = "{} {}".format(question, c if c else "")
        question_filtered = question_filtered.strip()
        response = search(question_filtered, lang=language)
        sites = []
        for site in response:
            data = get_data(site)
            if (data):
                paragraphs = data["paragraphs"]
                paragraphs = "\n".join(paragraphs)
                sites.append({
                    "context": paragraphs,
                    "url": site
                })
        answers = []
        for site in sites: 
            answer = question_answer(question, site["context"], language)
            if answer: 
                answers.append({
                    "answer": answer,
                    "url": site["url"]
                })
        if len(answers):
            ordered = sorted(answers, key=lambda x: x["answer"]["score"], reverse=True)
            return ordered
        else:
            return []
    except:
        return []
