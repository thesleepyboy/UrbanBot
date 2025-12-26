import aiohttp
import discord

from datetime import datetime
from discord.ext import commands

from utils import safe_functions as sf
from utils import embeds as em
from utils import paginator

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name='search', description='Search a word')
    @discord.app_commands.describe(term='The term you want to search')
    @discord.app_commands.checks.cooldown(1, 10.0)
    async def search(self, interaction: discord.Interaction, term: str):
        definitions = await sf.safe_get(term)
        if not definitions:
            return await sf.safe_send(interaction, embed=em.warning_embed(
                description="I couldn't find the term you're looking for"
            ))

        if isinstance(definitions, aiohttp.ClientResponseError):
            return await sf.safe_send(interaction, embed=em.error_embed(
                title=f'HTTP Exception {definitions.status}',
                description=definitions.message
            ))

        embeds = []
        for definition in definitions:
            parsed_definition = definition['definition'].replace('[', '').replace(']', '')
            parsed_example = definition['example'].replace('[', '').replace(']', '')
            parsed_date = datetime.strftime(datetime.fromisoformat(definition['written_on']), '%B %d, %Y')

            embed = em.default_embed(
                title=definition['word'],
                url=definition['permalink'],
                description=parsed_definition
            )
            embed.add_field(name='Example', value=parsed_example)
            embed.set_footer(text=f'Created by {definition['author']} on {parsed_date}')

            embeds.append(embed)

        await sf.safe_send(
            interaction, content=f'Page 1/{len(embeds)}',embed=embeds[0], view=paginator.PaginatorView(embeds))

async def setup(bot: commands.Bot):
    await bot.add_cog(Search(bot=bot))