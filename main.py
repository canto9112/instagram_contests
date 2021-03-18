import argparse
import os
import random
import re
import shutil
from pathlib import Path

from dotenv import load_dotenv
from instabot import Bot


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


def get_media_likers(bot, post_link):
    media_id = bot.get_media_id_from_link(post_link)
    return bot.get_media_likers(media_id)


def get_users_who_markeds(bot, comments, regex):
    comment_condition = []

    comments_data = get_comment_text(comments)
    for comment in comments_data:
        text = comment['text']
        id = comment['user_id']
        marked_users = get_marked_users(text, regex)
        for user in marked_users:
            real_user = is_user_exist(user, bot)
            if real_user:
                comment_condition.append(str(id))
    return comment_condition


def get_users_followers(bot, username):
    return bot.get_user_followers(username)


def get_username(bot, id):
    return bot.get_username_from_user_id(id)


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

    bot = get_bot(login, password)
    comments = get_comments(bot, post_link)

    markeds = set(get_users_who_markeds(bot, comments, regex))
    likers = set(get_media_likers(bot, post_link))
    followers = set(get_users_followers(bot, organizers_account))

    unic_users = markeds & likers & followers
    winners_ids = random.choice(list(unic_users))
    winner_username = get_username(bot, winners_ids)
    print('Выйграл участник с именем -', winner_username)


if __name__ == "__main__":
    main()









