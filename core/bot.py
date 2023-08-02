import logging
import os
from traceback import format_exception

import coloredlogs
import discord
from dotenv import load_dotenv
from pycord.multicog import apply_multicog

load_dotenv()


class DynamicVoice(discord.AutoShardedBot):
    def __init__(self) -> None:
        coloredlogs.install(logging.DEBUG)
        logging.getLogger('discord').setLevel(logging.ERROR)

        super().__init__(
            activity=discord.Game('Dynamic Voice - 動態語音'),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
            chunk_guilds_at_startup=False,
            intents=discord.Intents.default(),
            member_cache_flags=discord.MemberCacheFlags.none(),
        )

        self.logger: logging.Logger = logging.getLogger('DynamicVoice')
        self.version: str = os.getenv('VERSION') or '未知'

        for k, v in self.load_extension('cogs', recursive=True, store=True).items():
            if v is True:
                self.logger.debug(f'[Cog] {k} 載入成功')
            else:
                self.logger.error(
                    f"[Cog] {k} 發生錯誤\n{''.join(format_exception(type(v), v, v.__traceback__))}"
                )

        apply_multicog(self._bot)

    async def on_ready(self) -> None:
        print(
            f"""

        Dynamic Voice - 讓動態語音變得更好
        正在運行版本 {self.version} ！

        """
        )
        self.logger.info(f'[Bot] {self._bot.user} 準備就緒')

    async def on_shard_ready(self, shard_id: int) -> None:
        self.logger.info(f'[Shard {shard_id}] 準備就緒')

    async def on_shard_disconnect(self, shard_id: int) -> None:
        self.logger.warning(f'[Shard {shard_id}] 已斷線')

    async def on_shard_resumed(self, shard_id: int) -> None:
        self.logger.info(f'[Shard {shard_id}] 已恢復連線')

    def run(self) -> None:
        super().run(os.environ['TOKEN'])
