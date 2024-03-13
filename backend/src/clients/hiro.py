import json
import requests
import redis

from dotenv import load_dotenv
from models.index import Ordinal
import os


load_dotenv()

def redis_client():
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        raise ValueError("No REDIS_URL provided")
    
    return redis.Redis.from_url(redis_url)


def get_ordinal_content(id) -> str:
    r = redis_client()

    # check if the inscription is in the cache
    content = r.get(id)

    # if content:
    #     return content

    # get the inscription off its id, eg: eb5f415da98b4a61407dac2452cb45a3fd168b38c95eec2c2bfd59c51b71cd4ci0
    inscription = get_ordinal_content(id)

    # https://docs.hiro.so/ordinals/inscription-content eg https://api.hiro.so/ordinals/v1/inscriptions/b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0/content
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}/content"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

    if response.status_code != 200:
        return None
    
    r.set(id, response.text)

    return response.text


def get_ordinal(id) -> Ordinal:
    # get the metadata off its id, eg: b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0
    r = redis_client()

    # check if the metadata is in the cache
    # metadata = r.get(id)

    # if metadata:
    #     return metadata

    # https://docs.hiro.so/ordinals/inscription-metadata
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text

    # Convert json into dictionary
    response_dict = response.json()
    r.set(id, json.dumps(response_dict))

    print(json.dumps(response_dict, indent=4, sort_keys=True))

    id = response_dict.get("id")
    address = response_dict.get("address")
    number = response_dict.get("number")
    sat_rarity = response_dict.get("sat_rarity")
    value = response_dict.get("value")
    mime_type = response_dict.get("mime_type")
    content_type = response_dict.get("content_type")

    ordinal = Ordinal(id=id, address=address, number=number, sat_rarity=sat_rarity, value=value, mime_type=mime_type, content_type=content_type)

    return ordinal
