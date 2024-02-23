from models.index import Ordinal
from dotenv import load_dotenv

import pymongo
import db

load_dotenv()


class OrdinalsRepository:
    def __init__(self):
        self.db = db.get_db()
        self.collection = self.db["ordinals"]

#     def get_ordinals(self):
#         ordinals = self.collection.find()
#         return ordinals

#     def get_ordinal_by_id(self, id):
#         query = {"id": id}
#         ordinal = self.collection.find(query)
#         return ordinal

#     def get_random_ordinal(self) -> Ordinal:
#         count = self.collection.count_documents({})
#         if count == 0:
#             return None

#         random_skip = random.randint(0, count - 1) if count else 0
#         cursor = self.collection.find().skip(random_skip).limit(1)

#         if cursor:
#             document = next(cursor)
#             ordinal = Ordinal(**document)
#             return ordinal

#         else:
#             return None

#     def insert_ordinal(self, ordinal: Ordinal) -> str:
#         ordinal_dict = ordinal.to_dict()

#         result = self.collection.insert_one(ordinal_dict)
#         print(f"Inserted ordinal with id: {result.inserted_id}")
#         return result.inserted_id

#     def seed_ordinals(self):
#         ordinals = self.load_seed_ordinals()

#         for ordinal in ordinals:
#             self.insert_ordinal(ordinal)

#         return ordinals

#     def load_seed_ordinals(self) -> list[Ordinal]:
#         # Opening JSON file
#         json_file_path = './data/seed.json'

#         with open(json_file_path, 'r') as file:
#             data = json.load(file)  # Load the JSON data from the file
#             ordinals = [Ordinal(ordinal['id'], ordinal['number'], ordinal['address'], ordinal['value'], ordinal['content_type'], ordinal['sat_rarity'])
#                         for ordinal in data['ordinals']]

#         return ordinals