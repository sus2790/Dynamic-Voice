import logging
from typing import Any

import discord
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: discord.AutoShardedBot, *args: Any, **kwargs: Any) -> None:
        self.bot: discord.AutoShardedBot = bot
        super().__init__(*args, **kwargs)

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger('DynamicVoice')
