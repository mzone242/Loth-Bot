from argparse import ArgumentParser

from discord.ext import commands

from src.utils import config
from src.utils import database
from src.utils import reddit





def main():

    parser = ArgumentParser(description="Start a bot")
    parser.add_argument('bot')
    parser.add_argument('--debug', '-d', action='store_true')

    args = parser.parse_args()

    start(args.bot, args.debug)


if __name__ == "__main__":
    main()