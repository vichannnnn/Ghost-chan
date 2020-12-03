import discord
import random
from discord.ext import commands
import sqlite3
import cogs.functions

conn = sqlite3.connect('emotes.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

class Emotes(commands.Cog, name="<:hug:783848710353453077> Emotes"):

    """ This is where all the miscellaneous and fun commands are at! Utility? Maybe... """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="hug [mention]**\n\nHugs someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, argument: discord.Member):
        hugList = [link[0] for link in c.execute(''' SELECT gifLink FROM hug ''')]

        embed = discord.Embed(description=f'{ctx.author.mention} hugged {argument.mention}\n\n',
                              colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(hugList))
        await ctx.send(embed=embed)

    @commands.command(description="kiss [mention]**\n\nKisses someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, argument: discord.Member):
        kissList = [link[0] for link in c.execute(''' SELECT gifLink FROM kiss ''')]

        embed = discord.Embed(
            description=f'{ctx.author.mention} kissed {argument.mention}\n\n', colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(kissList))
        await ctx.send(embed=embed)

    @commands.command(description="slap [mention]**\n\nSlaps someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, argument: discord.Member):
        slapList = [link[0] for link in c.execute(''' SELECT gifLink FROM slap ''')]

        embed = discord.Embed(
            description=f'{ctx.author.mention} slapped {argument.mention}\n\n', colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(slapList))
        await ctx.send(embed=embed)

    @commands.command(description="poke [mention]**\n\nPokes someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poke(self, ctx, argument: discord.Member):
        pokeList = [link[0] for link in c.execute(''' SELECT gifLink FROM poke ''')]

        embed = discord.Embed(
            description=f'{ctx.author.mention} poked {argument.mention}\n\n', colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(pokeList))
        await ctx.send(embed=embed)

    @commands.command(description="pat [mention]**\n\nPats someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, argument: discord.Member):
        patList = [link[0] for link in c.execute(''' SELECT gifLink FROM pat ''')]

        embed = discord.Embed(
            description=f'{ctx.author.mention} is patting {argument.mention}\n\n', colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(patList))
        await ctx.send(embed=embed)

    @commands.command(description="bite [mention]**\n\nBites someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bite(self, ctx, argument: discord.Member):
        biteList = [link[0] for link in c.execute(''' SELECT gifLink FROM bite ''')]

        embed = discord.Embed(
            description=f'{ctx.author.mention} is biting {argument.mention}\n\n', colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(biteList))
        await ctx.send(embed=embed)

    @commands.command(description="lick [mention]**\n\nLicks someone in the server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, argument: discord.Member):
        lickList = [link[0] for link in c.execute(''' SELECT gifLink FROM lick ''')]

        embed = discord.Embed(
            description=f'{ctx.author.mention} licked {argument.mention}\n\n', colour=cogs.functions.embedColour())
        embed.set_image(url=random.choice(lickList))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Emotes(bot))
