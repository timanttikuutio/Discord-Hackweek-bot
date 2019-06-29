import discord
from discord.ext import commands
import random
import youtube_dl


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self, ctx, choice=None):
        """Usage: !rps rock/paper/scissors"""
        if choice == None:
            embed=discord.Embed(color=0x00FFFF)
            embed.add_field(name="Usage:", value="You need to choose rock, paper or scissors.")
            await ctx.send(embed=embed)
           
        elif choice.lower() not in ["rock", "paper", "scissors"]:
            embed=discord.Embed(color=0x00FFFF)
            embed.add_field(name="Invalid choice.", value="You need to choose rock, paper or scissors.")
            await ctx.send(embed=embed)
        else:
            ai = random.randint(1, 3)
            if choice == "rock":
                if ai == 1:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="Nobody won.", value="You chose **Rock**, I choose **Rock**.")
                    await ctx.send(embed=embed)
                if ai == 2:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="I won.", value="You chose **Rock**, I choose **Paper**.")
                    await ctx.send(embed=embed)
                if ai == 3:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="{}, you won.".format(ctx.message.author), value="You chose **Rock**, I choose **Scissors**.")
                    await ctx.send(embed=embed)
            if choice == "paper":
                if ai == 1:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="{}, you won.".format(ctx.message.author), value="You chose **Paper**, I choose **Rock**.")
                    await ctx.send(embed=embed)
                if ai == 2:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="Nobody won.", value="You chose **Paper**, I choose **Paper**")
                    await ctx.send(embed=embed)
                if ai == 3:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="I won.", value="You chose **Paper**, I choose **Scissors**.")
                    await ctx.send(embed=embed)
            if choice == "scissors":
                if ai == 1:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="I won.", value="You chose **Scissors**, I choose **Rock**.")
                    await ctx.send(embed=embed)
                if ai == 2:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="{}, you won.".format(ctx.message.author), value="You chose **Scissors**, I choose **Paper**.")
                    await ctx.send(embed=embed)
                if ai == 3:
                    embed=discord.Embed(color=0x00FFFF)
                    embed.add_field(name="Nobody won.", value="You chose **Scissors**, I choose **Scissors**.")
                    await ctx.send(embed=embed)

    @commands.command()
    async def gtn(self, ctx, message: discord.Message = None):
        guesses = 10
        embed=discord.Embed(color=0x4A90E2)
        embed.add_field(name="I'm thinking of a new number:", value="Guess the number and i'll tell you if it's higher or lover than your guess!", inline=False)
        embed.set_footer(text="It's between 1 and 1000")
        await ctx.send(embed=embed)
        number = random.randint(1,1000)
        while True:
            guess = await self.client.wait_for("message", check=lambda message: message.author == ctx.author)
            if guess.content.lstrip("-").strip(".").isdigit() == True:
                if guesses < 1:
                    await ctx.send(guess.author.mention)
                    embed=discord.Embed(color=0xFF0000)
                    embed.set_author(name=guess.author.name, icon_url=guess.author.avatar_url)
                    embed.add_field(name="You guessed incorrectly 10 times and you lost.", value="The number was: `{}`. Better luck next time :)".format(number))
                    await ctx.send(embed=embed)
                    break
                else:
                    if int(guess.content) > number:
                        guesses = guesses - 1
                        embed=discord.Embed(color=0x00ffff)
                        embed.add_field(name="Lower:", value="It's lower than **{}**".format(guess.content), inline=False)
                        await ctx.send(embed=embed)

                    elif int(guess.content) < number:
                        guesses = guesses - 1
                        embed=discord.Embed(color=0x00ffff)
                        embed.add_field(name="Higher:", value="It's higher than **{}**".format(guess.content), inline=False)
                        await ctx.send(embed=embed)

                    elif int(guess.content) == number:
                        await ctx.send(ctx.author.mention)
                        embed=discord.Embed(color=0x00ff40)
                        embed.add_field(name="{} Guessed correctly.".format(guess.author), value="I was thinking of the number {}".format(number), inline=True)
                        await ctx.send(embed=embed)
                        break

            else:	
                if guess.content == "quit" or guess.content == "exit" and ctx.author == guess.author:
                    embed=discord.Embed(color=0x00ffff)
                    embed.add_field(name="Game cancelled.", value="I was thinking of the number {}".format(number))
                    await ctx.send(embed=embed)
                    break
                else:
                    continue

def setup(client):
    client.add_cog(fun(client))