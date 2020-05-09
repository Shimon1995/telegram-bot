import time
from partials import messages


def main(last):
    while True:
        result = messages.getLastMsg()
        chat_id = result['message']['chat']['id']
        if last != result:
            last = result
            messages.switchMessage(result['message']['text'])
        time.sleep(1)


main('')
