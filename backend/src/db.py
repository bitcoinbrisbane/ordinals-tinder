import pymongo
import json

from dtos.index import Feedback
from models.index import Ordinal


def insert_feedback(feedback: Feedback):
    # client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ordinals"]
    collection = db["feedback"]

    feedback_dict = feedback.to_dict()

    result = collection.insert_one(feedback_dict)
    print(f"Inserted feedback with id: {result.inserted_id}")


def load_seed_ordinals() -> list[Ordinal]:
    # Opening JSON file
    json_file_path = './data/seed.json'

    with open(json_file_path, 'r') as file:
        data = json.load(file)  # Load the JSON data from the file
        ordinals = [Ordinal(ordinal['id'], ordinal['number'], ordinal['address'], ordinal['value'], ordinal['content_type'], ordinal['sat_rarity'])
                    for ordinal in data['ordinals']]

    return ordinals


def get_feedbacks(user) -> list[Feedback]:
    # client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ordinals"]
    collection = db["feedback"]

    query = { "user": user }

    feedbacks = collection.find(query)

    return feedbacks