import os
from traceback import format_exception

import aiohttp
import discord
from base.cog import BaseCog
from core.emojis import Emojis
from discord import Webhook
from discord.ext import commands
from discord.utils import utcnow


class Errors(BaseCog):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        self.bot: discord.AutoShardedBot = bot

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ) -> None:
        caught: bool = True
        error_type: str = error.__class__.__name__
        error_message: str = ''.join(format_exception(type(error), error, error.__traceback__))

        if caught:
            self.logger.exception(error_message)

        error_embed = discord.Embed(
            title=f'{Emojis.CROSS} 又有一個奇怪的錯誤了',
            color=discord.Color.red(),
            timestamp=utcnow(),
        )
        error_embed.add_field(name='錯誤類型', value=f'```py\n{error_type}\n```')
        error_embed.add_field(name='錯誤訊息', value=f'```py\n{error}\n```')
        error_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        error_embed.set_footer(
            icon_url=ctx.guild.icon.url if ctx.guild.icon else ctx.author.avatar.url,
            text=ctx.guild.name if ctx.guild.icon else ctx.author.name,
        )

        user_embed = discord.Embed(
            title=f'{Emojis.CROSS} 看來你遇到了一個錯誤',
            description=f'機器人處理指令時發生錯誤，請稍後再試 {Emojis.SAD}',
            color=discord.Color.red(),
            timestamp=utcnow(),
        )
        user_embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        user_embed.set_footer(icon_url=ctx.author.avatar.url, text=f'{ctx.author} 測試')

        async with aiohttp.ClientSession() as session:
            webhook: Webhook = Webhook.from_url(os.environ['WEBHOOK_URL'], session=session)
            await webhook.send(
                f'<@!823122263552425984>\n```py\n{error_message[:1000]}\n```',
                embed=error_embed,
            )

        await ctx.respond(embed=user_embed, ephemeral=True)


def setup(bot: discord.AutoShardedBot) -> None:
    bot.add_cog(Errors(bot))
