import traceback
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

from utils import safe_functions as sf
from utils import embeds as em

load_dotenv()

class Tree(discord.app_commands.CommandTree):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            client=bot
        )

    async def on_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            return await sf.safe_send(interaction,
               embed=em.error_embed(description=f'This command is on cooldown. Retry in **{round(error.retry_after)}s**')
            )
        elif isinstance(error, discord.app_commands.CommandSignatureMismatch):
            return await sf.safe_send(interaction,
                embed=em.warning_embed(description='Hey! So, this command is outdated. Please, try again later')
            )
        elif isinstance(error, discord.app_commands.CommandInvokeError):
            await sf.safe_send(interaction,
               embed=em.error_embed(description="I tried executing this command but I couldn't for some reason")
            )

class UrbanBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=None,
            intents=discord.Intents.default(),
            tree_cls=Tree
        )

        self.app_emojis = {}

    async def get_app_emojis(self):
        app_emojis = await self.fetch_application_emojis()
        for emoji in app_emojis:
            self.app_emojis[emoji.name] = f'<:{emoji.name}:{emoji.id}>'

    async def setup_hook(self) -> None:
        sf.setup(self)
        em.setup(self)

        cogs_dir = os.listdir(os.path.join(os.path.dirname(__file__), 'cogs'))
        for folder in cogs_dir:
            cogs = os.listdir(os.path.join(os.path.dirname(__file__), 'cogs', folder))
            for cog in cogs:
                path = f'cogs.{folder}.{cog[:-3]}'
                try:
                    await self.load_extension(path)
                    print(f'{path} loaded successfully')
                except commands.NoEntryPointError:
                    print(f'Extension does not have a setup function')
                except Exception as e:
                    print(f'Unknown exception: {e}')
                    traceback.print_exc()
                    raise

        try:
            await self.tree.sync()
        except discord.app_commands.CommandSyncFailure as e:
            print(f"Couldn't sync commands: {e}")
            traceback.print_exc()
            raise

        await self.get_app_emojis()

bot = UrbanBot()
bot.run(os.getenv('BOT_TOKEN'))