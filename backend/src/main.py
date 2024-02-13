# Create a fast api
import random
from dtos.index import Feedback
import utils
import db
import clients.hiro

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/next/{address}")
def next(address: str):

    print("address", address)

    feedbacks = db.get_feedbacks(address)
    if len(feedbacks) < 5:
        ## select random ordinals to train

        # load a dictionary of ordinals from the json
        ordinals = db.load_seed_ordinals()

        # Get random ordinal number
        i = random.randint(1, 10)
        ordinal = ordinals[i]
        return ordinal
    else:
        ## filter liked ordinals
        feedbacks = feedbacks.filter(liked=True)

        ## select the next ordinal to train
        ordinal = db.get_next_ordinal(address)
        return ordinal


@app.get("/image/{index}")
def image(index: int):
    image = clients.hiro.get_ordinal_content(index)
    return image


@app.post(("/"))
def set_feedback(feedback: Feedback):

    # validate the signature
    if not utils.verify_message(feedback.user, feedback.signature, feedback.message):
        return {"error": "Invalid signature"}

    
    # save the feedback to the database
    db.insert_feedback(feedback)

    return {"index": 0}


@app.post("/buy")
def buy():
    return {"index": 0}