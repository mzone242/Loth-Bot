import logging

from src.bot import loth
from src.utils.helper import setup_logger

logger = logging.getLogger("launcher")
debug = False

setup_logger('launcher', debug)
setup_logger('bot', debug)
setup_logger('utils', debug)
# setup_logger('cogs', debug)
setup_logger('discord', False)

logger.info(f"Starting bot.")

bot = loth.Loth()

try:
    with open("token.txt", "r", encoding="utf-8") as token:
        bot.run(token.read())
finally:
    try:
        exit_code = bot.exit_code
    except:
        logger.info("Bot's exit code could not be retrieved.")
        exit_code = 0
    logger.info(f"Bot closed with exit code {exit_code}.")
    exit(exit_code)
