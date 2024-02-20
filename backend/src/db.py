import pymongo
import json
import os
from dotenv import load_dotenv
from dtos.index import Feedback
from models.index import Ordinal

load_dotenv()


def get_db():
    url = os.getenv('MONGO_URL')
    client = pymongo.MongoClient(url)
    db = client["ordinals"]
    return db


def get_feedbacks():
    db = get_db()
    collection = db["feedback"]
    feedbacks = collection.find()
    return feedbacks


def get_user_feedbacks(user):
    db = get_db()
    collection = db["feedback"]

    query = {"user": user}

    feedbacks = collection.find(query)
    return feedbacks
    # return list(feedbacks)


def insert_feedback(feedback: Feedback) -> int:
    db = get_db()
    collection = db["feedback"]

    feedback_dict = feedback.to_dict()

    result = collection.insert_one(feedback_dict)
    print(f"Inserted feedback with id: {result.inserted_id}")
    return result.inserted_id


def get_ordinals():
    db = get_db()
    collection = db["ordinals"]

    ordinals = collection.find()
    return ordinals
    # return list(ordinals)


def get_ordinal_by_id() -> Ordinal:
    db = get_db()
    collection = db["ordinals"]

    query = {"id": id}
    ordinal = collection.find(query)
    return ordinal


def insert_ordinal(ordinal: Ordinal):
    db = get_db()
    collection = db["ordinals"]

    ordinal_dict = ordinal.to_dict()

    result = collection.insert_one(ordinal_dict)
    print(f"Inserted ordinal with id: {result.inserted_id}")
    return result.inserted_id


def seed_ordinals():
    ordinals = load_seed_ordinals()

    for ordinal in ordinals:
        insert_ordinal(ordinal)

    return ordinals


def load_seed_ordinals() -> list[Ordinal]:
    # Opening JSON file
    json_file_path = './data/seed.json'

    with open(json_file_path, 'r') as file:
        data = json.load(file)  # Load the JSON data from the file
        ordinals = [Ordinal(ordinal['id'], ordinal['number'], ordinal['address'], ordinal['value'], ordinal['content_type'], ordinal['sat_rarity'])
                    for ordinal in data['ordinals']]

    return ordinals
