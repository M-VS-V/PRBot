#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import datetime
import random
import hashlib
import schedule
import time

Hash = hashlib.sha512
MAX_HASH_PLUS_ONE = 2**(Hash().digest_size * 8)

def str_to_probability(in_str):
    """Return a reproducible uniformly random float in the interval [0, 1) for the given string."""
    seed = in_str.encode()
    hash_digest = Hash(seed).digest()
    hash_int = int.from_bytes(hash_digest, 'big')  # Uses explicit byteorder for system-agnostic reproducibility
    return hash_int / MAX_HASH_PLUS_ONE  # Float division

def str_to_prob(in_str):
    return random.Random(in_str).random()

token = "533104134:AAGe7wFEMq0AfJX6D17Wm9gptIFOfwv79CU"
#"https://api.telegram.org/bot533104134:AAGe7wFEMq0AfJX6D17Wm9gptIFOfwv79CU/sendMessage?text=Пульцы&chat_id=-1001066118523" kartish
#https://api.telegram.org/bot533104134:AAGe7wFEMq0AfJX6D17Wm9gptIFOfwv79CU/sendMessage?text=ЗАчем&chat_id=-1001197750275 delo

DELO_CHAT_ID = -1001197750275

class BotHandler:

    def job(self, t):
        self.send_message(DELO_CHAT_ID, t)
        return

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        try:
            res = resp.json()
        except:
            res = {'result' : {}}
            print("exception")

        print("result = {} date = {}".format(str(res), datetime.datetime.now()))
        if 'result' in res:
            return res['result']

        return {}

    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
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
    'keri_kun': 'СанСаныч',
    'sanllier': 'Горемыка',
    'xtxtxtxtxt': 'МашинаБездушная',
    'yadgar0v': 'Кандёр',
    'trimonovds': 'RxПсина',
    'elrid': 'Слава',
    'likhogrud': 'Коля'
}

def sampleOwn(users, anyString):
    print()
    random.seed(anyString)
    random.shuffle(users)
    return random.sample(users, 3)


usersCount = len(usernames)
#https://api.telegram.org/bot533104134:AAGe7wFEMq0AfJX6D17Wm9gptIFOfwv79CU/sendMessage?chat_id=117947739&text="Как побегал"
def main():
    new_offset = None
    today = now.day
    hour = now.hour
    #schedule.every(1).seconds.do(greet_bot.job, '5 часов 123 минуты')
    schedule.every().day.at('18:00').do(greet_bot.job, '1 час до псарни')
    schedule.every().day.at('18:30').do(greet_bot.job, '30 мин до комнаты боли')
    schedule.every().day.at('19:00').do(greet_bot.job, 'Пора пиздовать на ревью')

    while True:
        schedule.run_pending()
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        print("new_offset={}".format(new_offset))
        if (last_update.get('update_id') is None
                or last_update.get('message') is None
                or last_update['message'].get('text') is None
                or last_update['message'].get('chat') is None
                or last_update['message']['chat'].get('id') is None):
            continue
        last_update_id = last_update['update_id']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_username = last_update['message']['chat'].get('username')
        text = last_update['message']['text']

        users = list(filter(lambda x: x != last_chat_username, usernames.keys()))
        print('last_chat_name = ' + str(last_chat_username))
        print('last_chat_id = ' + str(last_chat_id))
        print('users = ' + str(users))
        print('text = ' + str(text))

        # dic = {}
        # for i in range(10000):
        #     option1, option2, option3 = sampleOwn(users, str(i))
        #     if option1 in dic:
        #         dic[option1] += 1
        #     else:
        #         dic[option1] = 0
        #
        #     if option2 in dic:
        #         dic[option2] += 1
        #     else:
        #         dic[option2] = 0
        #
        #     if option3 in dic:
        #         dic[option3] += 1
        #     else:
        #         dic[option3] = 0
        #
        # for k,v in dic.items():
        #     print(k,v,sep= '_')

        option1, option2, option3 = sampleOwn(users, text)
        print(option1, option2, option3)

        if not str(last_chat_id).startswith('-'):
            greet_bot.send_message(DELO_CHAT_ID, "Были назначены '{}, {}, {}' на PR {} от {}\n".format(usernames[option1], usernames[option2], usernames[option3], text, last_chat_username))
            greet_bot.send_message(last_chat_id, "{}, {}, {}\n".format(usernames[option1],usernames[option2],usernames[option3]))


        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
