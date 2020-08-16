import praw
import datetime
from configparser import ConfigParser

reddit = None
subreddit = None
over_threshold = []


def praw_config(filename='src/utils/reddit.ini', section='Loth-Bot'):
    #print('Reddit config')
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
                         user_agent='Windows:Loth-Bot:v0.1.3 (by /u/mzone123)')
    global subreddit
    subreddit = reddit.subreddit('PrequelMemes')
    #print(subreddit)
    return


def fetch_posts(_limit):
    if subreddit is None:
        praw_config()
    #print(subreddit)
    new = subreddit.new(limit=_limit)
    time = int(datetime.datetime.now().timestamp())
    over_threshold.clear()
    count = 0
    total = 0
    for post in new:
        _post = (post.id, post.score, int(post.created_utc), False, post.author.name, post.url, post.title)
        if time - _post[2] > 86400:
            #print('broke')
            break
        total += 1
        if _post[1] >= 100:
            over_threshold.append(_post)
            count += 1
    print(str(count) + ' posts found over 100 upvotes out of ' + str(total) + ' posts')
    print(time)
    return over_threshold


if __name__ == '__main__':
    praw_config()
