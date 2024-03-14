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
    # r = redis_client()

    # check if the inscription is in the cache
    # content = r.get(id)

    # if content:
    #     return content

    # https://docs.hiro.so/ordinals/inscription-content eg https://api.hiro.so/ordinals/v1/inscriptions/b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0/content
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}/content"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    print(response.content)
    if response.status_code != 200:
        return None
    
    # r.set(id, response.content.hex())

    return response.content


def get_ordinal(id) -> Ordinal:
    # get the metadata off its id, eg: b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0
    r = redis_client()

    # # check if the metadata is in the cache
    response_dict = r.get(id)
    if response_dict:
        response_dict = json.loads(response_dict)


    if not response_dict:
        # https://docs.hiro.so/ordinals/inscription-metadata
        url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # Convert json into dictionary
        response_dict = response.json()
        
        
    print(json.dumps(response_dict, indent=4, sort_keys=True))

    id = response_dict.get("id")
    address = response_dict.get("address")
    number = response_dict.get("number")
    sat_rarity = response_dict.get("sat_rarity")
    value = response_dict.get("value")
    mime_type = response_dict.get("mime_type")
    content_type = response_dict.get("content_type")

    ordinal = Ordinal(id=id, address=address, number=number, sat_rarity=sat_rarity, value=value, mime_type=mime_type, content_type=content_type)

    ordinals_json = json.dumps(ordinal, default=lambda o: o.__dict__)
    r.set(id, ordinals_json)

    return ordinal
