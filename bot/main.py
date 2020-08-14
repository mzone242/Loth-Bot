from src import reddit
from src import database
from src import config

limit = 1000

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

