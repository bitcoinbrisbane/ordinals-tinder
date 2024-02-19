# Create a fast api
import json
import os
from dtos.index import Feedback
from dtos.index import Ordinal
import utils
import db
import ml
import clients.hiro

from fastapi import FastAPI
from fastapi.responses import Response

load_dotenv()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


# tool to test btc address
@app.get("/address")
def root():
    return utils.generate_bitcoin_address()


@app.get("/next/{address}")
def next(address: str):

    ordinal = ml.next(address)
    return ordinal


@app.get("/ordinal/{index}")
def image(index: str):
    ordinal_data = clients.hiro.get_ordinal_metadata(index)
    
    print(json.dumps(ordinal_data, indent=4, sort_keys=True))

    id = ordinal_data.get("id")
    number = ordinal_data.get("number")
    address = ordinal_data.get("address")
    url = os.getenv('API_URL')
    content_url = f"{url}/image/{id}"
    content_type = ordinal_data.get("content_type")

    return Ordinal(id=id, number=number, address=address, content_url=content_url, content_type=content_type)


@app.get("/image/{index}")
def image(index: str):
    image = clients.hiro.get_ordinal_content(index)
    print(image)
    return Response(content=image, media_type="image/webp")


@app.post("/", status_code=201)
def set_feedback(feedback: Feedback):

    # validate the signature
    if not utils.verify_message(feedback.user, feedback.signature, feedback.message):
        return {"error": "Invalid signature"}

    # save the feedback to the database
    inserted_id = db.insert_feedback(feedback)

    return {"id": inserted_id}


@app.post("/buy")
def buy():
    return {"tx": "26482871f33f1051f450f2da9af275794c0b5f1c61ebf35e4467fb42c2813403"}
