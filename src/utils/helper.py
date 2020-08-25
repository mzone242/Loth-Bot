import logging
import datetime
import sys

from src.utils import reddit
from src.utils import database

logger = logging.getLogger('utils.helper')


def setup_logger(name, debug):
    logger = logging.getLogger(name)
    d = datetime.datetime.now()
    time = f"{d.month}-{d.day}_{d.hour}h{d.minute}m"

    if sys.platform == 'linux':
        filename = '/home/rick/logs/{}.log'
    else:
        filename = './logs/{}.log'
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    file_handler = logging.FileHandler(filename.format(time))
    # file_handler.setLevel(level)

    stream_handler = logging.StreamHandler(sys.stdout)
    # stream_handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
    return logger


def config():
    database.config()


def praw_config(version):
    reddit.pass_version(version)
    reddit.praw_config()


def scrape_reddit(limit):
    posts = reddit.fetch_posts(limit)
    return database.update_scores(posts)


def update_database(posts_to_add):
    database.insert_posts(posts_to_add)
    return database.update_posts()


def clean_database():
    database.remove_posts()
