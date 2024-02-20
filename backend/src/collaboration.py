import random
import db
# import redis
from dotenv import load_dotenv
from dtos.index import Ordinal
import pandas as pd
# import os

load_dotenv()

def get_feedbacks_as_df() -> pd.DataFrame:
    feedbacks = db.get_feedbacks()
    return cast_to_df(feedbacks)


def cast_to_df(feedbacks) -> pd.DataFrame:
    if not feedbacks:
        return pd.DataFrame()
    
    data = {
        'user_id': [],
        'id': [],
        'time_spent': [],
        'liked': []
    }

    for feedback in feedbacks:
        data['user_id'].append(feedback.get('user'))
        data['id'].append(feedback.get('id'))
        data['time_spent'].append(feedback.get('time_spent'))
        data['liked'].append(feedback.get('liked'))


    return pd.DataFrame(data)


def get_random_ordinal() -> Ordinal:
    ordinals = db.get_ordinals()
    ordinals_list = list(ordinals)
    return random.choice(ordinals_list)


def next(address) -> Ordinal:
    print(f"Getting next ordinal for user {address}")

    feedbacks = db.get_feedbacks()

    # If we dont have any feedbacks, return a random ordinal
    if not feedbacks:
        return get_random_ordinal()

    df = get_feedbacks_as_df()

    # Find images liked by the target user
    liked_ordinals = set(df[(df['user_id'] == address)
                            & (df['liked'])]['id'])

    # Find other users who liked the same images
    similar_users = df[df['id'].isin(liked_ordinals) & (
        df['user_id'] != id) & (df['liked'])]['user_id'].unique()

    # Recommend images liked by similar users but not yet viewed by the target user
    recommendations = df[(df['user_id'].isin(similar_users)) & (
        df['liked']) & (~df['id'].isin(liked_ordinals))]['id'].unique()

    # print(recommendations)
    recommendations_list = list(recommendations)
    if len(recommendations_list) > 0:
        # Get random ordinal number
        i = random.randint(1, 10)

        # print(ordinals)
        # ordinal = ordinals[i]
        # return ordinal

    return get_random_ordinal()
