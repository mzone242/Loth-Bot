import praw
import logging
import datetime
import sys
from configparser import ConfigParser

from src.utils import reddit
from src.utils import database

logger = logging.getLogger('utils.helper')


def setup_logger(name, debug):
    logger = logging.getLogger(name)
    d = datetime.datetime.now()
    time = f"{d.month}-{d.day}_{d.hour}h{d.minute}m"

    if sys.platform == 'linux':
        filename = '/home/mzone242/Loth-Bot/logs/{}.log'
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


def load_db_creds(filename='src/utils/database.ini', section='postgresql'):
    logger.info('Configuring db')
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    database.load_db(db)
    return


def load_reddit_creds(version, subreddit, filename='src/utils/reddit.ini', section='Loth_Bot'):
    logger.info('Configuring praw')
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        client_id = parser.get(section, 'client_id')
        client_secret = parser.get(section, 'client_secret')
        username = parser.get(section, 'username')
        password = parser.get(section, 'password')
    else:
        logger.error('Section {0} not found in the {1} file'.format(section, filename))

    _reddit = praw.Reddit(client_id=client_id,
                          client_secret=client_secret,
                          username=username,
                          password=password,
                          user_agent=sys.platform + ':Loth-Bot:' + version + ' (by /u/mzone123)')
    reddit.load_subreddit(_reddit.subreddit(subreddit))
    return


def scrape_reddit(limit):
    posts = reddit.fetch_posts(limit)
    return database.update_scores(posts)


def update_database(posts_to_add):
    database.insert_posts(posts_to_add)
    return database.update_posts()


def clean_database():
    database.remove_posts()
