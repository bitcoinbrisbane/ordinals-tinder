import random
import db
import redis
from dotenv import load_dotenv
from dtos.index import Ordinal
import pandas as pd
import os

load_dotenv()


def train():
    return True


def next(address) -> Ordinal:
    print("address", address)

    redis_url = os.getenv('REDIS_URL')
    r = redis.Redis.from_url(redis_url)

    ordinals = db.load_seed_ordinals()
    feedbacks = db.get_feedbacks(address)
    if not feedbacks:
        # Get random ordinal number
        i = random.randint(1, 10)
        ordinal = ordinals[i]
        return ordinal

    # cached_feedbacks = r.get(address)

    # ordinals = r.get('ordinals')
    # if not ordinals:
    #     ordinals = db.load_seed_ordinals()
    #     r.set('ordinals', ordinals)

    

    # if cached_feedbacks:
    #     return cached_feedbacks
        

    # mock data to test the function
    data = {
        'user_id': [1, 1, 2, 2, 3, 3, 4, 4],
        'id': ['img1', 'img2', 'img2', 'img3', 'img1', 'img4', 'img4', 'img3'],
        'view_time_seconds': [120, 30, 45, 200, 150, 60, 10, 75],
        'liked': [True, False, True, True, True, False, False, True]
    }

    df = pd.DataFrame(data)

    # Find images liked by the target user
    liked_images = set(df[(df['user_id'] == address) & (df['liked'])]['image_id'])

    # Find other users who liked the same images
    similar_users = df[df['id'].isin(liked_images) & (df['user_id'] != id) & (df['liked'])]['user_id'].unique()
    
    # Recommend images liked by similar users but not yet viewed by the target user
    recommendations = df[(df['user_id'].isin(similar_users)) & (df['liked']) & (~df['id'].isin(liked_images))]['id'].unique()

    # return a random image from the recommendations

    

    # if len(feedbacks) < 5:
    #     # select random ordinals to train

    #     # load a dictionary of ordinals from the json
    #     ordinals = db.load_seed_ordinals()

    #     # Get random ordinal number
    #     i = random.randint(1, 10)
    #     ordinal = ordinals[i]
    #     return ordinal
    # else:

    
    # filter liked ordinals
    feedbacks = feedbacks.filter(liked=True)

    # select the next ordinal to train
    ordinal = db.get_next_ordinal(address)
    return ordinal
