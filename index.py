import requests
import time
from dotenv import TOKEN

URL = f'https://api.telegram.org/bot{TOKEN}/'


todos = [{
    'content': 'Something something something something',
    'done': False,
},
    {
    'content': 'Something else',
    'done': True,
}]

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

    elif message == '/removedodo':
        sendMessage('Pick a todo')
        message = getNewMsg(message)
        removeToDo(message)
        listToDos()

    elif message == '/listtodos':
        listToDos()

    # else:
    #     sendMessage('IDK, what you wnat from me')

# Managing ToDos


def addToDo(content):
    todo = {
        'content': content,
        'done': False,
    }
    todos.append(todo)


def getDoneToDo(content):
    for todo in todos:
        if todo['content'] == content:
            todo['done'] = True


def getUndoneToDo(content):
    for todo in todos:
        if todo['content'] == content:
            todo['done'] = False


def removeToDo(content):
    for todo in todos:
        if todo['content'] == content:
            todos.remove(todo)


def listToDos():
    message = ''
    for todo in todos:
        done = 'has been done' if todo['done'] == True else 'undone yet'
        message += f"<code>{todo['content']}</code> | <i>{done}</i>;\n"
    sendMessage(message)

# partials


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
