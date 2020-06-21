from pymongo import MongoClient
from environment import MONGO_CLIENT


client = MongoClient(MONGO_CLIENT)

collection = client['todo']['todo']


def resetIds():
    number = 1
    for todo in collection.find({}):
        collection.update_one(todo, {'$set': {'id': number}})
        number += 1
