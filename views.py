from pathlib import Path
from typing import Any

import aiofiles
import discord
import msgspec
from core.emojis import Emojis
from discord.enums import ChannelType
from discord.utils import MISSING, utcnow


class BaseView(discord.ui.View):
    def __init__(
        self, timeout: float = 60.0 * 5, channel_types: list[ChannelType] = MISSING
    ) -> None:
        super().__init__(timeout=timeout)
        self.channel_types: list[ChannelType] = channel_types

    async def on_timeout(self) -> None:
        for children in self.children:
            children.disabled = True  # type: ignore
        await self.message.edit(view=self)

    @discord.ui.channel_select(
        placeholder='戳我選取頻道',
        channel_types=None,  # type: ignore
    )
    async def channel_select_dropdown(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        embed = discord.Embed(
            title=f'{Emojis.LOADING} 正在處理中...',
            description='聽說沒有人會注意這裡 🤔',
            color=discord.Color.yellow(),
            timestamp=utcnow(),
        )
        embed.set_author(
            name=interaction.client.user.name,
            icon_url=interaction.client.user.avatar,
        )
        embed.set_footer(icon_url=interaction.user.avatar, text=interaction.user)
        await interaction.response.edit_message(content=None, embed=embed, view=None)

        guild_path = Path(f'data/{interaction.guild_id}.json')

        if not guild_path.exists():
            guild_path.touch()

        async with aiofiles.open(guild_path, 'r') as f:
            content: str = await f.read()
            self.feature: Any | dict[Any, Any] = msgspec.json.decode(content) if content else {}
            self.feature['dvc-channel'] = int(
                ', '.join(f'{channel.id}' for channel in select.values)  # type: ignore
            )

        async with aiofiles.open(guild_path, 'w') as f:
            await f.write(msgspec.json.encode(self.feature))  # type: ignore

        embed = discord.Embed(
            title=f'{Emojis.SUCCESSFUL} 設定成功!',
            description=f"已將動態語音通知頻道設置為:{self.feature['dvc-notify-channel']}",
            color=discord.Color.green(),
            timestamp=utcnow(),
        )
        embed.set_author(
            name=interaction.client.user.name,
            icon_url=interaction.client.user.avatar,
        )
        embed.set_footer(icon_url=interaction.user.avatar, text=interaction.user)
        await interaction.edit_original_response(content=None, embed=embed, view=None)


class VoiceChannel(BaseView):
    def __init__(self, timeout: float = 60.0 * 5) -> None:
        channel_types: list[ChannelType] = [ChannelType.voice]
        super().__init__(timeout=timeout, channel_types=channel_types)


class NotifyView(BaseView):
    def __init__(self, timeout: float = 60.0 * 5) -> None:
        channel_types: list[ChannelType] = [
            discord.abc.MessageableChannel
        ]
        super().__init__(timeout=timeout, channel_types=channel_types)


class Dropdown(discord.ui.Select):
    def __init__(self, bot: discord.AutoShardedBot) -> None:
        options: list[discord.SelectOption] = [
            discord.SelectOption(
                label='設定動態語音通知頻道',
                emoji=str(Emojis.TEXT),
                value='dvc-notify-channel',
            ),
            discord.SelectOption(
                label='設定動態語音頻道',
                emoji=str(Emojis.VOICE),
                value='dvc-voice-channel',
            ),
        ]

        super().__init__(
            placeholder='選擇操作',
            options=options,
        )

        self.bot: discord.AutoShardedBot = bot

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.values[0] == 'dvc-notify-channel':
            embed = discord.Embed(
                title=f'{Emojis.MENU} 通知頻道選擇',
                description=f'{interaction.user.mention} 請選取下列選單來設定動態語音通知頻道:',
                color=discord.Color.blue(),
                timestamp=utcnow(),
            )
            embed.set_author(
                name=interaction.client.user.name,
                icon_url=interaction.client.user.avatar,
            )
            embed.set_footer(icon_url=interaction.user.avatar, text=interaction.user)
            await interaction.response.send_message(
                embed=embed,
                view=NotifyView(),
                ephemeral=True,
            )
        elif self.values[0] == 'dvc-voice-channel':
            embed = discord.Embed(
                title=f'{Emojis.MENU} 語音頻道選擇',
                description=f'{interaction.user.mention} 請選取下列選單來設定動態語音頻道:',
                color=discord.Color.blue(),
                timestamp=utcnow(),
            )
            embed.set_author(
                name=interaction.client.user.name,
                icon_url=interaction.client.user.avatar,
            )
            embed.set_footer(icon_url=interaction.user.avatar, text=interaction.user)
            await interaction.response.send_message(
                embed=embed,
                view=VoiceChannel(),
                ephemeral=True,
            )


class DropdownView(discord.ui.View):
    def __init__(self, bot: discord.AutoShardedBot, timeout: float = 60.0 * 5) -> None:
        super().__init__(timeout=timeout)
        self.add_item(Dropdown(bot))

    async def on_timeout(self) -> None:
        for children in self.children:
            children.disabled = True  # type: ignore
        await self.message.edit(view=self)
