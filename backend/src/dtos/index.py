from pydantic import BaseModel

class Feedback(BaseModel):
    def __init__(self, id, user, liked):
        self.id = id
        self.user = user
        self.liked = liked

    def __repr__(self):
        return f"Feedback(id='{self.id}', user={self.user}, liked={self.liked})"
