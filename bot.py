import discord
from discord.ext import commands
from utils.config import Config
import datetime
import utils
import sys, os
import asyncio

print("Connecting...")

config = Config()
TOKEN = config.token
global extensions
extensions = [
        "information",
        "moderation",
        "CommandErrorHandler",
        "logs",
        "fun"
    ]

client = commands.AutoShardedBot(command_prefix = config.command_prefix)

@client.event
async def on_ready():
    print("Logged in as:\n{}/{}#{}\n----------".format(client.user.id, client.user.name, client.user.discriminator))
    await client.change_presence(activity=discord.Game(name=""))
    for extension in extensions:
        try:
            client.load_extension("commands." + extension)
        except Exception as e:
            print("Couldn't load cog {} because of an error: {}".format(extension, e))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)        

@commands.is_owner()
@client.command()
async def reload(ctx, extension):
    """Use [p]reloadcog all to reload every cog or specify name to reload the specified cog."""
    if extension not in extensions:
        await ctx.send("Extension named {} does not exist. Please re-check spelling.".format(extension))
    else:
        client.reload_extension("commands." + extension)
        await ctx.send("Reloading cog `{}`...".format(extension))

@commands.is_owner()
@client.command()
async def shutdown(ctx, arg=None):
    """Use -force to force the bot to shut down."""
    if arg == "-force":
        sys.exit()
    else:
        await client.logout()

client.run(TOKEN, reconnect=True)