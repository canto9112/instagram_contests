from instabot import Bot
from pprint import pprint
import os
from dotenv import load_dotenv
import shutil
import json


def get_comments(login, password):
    bot = Bot()
    bot.login(username=login, password=password)
    media_id = bot.get_media_id_from_link("https://www.instagram.com/p/BtON034lPhu/")
    comments = bot.get_media_comments_all(media_id)
    with open("comments.json", "w", encoding="utf-8") as file:
        json.dump(comments, file)


def get_text_comment(file_path):
    with open(file_path, 'r') as f:
        comments_data = json.loads(f.read())
        for comments in comments_data:
            print(comments['text'])


if __name__ == "__main__":
    load_dotenv()

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('ISTAGRAM_PASSWORD')
    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')
    # shutil.rmtree(path)

    # get_comments(login, password)
    # with open("comments.json", "r") as my_file:
    #     file_contents = my_file.read()
    # print(file_contents)
    #
    path = 'comments.json'
    get_text_comment(path)


