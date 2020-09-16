This bot regularly scans Reddit and uploads posts that are over a certain threshold to Discord channels for moderation purposes.

It is currently intended for personal use, so the subreddit and Discord channels are hardcoded, but I am in the process of making it scalable. However, due to praw API limits, this is likely only scalable to a few subs.

To Do List:
- Add post removal via Discord
- Integrate taskerbot functionality
- Refactor bot and move to cogs
- Move from PostgreSQL database to local caching (can still store data in db afterwards for statistical purposes)
- Add modqueue
- Modmail?
