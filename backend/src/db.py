import pymongo
import json
import random
import os
from dotenv import load_dotenv
from models.index import Feedback
from models.index import Ordinal
from models.index import User, UserInDB

load_dotenv()


def get_db():
    url = os.getenv('MONGO_URL')

    if not url:
        raise Exception("MONGO_URL not found in environment variables.")

    client = pymongo.MongoClient(url)
    db = client["ordinals"]
    return db


def get_feedback_collection():
    db = get_db()
    collection = db["feedback"]
    return collection


def get_ordinals_collection():
    db = get_db()
    collection = db["ordinals"]
    return collection


def add_user(user_in_db: UserInDB):
    db = get_db()
    collection = db["users"]

    if collection.find_one({"email": user_in_db.email}):
        return {"error": "User already exists"}

    user_dict = user_in_db.dict()
    result = collection.insert_one({"user": user_dict})
    return result.inserted_id


def get_user(email: str) -> User:
    db = get_db()
    collection = db["users"]

    query = {"email": email}
    document = collection.find_one(query)
    return User(**document)


def get_feedbacks():
    db = get_db()
    collection = db["feedback"]
    feedbacks = collection.find()
    return feedbacks


def get_user_feedbacks(user: str):
    collection = get_feedback_collection()

    query = {"user": user}
    feedbacks = collection.find(query)
    return feedbacks


def insert_feedback(feedback: Feedback) -> str:
    collection = get_feedback_collection()

    feedback_dict = feedback.to_dict()

    result = collection.insert_one(feedback_dict)
    return str(result.inserted_id)


def get_ordinals():
    collection = get_ordinals_collection()
    ordinals = collection.find()
    return ordinals


def get_ordinal_by_id(id: str) -> Ordinal:
    collection = get_ordinals_collection()

    query = {"id": id}
    document = collection.find(query)

    return Ordinal(**document)


def get_random_ordinal() -> Ordinal:
    collection = get_ordinals_collection()
    count = collection.count_documents({})
    if count == 0:
        return None

    random_skip = random.randint(0, count - 1) if count else 0
    cursor = collection.find().skip(random_skip).limit(1)

    if cursor:
        document = next(cursor)
        ordinal = Ordinal(**document)
        return ordinal

    else:
        return None


def insert_ordinal(ordinal: Ordinal) -> str:
    collection = get_ordinals_collection()
    ordinal_dict = ordinal.to_dict()

    result = collection.insert_one(ordinal_dict)
    print(f"Inserted ordinal with id: {result.inserted_id}")
    return result.inserted_id


def seed_ordinals() -> list[Ordinal]:
    ordinals = load_seed_ordinals()

    for ordinal in ordinals:
        insert_ordinal(ordinal)

    return ordinals


def load_seed_ordinals() -> list[Ordinal]:
    # Opening JSON file
    json_file_path = './data/seed.json'

    try:
        with open(json_file_path, 'r') as file:
            ordinals_data = json.load(file)
            ordinals_list = [Ordinal(**ordinal_data)
                             for ordinal_data in ordinals_data]
            return ordinals_list
    except FileNotFoundError:
        print("The file was not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []
