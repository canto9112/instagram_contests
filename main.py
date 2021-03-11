from instabot import Bot
from pprint import pprint
import os
from dotenv import load_dotenv
import shutil
import json
import re
from time import sleep
from itertools import groupby


def get_bot(login, password):
    bot = Bot()
    bot.login(username=login, password=password)
    return bot


def get_comments(bot, post_link):
    media_id = bot.get_media_id_from_link(post_link)
    return bot.get_media_comments_all(media_id)


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


def fulfilled_conditions_like(bot, post_link):
    media_id = bot.get_media_id_from_link(post_link)
    return bot.get_media_likers(media_id)


def fulfilled_conditions_comment(bot, comments, regex):
    comment_condition = []

    comments_data = get_comment_text(comments)
    for comment in comments_data:
        text = comment['text']
        id = comment['user_id']
        username = comment['username']
        marked_users = get_marked_users(text, regex)
        for user in marked_users:
            real_user = is_user_exist(user, bot)
            if real_user:
                comment_condition.extend((id, username))
    return comment_condition


def fulfilled_conditions_follower(bot, username):
    return bot.get_user_followers(username)


if __name__ == "__main__":
    load_dotenv()

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')
    shutil.rmtree(path)

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('ISTAGRAM_PASSWORD')
    regex = "(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
    like_condition_file = 'likers2.json'
    comment_condition_file = 'comment_condition.json'
    followers_condition_file = 'followers.json'
    organizers_account = 'wowbeautybar.ru'
    post_link = "https://www.instagram.com/p/BtON034lPhu/"
    #
    bot = get_bot(login, password)
    comments = get_comments(bot, post_link)

    fulfilled_conditions_like(bot, post_link)
    fulfilled_conditions_comment(bot, comments, regex)
    fulfilled_conditions_follower(bot, organizers_account)

