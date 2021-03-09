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
    comments_data = []
    for comment in comments:
        text = comment['text']
        user_id = comment['user_id']
        username = comment['user']['username']
        comments_data.append({'text': text,
                              'user_id': user_id,
                              "username": username})
    return comments_data


def get_marked_users(text_comment, regex):
    result = re.findall(regex, text_comment)
    return result


def is_user_exist(user_name, bot):
    media_id = bot.get_user_id_from_username(user_name)
    if media_id:
        return True
    else:
        return False


def is_user_like_post(bot):
    media_id = bot.get_media_id_from_link("https://www.instagram.com/p/BtON034lPhu/")
    media_likers = bot.get_media_likers(media_id)
    return media_likers


if __name__ == "__main__":
    load_dotenv()

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')
    shutil.rmtree(path)

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('ISTAGRAM_PASSWORD')
    regex = "(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
    bot = get_bot(login, password)
    comments = get_comments(bot)

    likers = is_user_like_post(bot)

    socessfuly_comments = []
    comments_data = get_comment_text(comments)
    for comment in comments_data:
        text = comment['text']
        id = comment['user_id']
        username = comment['username']
        marked_users = get_marked_users(text, regex)
        for user in marked_users:
            real_user = is_user_exist(user, bot)
            if real_user and user in likers:
                socessfuly_comments.append((id, username))
                print(id, 'Добавлен')









