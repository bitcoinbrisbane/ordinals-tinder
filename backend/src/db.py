from mongoengine import Document, StringField, IntField, connect

class OrdinalMetaData(Document):
    image = StringField(required=True)
    label = IntField(required=True)


class Feedback(Document):
    address = StringField(required=True)
    signature = StringField(required=True)
    message = StringField(required=True)
    liked = StringField(required=True)


connect("ordinals")
