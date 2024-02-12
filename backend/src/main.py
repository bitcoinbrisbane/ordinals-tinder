# Create a fast api
import random
from dtos.index import Feedback
import utils
import db

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/next/{address}")
def next(address: str):

    print("address", address)

    feedbacks = db.get_feedbacks(address)
    if feedbacks.count() < 5:
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

    # lookup the next ordinal for this users address
    # bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297

    # https://docs.hiro.so/ordinals/inscription-content
    # url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}/content"

    # payload = {}
    # headers = {
    #     'Accept': 'application/json'
    # }

    # # response = requests.request("GET", url, headers=headers, data=payload)
    # # print(response.text)


# @app.get("/image/{index}")
# def image(index: int):
#     return {"index": index}


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