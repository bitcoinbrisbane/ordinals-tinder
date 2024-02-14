# Create a fast api
from dtos.index import Feedback
import utils
import db
import ml
import clients.hiro

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
# from fastapi import HTTP_201_CREATED

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/next/{address}")
def next(address: str):

    ordinal = ml.next(address)
    return ordinal


@app.get("/ordinal/{index}")
def image(index: str):
    ordinal = clients.hiro.get_ordinal_metadata(index)
    # Return as json
    jsonable_encoder(ordinal)
    return JSONResponse(content=ordinal)


@app.get("/image/{index}")
def image(index: str):
    image = clients.hiro.get_ordinal_content(index)
    print(image)
    return Response(content=image, media_type="image/webp")


@app.post(("/"))
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
