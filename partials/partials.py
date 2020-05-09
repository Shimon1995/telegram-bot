from pymongo import MongoClient


client = MongoClient('localhost', 27017)

collection = client['todo']['todo']


def resetIds():
    number = 1
    for todo in collection.find({}):
        collection.update_one(todo, {'$set': {'id': number}})
        number += 1
