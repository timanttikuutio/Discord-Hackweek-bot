import traceback
import sys
from discord.ext import commands
import discord


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, "on_error"):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, "original", error)
        
        if isinstance(error, ignored):
            return await ctx.send(error)

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"{ctx.command} can not be used in PM''s.")
            except:
                pass

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send("You don't have permission to run this command.\nError: {}".format(error))

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("The bot doesn't have permissions to run this command.\nError: {}".format(error))


def setup(client):
    client.add_cog(CommandErrorHandler(client))