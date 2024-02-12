from pydantic import BaseModel


class Feedback(BaseModel):
    id: str
    user: str
    message: str
    signature: str
    liked: bool

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "liked": self.liked
        }