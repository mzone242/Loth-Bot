import asyncio
import logging

import discord
from discord.ext import tasks, commands

from src.bot import main

logger = logging.getLogger("bot")

VERSION = "0.2.0"
CHANNEL = 455483961490276353
NOT_SHIT = 725127435737367054
MEH_SHIT = 714410477236519001


class Loth(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="%")
        self.exit_code = 0
        self.version = VERSION
        self.channel = NOT_SHIT
        self.channel2 = MEH_SHIT

    def run(self, token):
        super().run(token, reconnect=True)

    async def on_ready(self):
        self.routine.start()
        logger.info("Logged in as {0.user}.".format(self))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("check_sub"):
        if message.content.startswith("check_sub"):
            await self.check_sub()

    @tasks.loop(minutes=5)
    async def routine(self):
        await self.check_sub()

    async def check_sub(self):
        logger.info("Checking sub")
        posts = main.scrape_reddit(1000)
        await self.send_embed(posts, 100, self.channel2)
        _posts = main.update_database(posts)
        await self.send_embed(_posts, 1000, self.channel)
        main.clean_database()

    async def send_embed(self, posts, upvotes, _channel):
        logger.info(f"Sending {len(posts)} to {_channel}.")
        channel = self.get_channel(_channel)
        for post in posts:
            if post is None:
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
