import random
import db
import redis
from dotenv import load_dotenv
from dtos.index import Ordinal
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

load_dotenv()


def get_feedbacks_as_df() -> pd.DataFrame:
    feedbacks = db.get_feedbacks()
    if not feedbacks:
        return pd.DataFrame()

    data = {
        'user_id': [],
        'id': [],
        'time_spent': [],
        'liked': []
    }

    for feedback in feedbacks:
        data['user_id'].append(feedback.user)
        data['id'].append(feedback.id)
        data['time_spent'].append(feedback.time_spent)
        data['liked'].append(feedback.liked)

    return pd.DataFrame(data)


def train():
    df = get_feedbacks_as_df()

    # Convert categorical variables to numerical
    df['user_id'] = df['user_id'].astype('category').cat.codes
    df['id'] = df['id'].astype('category').cat.codes

    # Prepare features and labels
    X = df[['user_id', 'id', 'time_spent']]  # Features
    y = df['liked']  # Target variable

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Initialize and train the classifier
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Example: Predicting for a specific user for images not in their viewed list
    user_id = 0  # Assuming numeric user_id after conversion
    images_to_recommend = np.setdiff1d(np.unique(df['image_id']), X_test['image_id'])

    # Create a DataFrame for predictions
    predict_df = pd.DataFrame({'user_id': user_id, 'image_id': images_to_recommend, 'view_time_seconds': [100] * len(images_to_recommend)})

    # Predict probabilities
    probabilities = clf.predict_proba(predict_df)[:, 1]  # Get probability for the 'liked' class

    # Recommend images with the highest 'like' probability
    recommendations = images_to_recommend[np.argsort(-probabilities)]
    print(f"Recommended images for user {user_id}: {recommendations}")



def next(address) -> Ordinal:

    # train()

    print(f"Getting next ordinal for user {address}")

    # redis_url = os.getenv('REDIS_URL')
    # r = redis.Redis.from_url(redis_url)
    ordinals = db.get_ordinals()

    print(type(ordinals))

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
