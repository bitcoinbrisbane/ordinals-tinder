# Create a fast api 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/next/{address}")
def next(address: str):

    ordinal = {

    }

    return ordinal


@app.get("/image/{index}")
def image(index: int):
    return {"index": index}