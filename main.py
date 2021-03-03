from instabot import Bot
from pprint import pprint
import os
from dotenv import load_dotenv
import shutil
import json
import re
from time import sleep


def get_bot(login, password):
    bot = Bot()
    bot.login(username=login, password=password)
    return bot


def get_comments(bot):
    media_id = bot.get_media_id_from_link("https://www.instagram.com/p/BtON034lPhu/")
    comments = bot.get_media_comments_all(media_id)
    return comments


def get_comment_text(comments):
    users_id = []
    usernames = []
    texts = []
    for comment in comments:
        text = comment['text']
        user_id = comment['user_id']
        username = comment['user']['username']
        users_id.append(user_id)
        usernames.append(username)
        texts.append(text)
    return users_id, usernames, texts


def get_marked_users(text_comment, regex):
    users = []
    for text in text_comment:
        result = re.findall(regex, text)
        users.append(result)
    return users


def is_user_exist(user_name, bot):
    media_id = bot.get_user_id_from_username(user_name)
    if media_id:
        return True
    else:
        return False


if __name__ == "__main__":
    load_dotenv()

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')
    shutil.rmtree(path)

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('ISTAGRAM_PASSWORD')
    regex = "(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
    bot = get_bot(login, password)
    comments = get_comments(bot)
    user_ids, usernames, texts = get_comment_text(comments)
    marked_users = get_marked_users(texts, regex)

    for users in marked_users:
        for user_name in users:
            real_user = is_user_exist(user_name, bot)
            print(real_user)








