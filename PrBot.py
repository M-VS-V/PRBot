#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import datetime
import random

from time import sleep

token = "533104134:AAGe7wFEMq0AfJX6D17Wm9gptIFOfwv79CU"

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = {}

        return last_update

greet_bot = BotHandler(token)
greetings = ('Здоров братиш, есть че посмотреть?',
             'Часик в радость, чефир в сладость',
             'ку',
             'здорово',
             'Доброе утро')

now = datetime.datetime.now()
usernames = {
    'artkirillov': 'Артем',
    'gorem': 'Саша',
    'keri_kun': 'Саня',
    'xtxtxtxtxt': 'Сева',
    'yadgar0v': 'Искандер',
    'trimonovds': 'Дима',
    'elrid': 'Слава'
}

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if (last_update.get('update_id') is None
                or last_update.get('message') is None
                or last_update['message'].get('chat') is None
                or last_update['message']['chat'].get('id') is None):
            continue

        last_update_id = last_update['update_id']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['username']

        users = list(filter(lambda x: x != last_chat_name, usernames.keys()))
        print(last_chat_name)
        print(users)
        option1, option2 = random.sample(users, 2)

        greet_bot.send_message(last_chat_id, "{}, {}\n".format(usernames[option1],usernames[option2]))

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()