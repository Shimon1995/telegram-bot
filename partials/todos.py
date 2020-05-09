from partials import messages, partials


def trying(content):
    try:
        content = int(content)
    except:
        content = content


def addToDo(content):
    todos = []
    for todo in partials.collection.find({}):
        todos.append(todo)
    index = todos[-1]['id'] + 1
    todo = {
        'id': index,
        'content': content,
        'done': False,
    }
    partials.collection.insert_one(todo)


def getDoneToDo(content):
    trying(content)
    partials.collection.update_one({'$or': [{'id': content}, {'content': content}]}, {
        '$set': {'done': True}})


def getUndoneToDo(content):
    trying(content)
    partials.collection.update_one({'$or': [{'id': content}, {'content': content}]}, {
        '$set': {'done': False}})


def removeToDo(content):
    partials.collection.delete_one(
        {'$or': [{'content': content}, {'id': content}]})


def listToDos():
    message = ''
    for todo in partials.collection.find({}):
        done = 'has been done' if todo['done'] else 'undone yet'
        message += f"{todo['id']}) <code>{todo['content']}</code> | <i>{done}</i>;\n"
    messages.sendMessage(message)
