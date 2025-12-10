# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/add")
def add(a: int = 0, b: int = 0):
    return {"result": a + b}
