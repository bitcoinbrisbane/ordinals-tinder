import requests


def get_ordinal_content(id):
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
