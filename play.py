from pymongo import MongoClient

client = MongoClient('localhost', 27017)

collection = client['todo']['todo']

# result = collection.find_one(
# {'$or': [{'content': 'do something special'}, {'id': 100}]})

# result = collection.update_one({'id': 1}, {'$set': {'content': 'something'}})

# print(result)


def trying(content):
    try:
        content = int(content)
    except:
        content = content


# def getDoneToDo(content):
#     trying(content)
#     collection.delete_one({'$or': [{'content': content}, {'id': content}]})


# getDoneToDo('something')


def resetIds():
    number = 1
    for todo in collection.find({}):
        collection.update_one(todo, {'$set': {'id': number}})
        number += 1


resetIds()
