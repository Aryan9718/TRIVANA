# app/main.py
from fastapi import FastAPI  # ✅ make sure this line exists

app = FastAPI()  # initialize FastAPI

@app.get("/health")
def health():
    return {"status": "ok"}
