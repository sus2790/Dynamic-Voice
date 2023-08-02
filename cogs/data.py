from pathlib import Path
from typing import Any

import aiofiles
import discord
import msgspec
from discord.ext import commands
from pycord.multicog import add_to_group

from base.cog import BaseCog
from core.emojis import Emojis


class Data(BaseCog):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        self.bot: discord.AutoShardedBot = bot

    @add_to_group('dvc')
    @commands.slash_command(description='設定該伺服器的動態語音資料')
    @discord.default_permissions(administrator=True)
    async def data(
        self, ctx: discord.ApplicationContext
    ) -> discord.Interaction | discord.WebhookMessage | None:
        guild_path = Path(f'data/{ctx.guild_id}.json')

        if not guild_path.exists():
            guild_path.touch()

        async with aiofiles.open(guild_path, 'r') as f:
            content: str = await f.read()
            self.data: Any | dict[Any, Any] = msgspec.json.decode(content) if content else {}

        if len(self.data) == 0:
            embed = discord.Embed(
                title=f'{Emojis.DATA} {ctx.guild.name} 資料錯誤',
                description='無法讀取伺服器資料，你真的有設定嗎._.',
                color=discord.Color.random(),
            )
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_footer(icon_url=ctx.author.avatar.url, text=ctx.author)
            return await ctx.respond(embed=embed)

        embed = discord.Embed(
            title=f'{Emojis.DATA} {ctx.guild.name} 的動態語音資料',
            color=discord.Color.random(),
        )
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(icon_url=ctx.author.avatar.url, text=ctx.author)
        channel_description: dict[str, str] = {
            'dvc-notify-channel': '動態語音通知頻道',
            'dvc-channel': '動態語音頻道',
        }
        for key, value in self.data.items():
            title = channel_description.get(key, '未知')
            value = f'```{value}```' if title.startswith('未知') else f'```{value}```(<#{value}>)'
            embed.add_field(name=title, value=value, inline=True)
        await ctx.respond(embed=embed)


def setup(bot: discord.AutoShardedBot) -> None:
    bot.add_cog(Data(bot))
