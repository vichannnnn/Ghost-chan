import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
import aiohttp
from googleapiclient.discovery import build
from authentication import google_api_key, google_cse_id, topGGtoken
import dbl
import sqlite3
import cogs.functions

conn = sqlite3.connect('emotes.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

class Utility(commands.Cog, name="🎲 Fun"):

    """ This is where all the miscellaneous and fun commands are at! Utility? Maybe... """

    def __init__(self, bot):
        self.bot = bot
        self.token = f'{topGGtoken}'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='password',
                                   webhook_port=5000)

    @commands.command(description="vote**\n\nVote for Ghost-chan!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vote(self, ctx):

        check = await self.dblpy.get_user_vote(ctx.message.author.id)

        if check:
            embed = discord.Embed(
                description=f"**{ctx.message.author}**, thank you for voting for Ghost-chan today!\n\nAs a form of appreciation, here is a hug from voting for me!", colour=cogs.functions.embedColour())
            embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)

            hugList = [link[0] for link in c.execute(''' SELECT gifLink FROM hug ''')]

            embed.set_image(url=random.choice(hugList))
            await ctx.send(embed=embed)
            channel = self.bot.get_channel(706292370085249034)
            await channel.send(f"<@{ctx.message.author.id}> has voted for Ghost-chan.")

        else:

            embed = discord.Embed(
                title=f"**You have not voted for Ghost-chan yet..**",
                description="You can vote for me with the link below:", colour=cogs.functions.embedColour())
            embed.add_field(name="Ghost-chan's Voting Link",
                            value="[🔗 Discord Bot List](https://top.gg/bot/699457008759472200/vote)",
                            inline=True)
            embed.set_thumbnail(url="https://i.imgur.com/3Lgs39V.png")
            embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(description="google [word]**\n\nGoogle Search the top 10 result of the said word.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, word):

        search_result = ''

        def google_search(search_term, api_key, cse_id, **kwargs):
            service = build("customsearch", "v1", developerKey=api_key)
            res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
            return res["items"]

        results = google_search(word, google_api_key, google_cse_id, num=10)

        i = 0

        for result in results:

            i += 1
            search_result += f'{i}) {result["link"]}\n\n'

        embed = discord.Embed(
            description=f"Here are your top 10 Google Search results for the word `{word}`:\n\n{search_result}", colour=cogs.functions.embedColour())
        embed.set_author(name="Google Search Results",
                         icon_url="https://w7.pngwing.com/pngs/882/225/png-transparent-google-logo-google-logo-google-search-icon-google-text-logo-business.png")
        embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description="upload [Name of Emoji] [Image URL]**\n\nUploads an emoji to your Discord Server. Manage Emoji Permission Required.")
    @has_permissions(manage_emojis=True)
    async def upload(self, ctx, name, image_url):

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                image_bytes = await response.read()

        await ctx.message.guild.create_custom_emoji(name=name, image=image_bytes)
        embed = discord.Embed(description=f"Uploaded `{name}` as an emote to `{ctx.message.guild}` server!", colour=cogs.functions.embedColour())
        embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)






def setup(bot):
    bot.add_cog(Utility(bot))
