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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "0de32bd3630c06a185ae0b7fdf132f7d87c26893342b056644b0d53696266675i0",
                    "user": "bc1paxxeugh54jvrqcwz0hwjlnt4tktuef5jfmfp6tn77x5cdjkrtf3q2lqgh4",
                    "liked": True,
                    "message": "e7a6259b-e1b0-4e1e-a3f2-80fc0f87695e",
                    "signature": "3045022100d8f8b4c7b9a8c6b1d2f0f2d3c0b5f1c61ebf35e4467fb42c2813403",
                    "time_stamp": 1708735333,
                    "time_spent": 1000,
                }
            ]
        }
    }

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
    number: int
    sat_rarity: str
    value: int
    mime_type: str
    content_type: str

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "number": self.number,
            "sat_rarity": self.sat_rarity,
            "value": self.value,
            "mime_type": self.mime_type,
            "content_type": self.content_type
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str