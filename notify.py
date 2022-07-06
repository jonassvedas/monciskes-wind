#! python3
import requests
import os
import json

db_file = "chat_ids_db.json"

def get_chat_ids_from_db():
    if (os.path.isfile(db_file)):
        f = open(db_file)
        data = json.load(f)
        f.close()
        return data
    else:
        return []

def save_chat_ids_to_db(chat_ids):
    print("Saving ids:")
    print(chat_ids)
    f = open(db_file, "w")
    json.dump(chat_ids, f)
    f.close()

def get_bot_updates(bot_api_key):
    url = "https://api.telegram.org/bot{}/getUpdates".format(bot_api_key)
    r = requests.get(url)
    return r.json()

def get_chat_ids(bot_api_key):

    chat_ids = get_chat_ids_from_db()
    data = get_bot_updates(bot_api_key)

    for result in data['result']:
        try:
            chat_ids.append(result['message']['from']['id'])
        except:
            print("Exeption occured during json parsing probably key error.")

    no_duplicates_ids = list(set(chat_ids))

    return no_duplicates_ids

def send_telegram_message(bot_api_key, chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_api_key)

    data = {'chat_id' : chat_id,
            'text'    : text}

    r = requests.post(url, data)

def send_telegram(bot_api_key,text, chat_ids):
    for chat_id in chat_ids:
        send_telegram_message(bot_api_key, chat_id, text)


