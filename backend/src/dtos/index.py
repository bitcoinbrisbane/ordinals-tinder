from pydantic import BaseModel


class Feedback(BaseModel):
    id: str
    user: str
    message: str
    signature: str
    liked: bool
    time_stamp: int

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "liked": self.liked,
            "time_stamp": self.time_stamp
        }
