import logging
import datetime

from src.utils import reddit
from src.utils import database

logger = logging.getLogger(__name__)
filename = '../logs/{}.log'
handler = logging.FileHandler(filename.format(str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h', 1).replace(':', 'm').split('.')[0][:-2]))
formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

logger.info("Starting \"Loth-Bot\" bot script!")
#_pfx = ["~", "?", "-"]
#bot = commands.Bot(command_prefix=_pfx)
#bot.help_command = commands.MinimalHelpCommand()
# bot.remove_command('help')
version = "v0.1.2"

START_TIME = datetime.datetime.now()
STARTED = False


limit = 1

print('Step 1')
posts = reddit.fetch_posts(limit)
print('Step 2')
posts_to_add = database.check_posts(posts)
if posts_to_add is not None:
    for post in posts_to_add:
        print('This post has over 100 upvotes: https://www.reddit.com/r/PrequelMemes/comments/' + post[0])
#print(posts_to_add)
print('Step 3')
database.insert_posts(posts_to_add)
over_1000 = database.update_posts()
if over_1000 is not None:
    for post in over_1000:
        print('This post has over 1000 upvotes: https://www.reddit.com/r/PrequelMemes/comments/' + post[0])

