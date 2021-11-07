from fastapi import FastAPI
from models import Query

app = FastAPI()

@app.get("/")
def root():
    return {
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/model")
def ask_to_model(query: Query):
    q = query.content
    return [
        {
            "url": "http://demodemo.com/demodemodemo",
            "answer": "demo demodemodemo"
        },
        {
            "url": "http://demodemo.com/demodemodemo",
            "answer": "demo demodemodemo"
        },
        {
            "url": "http://demodemo.com/demodemodemo",
            "answer": "demo demodemodemo"
        }
    ]
