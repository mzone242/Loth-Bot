import datetime
import logging

import prawcore

logger = logging.getLogger("utils.reddit")

subreddit = None
over_threshold = []


def load_subreddit(_subreddit):
    global subreddit
    subreddit = _subreddit
    return


def fetch_posts(_limit):
    try:
        logger.info(f"Fetching top {_limit} posts from {subreddit.display_name}")
        top = subreddit.top("day", limit=_limit)
        over_threshold.clear()
        count = 0
        total = 0
        time = int(datetime.datetime.now().timestamp())

        for post in top:
            if post is None:
                logger.info(f"None post encountered from praw")
                continue
            if not post.author:
                name = '[deleted]'
            else:
                name = post.author.name
            _post = (post.id, post.score, int(post.created_utc), False, name, post.url, post.title)
            total += 1
            if _post[1] >= 100 and time - _post[2] < 86400:
                over_threshold.append(_post)
                count += 1

        logger.info(f'{str(count)} posts found over 100 upvotes out of {str(total)} posts')
        logger.info(f'Current time is {time}')
    except prawcore.exceptions.ServerError as error:
        logger.info(error)
        return None
    return over_threshold
