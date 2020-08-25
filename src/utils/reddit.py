import praw
import datetime
import logging
from configparser import ConfigParser

logger = logging.getLogger("utils.reddit")

subreddit = None
over_threshold = []


def load_subreddit(_subreddit):
    global subreddit
    subreddit = _subreddit
    return


def fetch_posts(_limit):
    new = subreddit.new(limit=_limit)
    top = subreddit.top("day", limit=200)
    # ideally get rid of this variable and rework algorithm below to searching top 200 last 24 hours
    time = int(datetime.datetime.now().timestamp())
    over_threshold.clear()
    count = 0
    total = 0

    for post in new:
        if post is None:
            logger.info(f"None post encountered from praw")
            continue
        if not post.author:
            name = '[deleted]'
        else:
            name = post.author.name
        _post = (post.id, post.score, int(post.created_utc), False, name, post.url, post.title)
        if time - _post[2] > 86400:
            # print('broke')
            break
        total += 1
        if _post[1] >= 100:
            over_threshold.append(_post)
            count += 1

    logger.info(f'{str(count)} posts found over 100 upvotes out of {str(total)} posts')
    logger.info(f'Current time is {time}')
    return over_threshold
