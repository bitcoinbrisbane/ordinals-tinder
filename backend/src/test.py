#!/usr/bin/python3
# Test script for mongo + pydantic
from models.index import Ordinal
import collaboration

import db

ordinals = db.get_ordinals()

ordinal = collaboration.get_random_ordinal()
print(ordinal)
print(type(ordinal))
