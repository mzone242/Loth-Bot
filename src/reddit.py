import praw
from configparser import ConfigParser

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

    return praw_params

params = praw_config()
reddit = praw.Reddit(client_id = params['client_id'],
                     client_secret = params['client_secret'],
                     username = params['username'],
                     password = params['password'],
                     user_agent = 'Windows:Loth-Bot:v0.1 (by /u/mzone242)')
print(reddit.user.me())
subreddit = reddit.subreddit('PrequelMemes')