import discord
from discord.ext import tasks, commands

import asyncio

from src.bot import main

VERSION = '0.1.3'
CHANNEL = 455483961490276353
NOT_SHIT = 725127435737367054
MEH_SHIT = 714410477236519001


class Loth(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='%')
        self.version = VERSION
        self.channel = NOT_SHIT
        self.channel2 = MEH_SHIT

    def run(self, token):
        super().run(token, reconnect=True)

    async def on_ready(self):
        self.routine.start()
        print('Logged in as {0.user}.'.format(self))

    async def on_message(self, message):
        if message.author.bot:
            return
        """post = ("iajjog", 224, 1597540648, False, "howardthemetalalien", "https://i.redd.it/caa344x0n9h51.png", "hello there")
        embed = discord.Embed(title="This post has received over 100 upvotes. Please check it out.")
        embed.set_author(name=post[4], url=f"https://www.reddit.com/u/{post[4]}")
        embed.set_image(url=post[5])
        embed.description = f"https://www.reddit.com/r/PrequelMemes/comments/{post[0]}"
        channel = self.get_channel(self.channel2)
        await channel.send(embed=embed)"""
        if message.content.startswith('check_sub'):
            await self.check_sub()

    @tasks.loop(minutes=5)
    async def routine(self):
        await self.check_sub()

    async def check_sub(self):
        # await channel.send("Checking sub")
        posts = main.scrape_reddit(1000)
        await self.send_embed(posts, 100, self.channel2)
        _posts = main.update_database(posts)
        await self.send_embed(_posts, 1000, self.channel)
        main.clean_database()

    async def send_embed(self, posts, upvotes, _channel):
        channel = self.get_channel(_channel)
        for post in posts:
            embed = discord.Embed(title=f"This post has over {upvotes} upvotes. Please check it out.",
                                  description="Please react with :white_check_mark: if you checked the post and it is "
                                              "good and please react with :x: if you checked the post and removed it.")
            embed.add_field(name=f"{post[6]}", value=f"https://www.reddit.com/r/PrequelMemes/comments/{post[0]}")
            embed.set_author(name=post[4], url=f"https://www.reddit.com/u/{post[4]}")
            embed.set_image(url=post[5])
            msg = await channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            await asyncio.sleep(1)
