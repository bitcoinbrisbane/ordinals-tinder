import json
import requests
import redis

from dotenv import load_dotenv
import os

load_dotenv()

def get_ordinal_content(id):
    # get the inscription off its id, eg: b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0
    redis_url = os.getenv('REDIS_URL')
    r = redis.Redis.from_url(redis_url)

    # check if the inscription is in the cache
    content = r.get(id)

    if content:
        return content

    # https://docs.hiro.so/ordinals/inscription-content eg https://api.hiro.so/ordinals/v1/inscriptions/b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0/content
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}/content"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


def get_ordinal_metadata(id):
    # get the metadata off its id, eg: b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0
    redis_url = os.getenv('REDIS_URL')
    r = redis.Redis.from_url(redis_url)

    # check if the metadata is in the cache
    metadata = r.get(id)

    # if metadata:
    #     return metadata

    # https://docs.hiro.so/ordinals/inscription-metadata
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # return this as json
    # Convert json into dictionary
    response_dict = response.json()
    # if response.status_code == 200:
    #     r.set(id, response_dict)
    
    # Pretty Printing JSON string back
    # print(json.dumps(response_dict, indent=4, sort_keys=True))
    return response_dict
