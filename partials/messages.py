import requests
import time
from partials import todos
from dotenv import TOKEN


URL = f'https://api.telegram.org/bot{TOKEN}/'


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


def sendMessage(text):
    last_msg = getLastMsg()
    chat_id = last_msg['message']['from']['id']
    requests.get(
        URL + f'sendMessage?chat_id={chat_id}&text={text}&parse_mode=HTML&offset=100')


def switchMessage(message):
    if message == '/addtodo':
        sendMessage('Enter a todo content')
        message = getNewMsg(message)
        todos.addToDo(message)
        todos.listToDos()

    elif message == '/dotodo':
        sendMessage('Pick a todo')
        todo_content = getNewMsg(message)
        todos.getDoneToDo(todo_content)
        todos.listToDos()

    elif message == '/edittodo':
        sendMessage('Pick a todo')
        message = getNewMsg(message)
        todos.editToDo(message)
        todos.listToDos()

    elif message == '/undododo':
        sendMessage('Pick a todo')
        todo_content = getNewMsg(message)
        todos.getUndoneToDo(todo_content)
        todos.listToDos()

    elif message == '/removetodo':
        sendMessage('Pick a todo')
        message = getNewMsg(message)
        todos.removeToDo(message)
        todos.listToDos()

    elif message == '/listtodos':
        todos.listToDos()
