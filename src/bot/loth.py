import discord
from discord.ext import tasks, commands

from src.bot import main

VERSION = '0.1.2'


class Loth(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='%')
        self.token = None
        self.version = VERSION

    def run(self, token):
        self.token = token
        super().run(self.token, reconnect=True)

    async def on_ready(self):
        print('Logged in as {0.user}.'.format(self))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith('hello'):
            await message.channel.send('Hello!')



