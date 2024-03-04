#!/usr/bin/python3
# Test script for mongo + pydantic
from models.index import Ordinal
import collaboration

import db

test_db = False
test_pydantic = True

if test_db:
    ordinals = db.get_ordinals()

    ordinal = collaboration.get_random_ordinal()
    print(ordinal)
    print(type(ordinal))


# if test_pydantic:
#     ordinal = Ordinal(id="123", number=1, address="1", content_url="http://localhost:8000/image/123", content_type="image/png")
#     print(ordinal)
#     print(type(ordinal))
    

db.load_seed_ordinals()