import requests
import time
from dotenv import TOKEN
from pymongo import MongoClient

URL = f'https://api.telegram.org/bot{TOKEN}/'


client = MongoClient('localhost', 27017)

collection = client['todo']['todo']


# Messages


def getLastMsg():
    res = requests.get(URL + 'getUpdates')
    result = res.json()
    result = result['result']
    return result[-1]


def getNewMsg(old_msg):
    while True:
        new_msg = getLastMsg()
        new_msg = new_msg['message']['text']
        if new_msg != old_msg:
            return new_msg
        time.sleep(1)


def sendMessage(text, chat_id=685763684):
    requests.get(
        URL + f'sendMessage?chat_id={chat_id}&text={text}&parse_mode=HTML')


def switchMessage(message):
    if message == '/addtodo':
        sendMessage('Enter a todo content')
        message = getNewMsg(message)
        addToDo(message)
        listToDos()

    elif message == '/dotodo':
        sendMessage('Pick a todo')
        todo_content = getNewMsg(message)
        getDoneToDo(todo_content)
        listToDos()

    elif message == '/undododo':
        sendMessage('Pick a todo')
        todo_content = getNewMsg(message)
        getUndoneToDo(todo_content)
        listToDos()

    elif message == '/removetodo':
        sendMessage('Pick a todo')
        message = getNewMsg(message)
        removeToDo(message)
        listToDos()

    elif message == '/listtodos':
        listToDos()


# Managing ToDos

def trying(content):
    try:
        content = int(content)
    except:
        content = content


def addToDo(content):
    todos = []
    for todo in collection.find({}):
        todos.append(todo)
    index = todos[-1]['id'] + 1
    todo = {
        'id': index,
        'content': content,
        'done': False,
    }
    collection.insert_one(todo)


def getDoneToDo(content):
    trying(content)
    collection.update_one({'$or': [{'id': content}, {'content': content}]}, {
                          '$set': {'done': True}})


def getUndoneToDo(content):
    trying(content)
    collection.update_one({'$or': [{'id': content}, {'content': content}]}, {
                          '$set': {'done': False}})


def removeToDo(content):
    collection.delete_one({'$or': [{'content': content}, {'id': content}]})


def listToDos():
    message = ''
    for todo in collection.find({}):
        done = 'has been done' if todo['done'] == True else 'undone yet'
        message += f"{todo['id']}) <code>{todo['content']}</code> | <i>{done}</i>;\n"
    sendMessage(message)

# partials


def resetIds():
    number = 1
    for todo in collection.find({}):
        collection.update_one(todo, {'$set': {'id': number}})
        number += 1

# Main


def main(last):
    while True:
        result = getLastMsg()
        chat_id = result['message']['chat']['id']
        if last != result:
            last = result
            switchMessage(result['message']['text'])
        time.sleep(1)


main('')
