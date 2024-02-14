import random
import db
import redis
from dotenv import load_dotenv
import os

load_dotenv()


def train():
    return True


def next(address):
    print("address", address)

    redis_url = os.getenv('REDIS_URL')
    r = redis.Redis.from_url(redis_url)

    cached_feedbacks = r.get(address)

    ordinals = r.get('ordinals')
    if not ordinals:
        ordinals = db.load_seed_ordinals()
        r.set('ordinals', ordinals)

    

    # if cached_feedbacks:
    #     return cached_feedbacks


    feedbacks = db.get_feedbacks(address)

    if len(feedbacks) < 5:
        # select random ordinals to train

        # load a dictionary of ordinals from the json
        ordinals = db.load_seed_ordinals()

        # Get random ordinal number
        i = random.randint(1, 10)
        ordinal = ordinals[i]
        return ordinal
    else:
        # filter liked ordinals
        feedbacks = feedbacks.filter(liked=True)

        # select the next ordinal to train
        ordinal = db.get_next_ordinal(address)
        return ordinal
