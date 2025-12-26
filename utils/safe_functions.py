import aiohttp
import discord

session = None
bot = None

def setup(_bot):
    global bot
    global session

    bot = _bot
    session = aiohttp.ClientSession(raise_for_status=True)

async def safe_get(term: str):
    url = f'https://api.urbandictionary.com/v0/define?term={term}'

    try:
        async with session.get(url, timeout=2.5) as response:
            data = await response.json()
            return data['list']
    except aiohttp.ClientResponseError as e:
        return e

async def safe_send(destination: discord.Interaction | discord.abc.Messageable, **kwargs):
    permissions = None
    if destination.guild:
        if isinstance(destination, discord.Interaction):
            permissions = destination.channel.permissions_for(destination.guild.me)
        else:
            permissions = destination.permissions_for(destination.guild.me)

    if permissions and not permissions.send_messages:
        return

    if not permissions.embed_links:
        if isinstance(destination, discord.Interaction):
            return await destination.response.send_message(content="I don't have permissions to send embeds here")
        else:
            return await destination.send(content="I don't have permissions to send embeds here")

    try:
        if isinstance(destination, discord.User):
            if not destination.dm_channel:
                await destination.create_dm()

            return await destination.send(**kwargs)
        elif isinstance(destination, discord.Interaction):
            if destination.response.is_done():
                return await destination.followup.send(**kwargs)

            return await destination.response.send_message(**kwargs)
        else:
            return await destination.send(**kwargs)
    except discord.Forbidden:
        if isinstance(destination, discord.User):
            return

        # modify