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
    number: int
    address: str
    content_url: str
    content_type: str

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "address": self.address,
            "content_url": self.content_url,
            "content_type": self.content_type
        }
