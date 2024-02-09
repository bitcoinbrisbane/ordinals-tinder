from pydantic import BaseModel


class Feedback(BaseModel):
    address: str
    message: str
    signature: str
    viewed: int
    liked: bool
    ordinal: int
