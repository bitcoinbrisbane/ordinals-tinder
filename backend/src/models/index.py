from pydantic import BaseModel


class Feedback(BaseModel):
    id: str
    user: str
    liked: bool
    time_stamp: int
    time_spent: int

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "liked": self.liked,
            "time_stamp": self.time_stamp,
            "time_spent": self.time_spent
        }


class FeedbackDTO(Feedback):
    message: str
    signature: str

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "liked": self.liked,
            "message": self.message,
            "signature": self.signature,
            "time_stamp": self.time_stamp,
            "time_spent": self.time_spent
        }


# View model to send to the front end
class Ordinal(BaseModel):
    id: str
    address: str
    content_type: str
    number: int
    sat_rarity: str
    value: int

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "content_type": self.content_type,
            "number": self.number,
            "sat_rarity": self.sat_rarity,
            "value": self.value
        }
