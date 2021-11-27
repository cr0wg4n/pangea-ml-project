# Pangea ML Project

## Project Setup

* Create a virtualenv 
* Activate the virtualenv
* Install all dependencies
```bash
pip install -r requirements.txt
```
## Run Server 

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Run Tests

```bash
python -m unittest tests  
```
