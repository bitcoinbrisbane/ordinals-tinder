# Create a fast api 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/next/{address}")
def next(address: str):

    # lookup the next ordinal for this users address
    # bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297 
    
    ordinal = {
        "id": "6abcb215dae6058653f4ba4d717a00fca46ac8c3dea46876057c128f3786f892i0",
        "address": "bc1paxxeugh54jvrqcwz0hwjlnt4tktuef5jfmfp6tn77x5cdjkrtf3q2lqgh4",
        "sat": "1162315496355503",
        "price": 1000,
        "owner": "",
        "image": "https://api.example.com/image/1162315496355503",
        "metadata": {
        }
    }

    return ordinal


@app.get("/image/{index}")
def image(index: int):
    return {"index": index}