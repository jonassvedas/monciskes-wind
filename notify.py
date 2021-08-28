#! python3
import requests

def send_telegram(bot_api_key, chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_api_key)

    data = {'chat_id' : chat_id,
            'text'    : text}

    r = requests.post(url, data)
