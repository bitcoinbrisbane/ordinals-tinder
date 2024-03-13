# Create a fast api
import json
import os
import redis
from dotenv import load_dotenv
from models.index import Feedback, FeedbackDTO
from models.index import Ordinal
import utils
import db
import collaboration
import clients.hiro
import ml

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello Ordinals World!"}


# tool to test btc address
@app.get("/address")
def root():
    return utils.generate_bitcoin_address()


@app.get("/ordinal/next/{address}")
def next(address: str):
    try:
        ordinal = collaboration.next(address)
        return ordinal
    except:
        raise HTTPException(status_code=500, detail="No ordinals found")


@app.get("/ordinal/{id}")
def ordinal(id: str) -> Ordinal:
    ordinal_data = clients.hiro.get_ordinal_metadata(id)

    print(json.dumps(ordinal_data, indent=4, sort_keys=True))

    id = ordinal_data.get("id")
    address = ordinal_data.get("address")
    content_type = ordinal_data.get("content_type")
    number = ordinal_data.get("number")
    sat_rarity = ordinal_data.get("sat_rarity")
    value = ordinal_data.get("value")
    
    print(id, address, content_type, number)
    ordinal = Ordinal(id=id, address=address, content_type=content_type, number=number, sat_rarity=sat_rarity, value=value)

    return ordinal


@app.get("/image/{id}")
def image(id: str):
    image = clients.hiro.get_ordinal_content(id)
    return Response(content=image, media_type="image/webp")


@app.post("/feedback", status_code=201)
def set_feedback(feedback: FeedbackDTO):

    # validate the signature
    if not utils.verify_message(feedback.user, feedback.signature, feedback.message):
        return {"error": "Invalid signature"}

    feedback = Feedback(id=feedback.id, user=feedback.user, liked=feedback.liked,
                        time_stamp=feedback.time_stamp, time_spent=feedback.time_spent)

    # save the feedback to the database
    inserted_id = db.insert_feedback(feedback)

    return {"id": str(inserted_id)}


@app.put("/seed", status_code=201)
def seed_ordinals() -> list[Ordinal]:
    try:
        # seed the ordinals
        ordinals = db.seed_ordinals()

        # if cache is enabled, update the cache
        # print("Updating cache")
        # redis_url = os.getenv('REDIS_URL')
        # r = redis.Redis.from_url(redis_url)

        # ordinals_json = json.dumps(ordinals, default=lambda o: o.__dict__)
        # r.set('ordinals', ordinals_json)

        return ordinals
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.post("/ordinal/buy")
def buy():
    return {"tx": "26482871f33f1051f450f2da9af275794c0b5f1c61ebf35e4467fb42c2813403"}


@app.post("/ordinal/sell", status_code=201)
def sell(ordinal: Ordinal):

    valid = utils.verify_message(
        ordinal.address, ordinal.signature, ordinal.message)
    if not valid:
        return HTTPException(status_code=403, detail="Invalid signature")

    # save the ordinal to the database
    inserted_id = db.insert_ordinal(ordinal)

    return {"id": inserted_id}


@app.post("/train")
def train():
    ml.train()
    return {"status": "Training complete"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
