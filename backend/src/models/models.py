# class OrdinalMetaData(Document):
#     image = StringField(required=True)
#     label = IntField(required=True)


class Ordinal():
    def __init__(self, id, number, address, sat, price, content_type, sat_rarity):
        self.id = id
        self.number = number
        self.address = address
        self.sat = sat
        self.price = price
        self.content_type = content_type
        self.sat_rarity = sat_rarity

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "address": self.address,
            "sat": self.sat,
            "price": self.price,
            "owner": self.owner,
            "content_type": self.content_type,
            "sat_rarity": self.sat_rarity
        }

    