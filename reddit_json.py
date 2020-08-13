import urllib.request, json

def fetch_json(file):

    over_threshold = []
    subreddit = 'PrequelMemes'
    new_url = 'https://www.reddit.com/r/' + subreddit + '/new.json?limit=100&after='

    # with urllib.request.urlopen('https://www.reddit.com/r/equelmemes/new.json?limit=100') as url:
    with open(file, 'r') as read_file:
        data = json.load(read_file)
        # data = json.loads(url.read().decode())
        page = data['data']['children']
        for post in page:
            post_data = post['data']
            _post = (post_data['id'], post_data['score'], int(post_data['created']))
            if _post[1] >= 100:
                over_threshold.append(_post)
        next_page = page[-1]['data']['id']
        print(next_page)
        print(over_threshold)
        print(len(over_threshold))
    return over_threshold

if __name__ == '__main__':
    fetch_json('equelmemes.json')