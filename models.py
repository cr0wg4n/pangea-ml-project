from pydantic import BaseModel

class Query(BaseModel):
    question: str
    country: str
    language: str