from mongoengine import Document, StringField, IntField
import json


class OrdinalMetaData(Document):
    image = StringField(required=True)
    label = IntField(required=True)


class Feedback(Document):
    address = StringField(required=True)
    signature = StringField(required=True)
    message = StringField(required=True)
    liked = StringField(required=True)



def load_seed_ordinals():
    # Opening JSON file
    f = open('../data/data.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    for i in data['ordinals']:
        print(i)

    # Closing file
    f.close()
