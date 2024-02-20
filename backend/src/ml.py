import random
import db
from dotenv import load_dotenv
from dtos.index import Ordinal

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
# from scipy import sparse
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense
from tensorflow.keras.optimizers import Adam

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


def train():
    df = get_feedbacks_as_df()

    # Assuming user_id and id start from 1
    num_users = 3 # df['user_id'].value_counts()
    num_images = 100 # df['id'].value_counts()

    # Split the data
    train, test = train_test_split(df, test_size=0.2, random_state=42)

    # # Convert to a user-item matrix
    # user_item_matrix = df.pivot_table(index='user_id', columns='id', values='liked', fill_value=0)
    # print(user_item_matrix)

    # Model architecture
    user_input = Input(shape=(1,), name='user_input')
    user_embedding = Embedding(num_users, 5, name='user_embedding')(user_input)
    user_vec = Flatten(name='flatten_users')(user_embedding)

    image_input = Input(shape=(1,), name='image_input')
    image_embedding = Embedding(num_images, 5, name='image_embedding')(image_input)
    image_vec = Flatten(name='flatten_images')(image_embedding)

    prod = Dot(name='dot_product', axes=1)([user_vec, image_vec])
    model = Model(inputs=[user_input, image_input], outputs=prod)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.summary()
    model.save('tf_model.h5')


    # Train the model
    history = model.fit([train.user_id, train.id], train.liked, epochs=10, validation_split=0.1)
    print(history)

    predictions = model.predict([test.user_id, test.id])
    print(predictions)



def next(address) -> Ordinal:
    print(f"Getting next ordinal for user {address}")

    # redis_url = os.getenv('REDIS_URL')
    # r = redis.Redis.from_url(redis_url)
    ordinals = db.get_ordinals()

    # # get ordinals from redis
    # ordinals = r.get('ordinals')
    # if not ordinals:
    #     ordinals = db.get_ordinals()
    #     json_ordinals = json.dumps(ordinals)
    #     r.set('ordinals', json_ordinals)

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

    print(recommendations)
    recommendations_list = list(recommendations)
    if len(recommendations_list) > 0:
        # Get random ordinal number
        i = random.randint(1, 10)

        print(ordinals)
        ordinal = ordinals[i]
        return ordinal

    # if len(recommendations) > 0:
    #     ordinal = ordinals[recommendations[0]]
    #     return ordinal

    # # Get random ordinal number
    # i = random.randint(1, 10)
    # ordinal = ordinals[0]
    # return ordinal
