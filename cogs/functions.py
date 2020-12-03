import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('bot.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

c.execute('''CREATE TABLE IF NOT EXISTS server (`server_id` INT PRIMARY KEY, `embed` STR) ''')

async def requestEmbedTemplate(ctx, description, author):
    embed = discord.Embed(description=f"{description}", colour=embedColour())
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    return await ctx.send(embed=embed)

async def errorEmbedTemplate(ctx, description, author):
    embed = discord.Embed(description=f"<:error:769707642670022686> {description}", colour=embedColour())
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    return await ctx.send(embed=embed)

async def successEmbedTemplate(ctx, description, author):
    embed = discord.Embed(description=f"<a:checkmark:768632370580291616> {description}", colour=embedColour())
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    return await ctx.send(embed=embed)

def embedColour():
    colourEmbedInt = int("0xdecaf0", 16)
    return colourEmbedInt

def createGuildProfile(ID):
    c.execute(''' INSERT OR REPLACE INTO server VALUES (?, ?) ''', (ID, "0xdecaf0"))
    conn.commit()
    print(f"Added for {ID} into guild database.")


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_database = [row for row in c.execute('SELECT server_id FROM server')]

        if guild.id not in guild_database:
            createGuildProfile(guild.id)


    @commands.Cog.listener()
    async def on_ready(self):
        guild_database = [row[0] for row in c.execute('SELECT server_id FROM server')]

        for guild in self.bot.guilds:
            if guild.id not in guild_database:
                createGuildProfile(guild.id)




def setup(bot):
    bot.add_cog(Functions(bot))