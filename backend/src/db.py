import pymongo
import json
import random
import os
from dotenv import load_dotenv
from models.index import Feedback
from models.index import Ordinal

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository

load_dotenv()


class OrdinalRepository(AbstractRepository[Ordinal]):
    class Meta:
        collection_name = "ordinals"


    # def __init__(self):
    #     self.db = get_db()
    #     self.collection = self.db["ordinals"]

    # def get_ordinals(self):
    #     ordinals = self.collection.find()
    #     return ordinals

    # def get_ordinal_by_id(self, id):
    #     query = {"id": id}
    #     ordinal = self.collection.find(query)
    #     return ordinal

    # def get_random_ordinal(self):
    #     count = self.collection.count_documents({})
    #     if count == 0:
    #         return None

    #     document = self.collection.find_one()
    #     if document:
    #         ordinal = Ordinal(**document)
    #         return ordinal
    #     else:
    #         return None

    # def insert_ordinal(self, ordinal: Ordinal):
    #     ordinal_dict = ordinal.to_dict()
    #     result = self.collection.insert_one(ordinal_dict)
    #     print(f"Inserted ordinal with id: {result.inserted_id}")
    #     return result.inserted_id

    # def seed_ordinals(self):
    #     ordinals = load_seed_ordinals()

    #     for ordinal in ordinals:
    #         self.insert_ordinal(ordinal)

    #     return ordinals


def get_db():
    url = os.getenv('MONGO_URL')
    client = pymongo.MongoClient(url)
    db = client["ordinals"]
    return db


def get_ordinals_collection():
    db = get_db()
    collection = db["ordinals"]
    return collection


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


def insert_feedback(feedback: Feedback) -> int:
    db = get_db()
    collection = db["feedback"]

    feedback_dict = feedback.to_dict()

    result = collection.insert_one(feedback_dict)
    print(f"Inserted feedback with id: {result.inserted_id}")
    return result.inserted_id


def get_ordinals():
    collection = get_ordinals_collection()
    ordinals = collection.find()
    return ordinals


def get_ordinals_2():
    url = os.getenv('MONGO_URL')
    client = pymongo.MongoClient(url)
    database = client["ordinals"]
    repo = OrdinalRepository(database=database)
    ordinals = repo.find({"id": "65d7f8fcb0d3e6dc93f9a771"})
    return ordinals


def get_ordinal_by_id():
    db = get_db()
    collection = db["ordinals"]

    query = {"id": id}
    ordinal = collection.find(query)
    return ordinal


def get_random_ordinal() -> Ordinal:
    db = get_db()
    collection = db["ordinals"]
    count = collection.count_documents({})
    if count == 0:
        return None

    # random_skip = random.randint(0, count - 1) if count else 0

    # ordinal = collection.find().skip(random_skip).limit(1)
    document = collection.find_one()
    # print(f"Random ordinal: {ordinal}")
    # print(type(ordinal))

    if document:
        ordinal = Ordinal(**document)
        return ordinal

    else:
        return None


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
