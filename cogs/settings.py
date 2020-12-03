import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import sqlite3
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


class Settings(commands.Cog, name="🛠️ Settings"):

    """ Ghost-chan's Settings Commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="sendset [#channel]**\n\nSets the announcement channel in the server where messages used from `send` command will go to. Leave channel argument empty to remove. Requires Administrator Permission.")
    @has_permissions(administrator=True)
    async def sendset(self, ctx, channel: discord.TextChannel = None):

        if channel:

            c.execute(''' INSERT OR REPLACE INTO send VALUES (?, ?) ''', (ctx.message.guild.id, channel.id))
            conn.commit()
            embed = discord.Embed(description=f"`{ctx.message.guild}`'s response feedback has been set to {channel}.\n\nAll message using `send` command will be sent to {channel} from now on.", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)

        else:

            c.execute(''' DELETE from send where server_id = ? ''', (ctx.message.guild.id,))
            conn.commit()
            embed = discord.Embed(description=f"`{ctx.message.guild}`'s response feedback channel has been removed.", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)


    @commands.command(description="ghoststatus**\n\nChecks if Ghost Ping Alert is on for the channel.")
    async def ghoststatus(self, ctx):

        id = str(ctx.message.channel.id)
        channel_id = id.replace('<', '').replace('>', '').replace('#', '')

        global guild_id

        channel_id_database = []

        for guild_id in c.execute(f'SELECT channel_id FROM settings WHERE server_id = {ctx.message.guild.id}'):
            channel_id_database.append(guild_id[0])

        if int(channel_id) in channel_id_database:

            embed = discord.Embed(title="Ghost Ping Alert's Status", description=f"<#{channel_id}>: **OFF**\n\nGhost-chan is currently not guarding this channel!", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(title="Ghost Ping Alert's Status", description=f"<#{channel_id}>: **ON**\n\nGhost-chan is currently guarding this channel!", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)

    @commands.command(description="ghostoff**\n\nDisables Ghost Ping Alert on the chat channel it was called on. Manage Message Permission Required.")
    @has_permissions(manage_messages=True)
    async def ghostoff(self, ctx):

        server_id = ctx.guild.id
        id = str(ctx.message.channel.id)
        channel_id = id.replace('<', '').replace('>', '').replace('#', '')

        global guild_id

        channel_id_database = []

        for guild_id in c.execute(f'SELECT channel_id FROM settings WHERE server_id = {ctx.message.guild.id}'):
            channel_id_database.append(guild_id[0])

        if int(channel_id) in channel_id_database:

            embed = discord.Embed(title='Error!',
                                  description=f"Ghost Ping Alert has already been disabled on <#{channel_id}> before!", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(description=f"Ghost Ping Alert is now disabled on <#{channel_id}>!", colour=cogs.functions.embedColour())

            c.execute(''' INSERT OR REPLACE INTO settings VALUES (?, ?) ''', (server_id, channel_id))
            conn.commit()

            await ctx.send(embed=embed)


    @commands.command(description="ghoston**\n\nEnables Ghost Ping Alert on the chat channel if it was disabled before. Manage Message Permission Required.")
    @has_permissions(manage_messages=True)
    async def ghoston(self, ctx):

        server_id = ctx.guild.id
        id = str(ctx.message.channel.id)
        channel_id = id.replace('<', '').replace('>', '').replace('#', '')

        global guild_id

        channel_id_database = []

        for guild_id in c.execute(f'SELECT channel_id FROM settings WHERE server_id = {ctx.message.guild.id}'):
            channel_id_database.append(guild_id[0])

        if int(channel_id) in channel_id_database:

            c.execute(''' DELETE from settings where channel_id = ? ''', (ctx.message.channel.id,))
            conn.commit()

            embed = discord.Embed(description=f"Ghost Ping Alert is now enabled on <#{channel_id}>!", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(title='Error!', description=f"Ghost Ping Alert was never disabled on <#{channel_id}> before!", colour=cogs.functions.embedColour())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Settings(bot))

