from pathlib import Path
from typing import Any

import aiofiles
import discord
import msgspec
from discord.ext import commands
from discord.utils import utcnow

from base.cog import BaseCog
from core.emojis import Emojis


class VoiceEvent(BaseCog):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        self.bot: discord.AutoShardedBot = bot
        self.channel: discord.VoiceChannel = None

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        guild_path = Path(f"data/{member.guild.id}.json")

        if not guild_path.exists():
            guild_path.touch()

        async with aiofiles.open(guild_path, "r") as f:
            content: str = await f.read()
            self.data: Any | dict[Any, Any] = (
                msgspec.json.decode(content) if content else {}
            )

        dvc_channel: Any | None = self.data.get("dvc-channel", None)
        notify_channel_id: Any | None = self.data.get("dvc-notify-channel", None)
        notify_channel: discord.TextChannel | None = self.bot.get_channel(
            notify_channel_id
        )  # type: ignore

        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title=f"{Emojis.JOIN} 加入語音頻道",
                description=f"{member.mention} 加入了語音頻道 {after.channel.mention}",
                color=discord.Color.green(),
                timestamp=utcnow(),
            )
            if notify_channel is not None:
                await notify_channel.send(embed=embed)

            if dvc_channel is not None and after.channel.id == int(dvc_channel):
                overwrites: dict[Any, discord.PermissionOverwrite] = {
                    after.channel.guild.default_role: discord.PermissionOverwrite(
                        connect=False
                    ),
                    member: discord.PermissionOverwrite(administrator=True),
                    after.channel.guild.me: discord.PermissionOverwrite(
                        administrator=True
                    ),
                }
                self.channel = await member.guild.create_voice_channel(
                    name=f"🌠 | {member.name} 的頻道",
                    category=after.channel.category,
                    overwrites=overwrites,
                    reason="Dynamic Voice",
                )
                await member.move_to(self.channel)

        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(
                title=f"{Emojis.LEAVE} 離開語音頻道",
                description=f"{member.mention} 離開了語音頻道 {before.channel.mention}",
                color=discord.Color.red(),
                timestamp=utcnow(),
            )
            if notify_channel is not None:
                await notify_channel.send(embed=embed)

            assert self.channel

            if (
                dvc_channel is not None
                and before.channel.id == self.channel.id
                and len(before.channel.members) == 0
            ):
                await before.channel.delete(reason="Dynamic Voice")


def setup(bot: discord.AutoShardedBot) -> None:
    bot.add_cog(VoiceEvent(bot))
