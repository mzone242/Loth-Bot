import discord
from discord.ext import tasks, commands

import asyncio

from src.bot import main

VERSION = '0.1.2'
CHANNEL = 455483961490276353


class Loth(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='%')
        self.version = VERSION
        self.channel = CHANNEL

    def run(self, token):
        super().run(token, reconnect=True)

    async def on_ready(self):
        print('Logged in as {0.user}.'.format(self))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith('check_sub'):
            await self.check_sub()

    @tasks.loop(minutes=5)
    async def routine(self):
        await self.check_sub()

    async def check_sub(self):
        channel = self.get_channel(self.channel)
        await channel.send("Checking sub")
        posts = main.scrape_reddit(1000)
        for post in posts:
            await channel.send(embed=discord.Embed(title="This post has over 100 upvotes: ",
                                                   description=f"https://www.reddit.com/r/"
                                                               f"PrequelMemes/comments/{post[0]}"))
            await asyncio.sleep(1)
        _posts = main.update_database(posts)
        for post in _posts:
            await channel.send(embed=discord.Embed(title="This post has over 1000 upvotes: ",
                                                   description=f"https://www.reddit.com/r/"
                                                               f"PrequelMemes/comments/{post[0]}"))
            await asyncio.sleep(1)
        main.clean_database()
