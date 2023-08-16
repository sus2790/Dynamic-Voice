import discord
from discord.utils import utcnow

from base.cog import BaseCog
from core.emojis import Emojis
from views.selects import DropdownView

class VoiceSetup(BaseCog):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        self.bot: discord.AutoShardedBot = bot

    dvc = discord.SlashCommandGroup('dvc', '動態語音指令', guild_only=True)

    @dvc.command(description='設定動態語音的功能')
    async def setup(self, ctx: discord.ApplicationContext) -> None:
        embed = discord.Embed(
            title=f'{Emojis.SETTING} 動態語音設定系統',
            description='歡迎使用 Dynamic Voice動態語音 設定系統！\n請選取下列選單進行設定：',
            color=discord.Color.random(),
            timestamp=utcnow(),
        )
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(icon_url=ctx.author.avatar.url, text=ctx.author)
        view = DropdownView(self.bot)
        await ctx.respond(embed=embed, view=view)


def setup(bot: discord.AutoShardedBot) -> None:
    bot.add_cog(VoiceSetup(bot))
