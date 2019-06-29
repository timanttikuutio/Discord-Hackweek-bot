import discord
from discord.ext import commands
import random as randint

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """Bans the specified user. An optional reason can be specified."""
        guild = ctx.guild
        if user in guild.users:
            embed=discord.Embed(color=0x80ffff)
            embed.add_field(name="You have been banned from {}", value=guild.name)
            embed.add_field(name="**Reason**", value=reason)
            await guild.ban(user, reason=reason)
        else:
            await ctx.send("User not found.")

    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """Kicks the specified user. An optional reason can be specified."""
        guild = ctx.guild
        if user in guild.members:
            guild.kick(user, reason=reason)

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def purge(self, ctx, amount, channel: discord.TextChannel=None):
        """Format: !purge amount #channel | Deletes the specified amount of messages from the channel. If an channel wasn't specified, the messages will be deleted from the current channel"""
        if channel == None:
            channel = ctx.channel
            deleted = await channel.purge(limit=int(amount))
            await ctx.send("{} messages deleted from {}.".format(len(deleted), channel.mention), delete_after=20)
        else:
            deleted = await channel.purge(limit=int(amount))
            await ctx.send("{} messaged deleted.".format(len(deleted)), delete_after=20)

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def role(self, ctx, user: discord.Member=None, *, role):
        """Gives roles to the specified user. Adding a minus(-) before the role will remove the specified role from the user."""
        guild = ctx.guild
        roles = guild.roles
        author = ctx.author
        if role == None:
            user = author
            pass
        if role.startswith("-"):
            role = role.split("-")[1]
            role = discord.utils.get(roles, name=role)
            await user.remove_roles(role)
            await ctx.send("{}-role removed from {}.".format(role, user))
        else:
            role = discord.utils.get(roles, name=role)
            await user.add_roles(role)
            await ctx.send("{}-role added to {}".format(role, user))
        await ctx.message.add_reaction("✅")


def setup(client):
    client.add_cog(moderation(client))