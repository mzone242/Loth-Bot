import praw
import datetime
import logging
from configparser import ConfigParser

logger = logging.getLogger("utils.reddit")

reddit = None
subreddit = None
user_agent = None
over_threshold = []
SUBREDDIT = 'PrequelMemes'


def pass_version(version):
    global user_agent
    user_agent = 'Windows:Loth-Bot:' + version + ' (by /u/mzone123)'


def praw_config(filename='src/utils/reddit.ini', section='Loth-Bot'):
    parser = ConfigParser()
    parser.read(filename)
    praw_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            praw_params[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    global reddit
    reddit = praw.Reddit(client_id=praw_params['client_id'],
                         client_secret=praw_params['client_secret'],
                         username=praw_params['username'],
                         password=praw_params['password'],
                         user_agent=user_agent)
    global subreddit
    subreddit = reddit.subreddit(SUBREDDIT)
    return


def fetch_posts(_limit):
    global subreddit
    if subreddit is None:
        if reddit is None:
            praw_config()
        else:
            subreddit = reddit.subreddit(SUBREDDIT)
    new = subreddit.new(limit=_limit)
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


if __name__ == '__main__':
    praw_config()
