#!/usr/bin/python3

import collaboration
import db
import random

from dtos.index import Feedback

users = ["bc1qq2ye3ljqvpz6wgp8r24ede3jhmwxzf27fas2kheyt",
         "bc1qq2dn8wgnynadcgesjnd75eqgmdmzuuqpt3sc36zqy", 
         "bc1qq2rh2nvzwgf0jw5evnycy7rrrsya9j9k6asscqt23"]

for x in range(len(users)):

    user = users[x]

    for y in range(10):
        ordinal = collaboration.next(user)
        print(f"Ordinal: {ordinal} for user {user}")

        # generate random number
        i = random.randint(1, 1000)
        liked = random.choice([True, False])

        feedback = Feedback(
            id=ordinal['id'], user=user, liked=liked, time_stamp=0, time_spent=i)
        print(feedback)
        db.insert_feedback(feedback)
