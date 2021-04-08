import requests
import datetime as dt
import random
import os
from dotenv import load_dotenv

have_words = False
words = []
word_count = 0

config = {}

def changeStatus(word):
    print("[Log] Changing to :", word)

    status = "Siri, one word : `%s`" % word.title()

    requests.patch(
        'https://discord.com/api/v8/users/@me/settings',
        json = {
            "custom_status": {
                "text": status
            }
        },
        headers = {
            "origin": "https://discord.com",
            "referer": os.environ.get("PROFILE_REFERER"),
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "authorization": os.environ.get("PROFILE_TOKEN"),
            "Content-Type": "application/json"
        }
    )

    print("[Log] Changed! :", status)

def randomWord():
    global have_words, words, word_count
    if(not have_words):
        ### read for words
        file = open("words.txt", "r")

        words = file.read().split('\n')
        word_count = len(words)

        file.close()

        have_words = True
        ###

    return words[random.randrange(word_count)]

def main():

    # loading config
    global config
    load_dotenv()
    config = {
        "token" : "",
        "referer" : ""
    }
    ###

    nextChange = dt.datetime.now() + dt.timedelta(hours = 1, minutes = random.randrange(1, 10), seconds = random.randrange(1, 30))
    changeStatus(randomWord())
    print("[Timer] NextChange is at ", end="")
    print(nextChange)

    while True:

        if(dt.datetime.now() > nextChange):
            nextChange = dt.datetime.now() + dt.timedelta(hours = 1, minutes = random.randrange(1, 6), seconds = random.randrange(1, 30))
            changeStatus(randomWord())

            print("[Timer] NextChange is at ", end="")
            print(nextChange)

if __name__ == "__main__":
    main()
