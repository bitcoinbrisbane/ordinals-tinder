# from mongoengine import Document, StringField, IntField
import json


# class OrdinalMetaData(Document):
#     image = StringField(required=True)
#     label = IntField(required=True)


# class Feedback(Document):
#     address = StringField(required=True)
#     signature = StringField(required=True)
#     message = StringField(required=True)
#     liked = StringField(required=True)


class Ordinal():
    def __init__(self, id, number, address, value, content_type, sat_rarity):
        self.id = id
        self.number = number
        self.address = address
        self.value = value
        self.content_type = content_type
        self.sat_rarity = sat_rarity

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "address": self.address,
            "value": self.value,
            "content_type": self.content_type,
            "sat_rarity": self.sat_rarity
        }

    def __repr__(self):
        return f"Ordinal(id='{self.id}', number={self.number})"


def load_seed_ordinals() -> list[Ordinal]:
    # Opening JSON file
    json_file_path = './data/seed.json'
    # f = open(json_file_path)

    # # returns JSON object as
    # # a dictionary
    # data = json.load(f)

    # ordinals = []
    # # Iterating through the json

    # # list of ordinals
    # for i in data['ordinals']:
    #     ordinals.append(Ordinal(i.get('id'), i.get('number'), i.get('address'), i.get('sat'), i.get('price'), i.get('content_type'), i.get('sat_rarity')))

    # # Closing file
    # f.close()

    with open(json_file_path, 'r') as file:
        data = json.load(file)  # Load the JSON data from the file
        ordinals = [Ordinal(ordinal['id'], ordinal['number'], ordinal['address'], ordinal['value'], ordinal['content_type'], ordinal['sat_rarity'])
                    for ordinal in data['ordinals']]

    return ordinals
