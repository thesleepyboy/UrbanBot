import discord

from discord.ext import commands

from utils import safe_functions as sf
from utils import embeds as em

class OnGuildJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        system_channel = guild.system_channel
        if not system_channel:
            return

        await sf.safe_send(system_channel,
            embed=em.default_embed(
                title='Hello!',
                description='Thanks for adding me into your server! Type `/search [term]` to search any term you want'
            )
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(OnGuildJoin(bot=bot))