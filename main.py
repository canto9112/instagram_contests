import argparse
import os
import random
import re
import shutil
from pathlib import Path

from dotenv import load_dotenv
from instabot import Bot


def get_comments(post_link, login, password):
    bot = Bot()
    bot.login(username=login, password=password)
    media_id = bot.get_media_id_from_link(post_link)
    comments = bot.get_media_comments_all(media_id)
    return bot, comments


def get_comments_data(comments):
    comments_data = []
    for comment in comments:
        text = comment['text']
        user_id = comment['user_id']
        username = comment['user']['username']
        comments_data.append({'text': text,
                              'user_id': user_id,
                              "username": username})
    return comments_data


def fetch_real_user(user_name, bot):
    return bot.get_user_id_from_username(user_name)


def get_likers_ids(bot, post_link):
    media_ids = bot.get_media_id_from_link(post_link)
    return bot.get_media_likers(media_ids)


def get_users_who_markeds(bot, comments, regex):
    comment_condition = []

    comments_data = get_comments_data(comments)
    for comment in comments_data:
        text = comment['text']
        id = comment['user_id']
        marked_users = re.findall(regex, text)
        for user in marked_users:
            real_user = fetch_real_user(user, bot)
            if real_user:
                comment_condition.append(str(id))
    return comment_condition


def get_args():
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('link', help='Ссылка на пост с розыгрышем')
    parser.add_argument('account', help='Аккаунт организатора')
    args = parser.parse_args()
    return args.link, args.account


def main():
    load_dotenv()

    instabot_config = Path('config')
    if instabot_config.exists():
        shutil.rmtree(instabot_config)

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('ISTAGRAM_PASSWORD')
    # Регулярное выражение для определения отмеченных пользователей
    regex = "(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"

    post_link, organizers_account = get_args()

    bot, comments = get_comments(post_link, login, password)

    markeds = set(get_users_who_markeds(bot, comments, regex))
    likers_ids = set(get_likers_ids(bot, post_link))
    followers = set(bot.get_user_followers(organizers_account))

    unic_users = markeds & likers_ids & followers
    winner_id = random.choice(list(unic_users))
    winner_username = bot.get_username_from_user_id(winner_id)
    print('Выйграл участник с именем -', winner_username)


if __name__ == "__main__":
    main()
