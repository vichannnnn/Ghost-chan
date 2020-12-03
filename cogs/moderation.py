import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import sqlite3
from datetime import datetime
import random
import traceback
import cogs.functions

conn = sqlite3.connect('settings.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

c.execute('''CREATE TABLE IF NOT EXISTS settings (
    `server_id` INT,
    `channel_id` INT) ''')

c.execute('''CREATE TABLE IF NOT EXISTS send (
    `server_id` INT PRIMARY KEY,
    `channel_id` INT) ''')

c.execute(
    '''CREATE TABLE IF NOT EXISTS reaction (`server_id` INT, `message_id` INT, `channel_id` INT, `role` STR, `emoji` STR) ''')


class Moderation(commands.Cog, name="📝 Moderation"):
    """ Ghost-chan's Moderation Commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="clear [amount] [user(optional)]**\n\nPrunes message in a channel. Requires Manage Messages Permission.")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int, member: discord.Member = None):

        if 0 < amount < 101:

            if member:

                deleted = await ctx.channel.purge(limit=amount, check=lambda x: x.author == member)
                embed = discord.Embed(description=f"Deleted {len(deleted)} messages of " + str(member) + "!", colour=cogs.functions.embedColour())
                embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            else:

                deleted = await ctx.channel.purge(limit=amount)
                embed = discord.Embed(description=f'Deleted {len(deleted)} messages!', colour=cogs.functions.embedColour())
                embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        else:

            embed = discord.Embed(description="Amount has to be an integer between 1 to 100!")
            await ctx.send(embed=embed)

    @commands.command(description="ban [user] [reason (optional)]**\n\nBans someone from the server. Requires Ban Members Permission.")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, userName: discord.User, *, reason=None):

        embed = discord.Embed(
            description=f"{userName} has been banned from the server by <@{ctx.message.author.id}> for the following reason: \n\n{reason}")
        embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        notif_embed = discord.Embed(
            description=f"You have been banned by <@{ctx.message.author.id}> from {ctx.message.guild} for the following reason: \n\n{reason}")

        try:
            await userName.send(embed=notif_embed)

        except:

            traceback.print_exc()

        await ctx.guild.ban(userName, reason=f"Banned by {ctx.message.author} | Reason: {reason}")

    @commands.command(description="kick [user]**\n\nKicks someone from the server. Requires Kick Permission.")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, userName: discord.User, *, reason=None):

        embed = discord.Embed(
            description=f"{userName} has been kicked from the server by <@{ctx.message.author.id}> for the following reason: \n\n{reason}")
        embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        notif_embed = discord.Embed(
            description=f"You have been kicked by <@{ctx.message.author.id}> from {ctx.message.guild} for the following reason: \n\n{reason}")
        await userName.send(embed=notif_embed)
        await ctx.guild.kick(userName, reason=f"Kicked by {ctx.message.author} | Reason: {reason}")

    @commands.command(
        description="send [message]**\n\nSends an announcement message to the channel set by `sendset`. Has a built-in cooldown of 30 seconds.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def send(self, ctx, *, message):

        server_id_database = []

        for guild, channel in c.execute('SELECT server_id, channel_id FROM send'):
            server_id_database.append(guild)

        if ctx.message.guild.id in server_id_database:

            for guild_id, channel_id in c.execute('SELECT server_id, channel_id FROM send'):

                if guild_id == ctx.message.guild.id:
                    channel = self.bot.get_channel(channel_id)

                    embed = discord.Embed(description=f"{message}", colour=cogs.functions.embedColour(),
                                          timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
                    await channel.send(embed=embed)

                    embed2 = discord.Embed(description=f"Your message has been sent to <#{channel_id}>.")
                    embed2.set_footer(text=ctx.message.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed2)

        else:
            embed = discord.Embed(description=f"`{ctx.message.guild}` has no message channel set!")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
