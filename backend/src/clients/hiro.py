import requests
import redis


def get_ordinal_content(id):
    # get the inscription off its id, eg: b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # check if the inscription is in the cache
    content = r.get(id)

    if content:
        return content

    # https://docs.hiro.so/ordinals/inscription-content
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}/content"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


def get_ordinal_metadata(id):
    # get the metadata off its id, eg: b4d12e3941fcab5cba27815d6e855fe9df970913e6b4dfbcb5c2a88564c3d667i0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # check if the metadata is in the cache
    metadata = r.get(id)

    if metadata:
        return metadata

    # https://docs.hiro.so/ordinals/inscription-metadata
    url = f"https://api.hiro.so/ordinals/v1/inscriptions/{id}"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        r.set(id, response.text)

    print(response.text)
    return response.text
