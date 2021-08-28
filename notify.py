#! python3
import requests

def get_chat_ids(bot_api_key):
    url = "https://api.telegram.org/bot{}/getUpdates".format(bot_api_key)

    r = requests.get(url)
    data = r.json()
    chat_ids = []

    for result in data['result']:
        chat_ids.append(result['message']['from']['id'])

    return list(set(chat_ids))

def send_telegram_message(bot_api_key, chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_api_key)

    data = {'chat_id' : chat_id,
            'text'    : text}

    r = requests.post(url, data)

def send_telegram(bot_api_key,  text):
    ids = get_chat_ids(bot_api_key)
    for chat_id in ids:
        send_telegram_message(bot_api_key, chat_id, text)

