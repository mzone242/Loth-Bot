from src.bot import loth

#Yes I'm aware this is very bare bones

bot = loth.Loth()

with open("token.txt", "r", encoding="utf-8") as token:
    bot.run(token.read())