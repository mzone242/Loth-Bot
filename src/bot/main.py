import logging

from src.utils import reddit
from src.utils import database


def scrape_reddit(limit):
    posts = reddit.fetch_posts(limit)
    return database.check_posts(posts)


def update_database(posts_to_add):
    database.insert_posts(posts_to_add)
    return database.update_posts()


def clean_database():
    database.remove_posts()
