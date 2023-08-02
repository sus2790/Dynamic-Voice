import discord
from discord.ext import commands
from discord.utils import utcnow
from pycord.multicog import add_to_group


class Ping(commands.Cog):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        self.bot: discord.AutoShardedBot = bot

    @add_to_group('dvc')
    @commands.slash_command(description='顯示機器人的延遲')
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        embed = discord.Embed(
            title='原神！啟動！',
            description=f'蹦蹦炸彈！`{self.bot.latency*1000:.2f}ms`',
            color=discord.Color.from_rgb(170, 36, 44),
            timestamp=utcnow(),
        )
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(icon_url=ctx.author.avatar.url, text=ctx.author)
        embed.set_image(url='https://i.imgur.com/8ndBsP8.png')
        await ctx.respond(embed=embed)


def setup(bot: discord.AutoShardedBot) -> None:
    bot.add_cog(Ping(bot))
