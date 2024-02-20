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


    data = {
        'user_id': [],
        'id': [],
        'view_time_seconds': [],
        'liked': []
    }

    for feedback in feedbacks:
        data['user_id'].append(feedback.user)
        data['id'].append(feedback.id)
        data['view_time_seconds'].append(feedback.view_time_seconds)
        data['liked'].append(feedback.liked)


    df = pd.DataFrame(data)

    # Find images liked by the target user
    liked_images = set(df[(df['user_id'] == address)
                       & (df['liked'])]['image_id'])

    # Find other users who liked the same images
    similar_users = df[df['id'].isin(liked_images) & (
        df['user_id'] != id) & (df['liked'])]['user_id'].unique()

    # Recommend images liked by similar users but not yet viewed by the target user
    recommendations = df[(df['user_id'].isin(similar_users)) & (
        df['liked']) & (~df['id'].isin(liked_images))]['id'].unique()


    if len(recommendations) > 0:
        ordinal = ordinals[recommendations[0]]
        return ordinal
    
    # Get random ordinal number
    i = random.randint(1, 10)
    ordinal = ordinals[i]
    return ordinal
