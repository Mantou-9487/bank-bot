import asyncio
import json
import logging
from os import getenv
import os
from dotenv import load_dotenv

from disnake import Intents,Game
from disnake.ext.commands import CommandSyncFlags

from disnake.ext.commands import Bot

logging.basicConfig(level=logging.INFO)


def main():
    loop = asyncio.new_event_loop()

    bot = Bot(
        command_prefix=getenv("PREFIX", "l!"), intents=Intents.all(), loop=loop,
        command_sync_flags=CommandSyncFlags.default()
    )
    load_extensions(bot)
    load_dotenv()
    bot.run(os.getenv("TOKEN"))

def load_extensions(bot: Bot) -> Bot:
    """
    Load extensions in extensions.json file
    :param bot: The bot to load the extensions to
    :return: The bot
    """
    for fn in os.listdir("./cogs"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")
    
    return bot

if __name__ == "__main__":
    main()