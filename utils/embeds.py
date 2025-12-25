import discord

bot = None
def setup(_bot):
    global bot
    bot = _bot

def error_embed(**kwargs):
    kwargs['description'] = f'{bot.app_emojis['cross']} {kwargs['description']}'
    kwargs['color'] = discord.Color.red()
    return discord.Embed(**kwargs)

def warning_embed(**kwargs):
    kwargs['description'] = f'{bot.app_emojis['warning']} {kwargs['description']}'
    kwargs['color'] = discord.Color.yellow()
    return discord.Embed(**kwargs)

def default_embed(**kwargs):
    kwargs['color'] = discord.Color.blurple()
    return discord.Embed(**kwargs)