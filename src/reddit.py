import praw
import datetime
from configparser import ConfigParser

reddit = None
subreddit = None
over_threshold = []


def praw_config(filename='reddit.ini', section='Loth-Bot'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    praw_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            praw_params[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    reddit = praw.Reddit(client_id=praw_params['client_id'],
                         client_secret=praw_params['client_secret'],
                         username=praw_params['username'],
                         password=praw_params['password'],
                         user_agent='Windows:Loth-Bot:v0.1 (by /u/mzone123)')
    subreddit = reddit.subreddit('PrequelMemes')
    return


def fetch_posts(_limit):
    if subreddit is None:
        praw_config()
    new = subreddit.new(limit=_limit)
    seconds_since_epoch = int(datetime.datetime.now().timestamp())
    count = 0
    for post in new:
        _post = (post.id, post.score, int(post.created))
        if seconds_since_epoch - _post[2] > 86400:
            break
        if _post[1] >= 100:
            over_threshold.append(_post)
            count += 1
    print(count)
    print(seconds_since_epoch)
    return over_threshold


if __name__ == '__main__':
    praw_config()
