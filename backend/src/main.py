# Create a fast api
import bitcoin
import requests
import random

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage

from backend.src.dtos.feedback import Feedback
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/next/{address}")
def next(address: str):

    print("address", address)

    # Get random ordinal number
    id = random.randint(1, 1000000)

    # lookup the next ordinal for this users address
    # bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297

    # https://docs.hiro.so/ordinals/inscription-content
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}/content"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

    ordinal = {
        "id": "6abcb215dae6058653f4ba4d717a00fca46ac8c3dea46876057c128f3786f892i0",
        "address": "bc1paxxeugh54jvrqcwz0hwjlnt4tktuef5jfmfp6tn77x5cdjkrtf3q2lqgh4",
        "sat": "1162315496355503",
        "price": 1000,
        "owner": "",
        "image": "https://api.example.com/image/1162315496355503",
        "metadata": {
        }
    }

    return ordinal


@app.get("/image/{index}")
def image(index: int):
    return {"index": index}


def verify_message(address, signature, message):
    """
    Verify a message signed by a Bitcoin private key.

    :param address: The Bitcoin address as a string.
    :param signature: The signature as a base64 encoded string.
    :param message: The original message that was signed.
    :return: True if the verification is successful, False otherwise.
    """
    try:
        message = BitcoinMessage(message)
        return VerifyMessage(P2PKHBitcoinAddress(address), signature, message)
    except Exception as e:
        print(f"Verification failed: {e}")
        return False


@app.post(("/"))
def image(feedback: Feedback):

    # validate the signature
    if not verify_message(feedback.address, feedback.signature, feedback.message):
        return {"error": "Invalid signature"}

    data = {
        "liked": True
    }

    return {"index": index}
