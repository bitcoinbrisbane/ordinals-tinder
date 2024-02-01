from src.backend.db import OrdinalMetaData


def suggest(address):
    data = OrdinalMetaData(image=address, label=0)
    return data
