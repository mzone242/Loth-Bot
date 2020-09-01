import asyncio
import logging
import random

import discord
from discord.ext import tasks, commands

from src.utils import helper

logger = logging.getLogger("bot")

VERSION = "v1.0.0"
CHANNEL = 455483961490276353
NOT_SHIT = 725127435737367054
MEH_SHIT = 714410477236519001
SUBREDDIT = 'PrequelMemes'


class Loth(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="%")
        self.version = VERSION
        self.channel = CHANNEL
        self.channel2 = CHANNEL
        self.subreddit = SUBREDDIT

    def run(self, token):
        logger.info("Run method called.")
        helper.load_db_creds()
        helper.load_reddit_creds(self.version, self.subreddit)
        super().run(token, reconnect=True)

    async def on_ready(self):
        self.routine.start()
        logger.info("Logged in as {0.user}.".format(self))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("check_sub"):
            await self.check_sub()

    @tasks.loop(minutes=5)
    async def routine(self):
        await self.check_sub()
        logger.info("Routine sleeping...")

    async def check_sub(self):
        logger.info("Checking sub")
        posts = helper.scrape_reddit(200)
        if posts is not None:
            await self.send_embed(posts, 100, self.channel2)
            await self.send_embed(helper.update_database(posts), 1000, self.channel)
            helper.clean_database()

    async def send_embed(self, posts, upvotes, _channel):
        logger.info(f"Sending {len(posts)} to {_channel}.")
        channel = self.get_channel(_channel)

        for post in posts:
            print(post[5])
            if post is None:
                logger.info(f"None post encountered. Please check {posts}")
                continue

            embed = discord.Embed(title=f"This post has over {upvotes} upvotes. Please check it out.",
                                  description="Please react with :white_check_mark: if you checked the post and it is "
                                              "good and please react with :x: if you checked the post and removed it.")
            embed.add_field(name=f"{post[6][:255]}", value=f"https://www.reddit.com/r/PrequelMemes/comments/{post[0]}")
            embed.set_author(name=post[4], url=f"https://www.reddit.com/u/{post[4]}")
            embed.set_image(url=post[5])

            msg = await channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            await asyncio.sleep(1)

    @property
    def exit_code(self):
        return self._exit_code
