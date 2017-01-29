# coding: utf-8
import argparse
import logging
import os
import json
import requests
from telegram.ext import Updater
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Check():
    def __init__(self, authToken, url, chatId):
        self.lastContent = ""
        self.filePath = os.path.dirname(os.path.realpath(__file__)) + "\cache"
        self.authToken = authToken
        self.url = url
        self.chatId = chatId

    def cacheContainsId(self, id, cache):
        for j in cache['nodes']:
            if j['id'] == id:
                return True
        return False

    def run(self):
        while True:
            if not os.path.isfile(self.filePath) or os.path.getsize(self.filePath) == 0:
                with open(self.filePath, "w") as file:
                    self.lastContent = json.loads(requests.get(self.url).text)
                    json.dump(self.lastContent, file)
            else:
                with open(self.filePath, "r") as file:
                    self.lastContent = json.load(file)

            r = requests.get(self.url)
            js = json.loads(r.text)

            if self.lastContent['nodes'] != js['nodes']:
                updater = Updater(self.authToken)
                for i in js['nodes']:
                    isNew = self.cacheContainsId(i['id'], self.lastContent)
                    if not isNew:
                        updater.bot.sendMessage(chat_id=self.chatId,
                                                text="Neuer Knoten <a href=\"https://map.freifunk-hennef.de/#!v:m;n:{}\"\
                                                >{}</a>".format(i['id'], i['name']), parse_mode="html")

            self.lastContent = js

            with open(self.filePath, "w") as file:
                json.dump(self.lastContent, file)

            logging.info("Sleeping 60s")
            sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Überprüft eine JSON-Datei nach Änderungen")
    parser.add_argument("-token", type=str, required=True, help="Authtoken für den Telegram Bot")
    parser.add_argument("-url", type=str, required=True, help="Netzwerkpfad zur JSON-Datei")
    parser.add_argument("-chat", type=int, required=True,
                        help="Telegram Chat-ID an die die Benachrichtigung gesendet werden soll")
    parsed_args = parser.parse_args()

    if not parsed_args.token:
        parser.print_help()
        exit()

    Check(parsed_args.token, parsed_args.url, parsed_args.chat).run()
