from typing import Any

import discord
from discord.ext import commands
from discord.utils import utcnow
from pycord.multicog import add_to_group

from base.cog import BaseCog


class Help(BaseCog):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        self.bot: discord.AutoShardedBot = bot
        self.pages: list[Any] = []

    def get_pages(self) -> list[Any]:
        return self.pages

    @add_to_group('dvc')
    @commands.slash_command(description='顯示所有指令的使用方法')
    async def help(self, ctx: discord.ApplicationContext) -> None:
        embed = discord.Embed(
            title=f'所有 {self.bot.user.name} 指令',
            color=discord.Color.from_rgb(72, 60, 76),
            timestamp=utcnow(),
        )
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(icon_url=ctx.author.avatar.url, text=ctx.author)

        for command in self.bot.walk_application_commands():
            if not isinstance(command, discord.SlashCommandGroup):
                embed.add_field(
                    name=f'</{command.qualified_name}:{command.qualified_id}>',
                    value=f'- {command.description}' or '這個指令還沒有介紹，你要幫我想一個嗎',
                    inline=True,
                )

        await ctx.respond(embed=embed)


def setup(bot: discord.AutoShardedBot) -> None:
    bot.add_cog(Help(bot))
