import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect("config/database.db")
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS logging(guild INT, actionlog INT, modlog INT)""")



class logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild = guild.id
        cur.execute("""SELECT guild FROM logging""")
        guilds = cur.fetchall()
        if guild not in guilds:
            cur.execute("""INSERT INTO logging VALUES (?, ?, ?)""", (guild, None, None))
            db.commit()
 
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        author = message.author
        cur.execute("""SELECT actionlog FROM logging WHERE guild = ?""", (guild.id,))
        channel = cur.fetchall()
        channel = guild.get_channel(channel[0][0])
        if message.author != guild.me:
            embed=discord.Embed(color=0x80ffff, description="**Message sent by** {} **deleted in** {}\n{}".format(author.mention, message.channel.mention, message.content))
            embed.set_author(name=author.name, icon_url=author.avatar_url)
            embed.set_footer(text="Author: {} | Message ID: {} • {}".format(author.id, message.id, message.created_at))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        print(messages.guild.id)
        for message in messages:
            guild = message.guild
        cur.execute("""SELECT actionlog FROM logging WHERE guild = ?""", (guild.id,))
        channel = cur.fetchall
        if channel != []:
            channel = guild.get_channel(channel[0][0])
            embed=discord.Embed(color=0x80ffff, description="**Bulk delete in** {}**, {} messages deleted.**")
            await channel.send(embed=embed)
    
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def logset(self, ctx, option, channel: discord.TextChannel):
        """Usage: !logset modlog/actionlog #channel"""
        guild = ctx.guild.id
        channel = channel
        if option == "modlog":
            cur.execute("""UPDATE logging SET modlog = ?, guild = ? WHERE guild = ?""", (channel.id, guild, guild))
            db.commit()
            await ctx.send("Modlog channel set to {}".format(channel.mention))

        elif option == "actionlog":  
            cur.execute("""UPDATE logging SET actionlog = ?, guild = ? WHERE guild = ?""", (channel.id, guild, guild))
            db.commit()
            await ctx.send("Actionlog channel set to {}".format(channel.mention))

        else:
            await ctx.send("Wrong option. Please use 'modlog' or 'actionlog'")

def setup(client):
    client.add_cog(logs(client))