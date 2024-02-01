from mongoengine import Document, StringField, IntField, connect

class OrdinalMetaData(Document):
    image = StringField(required=True)
    label = IntField(required=True)