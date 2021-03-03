from instabot import Bot
from pprint import pprint
import os
from dotenv import load_dotenv
import shutil
import json
import re
from time import sleep


def get_comments(bot, filename):
    media_id = bot.get_media_id_from_link("https://www.instagram.com/p/BtON034lPhu/")
    comments = bot.get_media_comments_all(media_id)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(comments, file)


def get_text_comment(file_path):
    text_comments = []
    with open(file_path, 'r') as f:
        comments_data = json.loads(f.read())
        for comments in comments_data:
            text_comments.append(comments['text'])
    return text_comments


def get_users(text_comments, regex):
    users = []
    for text in text_comments:
        result = re.findall(regex, text)
        users.append(result)
    return users


def is_user_exist(user_name, bot):
    media_id = bot.get_user_id_from_username(user_name)
    if media_id:
        return True
    else:
        return False


def get_bot(login, password):
    bot = Bot()
    bot.login(username=login, password=password)
    return bot


if __name__ == "__main__":
    load_dotenv()

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('ISTAGRAM_PASSWORD')
    bot = get_bot(login, password)
    # get_comments(bot)
    # with open("comments.json", "r") as my_file:
    #     file_contents = my_file.read()
    # print(file_contents)
    #
    regex = "(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
    comments_filename = 'comments.json'
    all_marked_users = 'users.json'

    text_comments = get_text_comment(comments_filename)
    marked_users = get_users(text_comments, regex)
    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')
    # shutil.rmtree(path)

    all_id = []
    for users in marked_users:
        for user_name in users:
            fake_user = is_user_exist(user_name, bot)
            print(fake_user)








