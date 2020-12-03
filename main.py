import discord
import math
from discord.ext import commands
from discord.ext.commands import has_permissions
import sqlite3
from authentication import bot_token
from datetime import datetime
import pytz
import traceback
import os
import cogs.functions
import platform

now = int(datetime.now(pytz.timezone("Singapore")).timestamp())

conn = sqlite3.connect('prefix.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

help_extensions = ['help']


c.execute('''CREATE TABLE IF NOT EXISTS prefix (
        `guild_id` INT PRIMARY KEY,
        `prefix` TEXT)''')

async def determine_prefix(bot, message):

    try:
        currentPrefix = prefixDictionary[message.guild.id]
        return commands.when_mentioned_or(currentPrefix)(bot, message)
    except KeyError:
        c.execute(''' INSERT OR REPLACE INTO prefix VALUES (?, ?)''', (message.guild.id, defaultPrefix))
        conn.commit()
        prefixDictionary.update({message.guild.id: defaultPrefix})
        print(f"Error Detected: Created a prefix database for {message.guild.id}: {message.guild}")
        return commands.when_mentioned_or(defaultPrefix)(bot, message)
    except AttributeError:
        print("DM Error has occurred on user-end.")
    except:
        traceback.print_exc()


bot = commands.AutoShardedBot(command_prefix=determine_prefix, help_command=None)
bot.load_extension("jishaku")

defaultPrefix = '=w='

for cog in os.listdir("cogs"):
    try:
        if cog == '__pycache__':
            continue

        if cog.endswith('.db'):
            continue

        else:
            newCog = cog.replace(".py", "")
            bot.load_extension(f"cogs.{newCog}")
            print(f'{cog} successfully loaded!')

    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension {cog}\n{exc}')
        traceback.print_exc()


@bot.command(help="Loads an extension. Bot Owner only!")
@commands.is_owner()
async def load(ctx, extension_name: str):
    try:
        bot.load_extension(extension_name)

    except (AttributeError, ImportError) as e:
        await ctx.send(f"```py\n{type(e).__name__}: {str(e)}\n```")
        return

    await ctx.send(f"{extension_name} loaded.")


@bot.command(help="Unloads an extension. Bot Owner only!")
@commands.is_owner()
async def unload(ctx, extension_name: str):
    bot.unload_extension(extension_name)
    await ctx.send(f"{extension_name} unloaded.")


@bot.command()
@has_permissions(manage_messages=True)
async def setprefix(ctx, new):
    guild = ctx.message.guild.id
    name = bot.get_guild(guild)

    for key, value in c.execute('SELECT guild_id, prefix FROM prefix'):

        if key == guild:
            c.execute(''' UPDATE prefix SET prefix = ? WHERE guild_id = ? ''', (new, guild))
            conn.commit()
            prefixDictionary.update({ctx.guild.id: f"{new}"})

            embed = discord.Embed(description=f"{name}'s Prefix has now changed to `{new}`.")
            await ctx.send(embed=embed)


@bot.command()
async def myprefix(ctx):
    c.execute(f'SELECT prefix FROM prefix WHERE guild_id = {ctx.message.guild.id}')
    currentPrefix = c.fetchall()[0][0]

    name = bot.get_guild(ctx.message.guild.id)
    embed = discord.Embed(description=f"{name}'s Prefix currently is `{currentPrefix}`.")
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f"Logging in as {str(bot.user)}")
    print(f"{str(bot.user)} has connected to Discord!")
    print(f"Current Discord Version: {discord.__version__}")
    print(f"Number of servers currently connected to {str(bot.user)}:")
    print(len([s for s in bot.guilds]))
    print(f"Number of players currently connected to {str(bot.user)}:")
    print(sum(guild.member_count for guild in bot.guilds))

    guild_id_database = [row[0] for row in c.execute('SELECT guild_id FROM prefix')]

    async for guild in bot.fetch_guilds():

        if guild.id not in guild_id_database:
            c.execute(''' INSERT OR REPLACE INTO prefix VALUES (?, ?)''', (guild.id, defaultPrefix))
            conn.commit()
            prefixDictionary.update({guild.id: defaultPrefix})
            print(f"Bot started up: Created a prefix database for {guild.id}: {guild}")


prefixDictionary = {}

for prefix in c.execute(f'SELECT guild_id, prefix FROM prefix'):
    prefixDictionary.update({prefix[0]: f"{prefix[1]}"})

@bot.event
async def on_guild_join(guild):

    guild_id_database = [row[0] for row in c.execute('SELECT guild_id FROM prefix')]

    if guild.id not in guild_id_database:
        c.execute(''' INSERT OR REPLACE INTO prefix VALUES (?, ?)''', (guild.id, defaultPrefix))
        conn.commit()
        prefixDictionary.update({guild.id: f"{defaultPrefix}"})
        print(f"Bot joined a new server: Created a prefix database for {guild.id}: {guild}")

    embed = discord.Embed(
        description=f"Hello **{guild.name}**!\n\n**Ghost-chan** here, a~~n Exorcist~~ Bot built by **{bot.get_user(624251187277070357)}** to guard your server from ghost pings! Thank you for adding me into your server!\n\nYou may type `=w=help` or `@Ghost-chan#1718 help` for more details about my commands!", colour=cogs.functions.embedColour())
    embed.set_thumbnail(url="https://i.imgur.com/3Lgs39V.png")
    embed.set_footer(text=f"Made with Discord.py :: {discord.__version__} and Python :: {platform.python_version()}",
                     icon_url="https://i.imgur.com/UzTCxvF.png")
    await guild.system_channel.send(embed=embed)
    demoEmbed = discord.Embed(colour=cogs.functions.embedColour())
    demoEmbed.set_image(url="https://i.imgur.com/RZSmdM1.gif")
    await guild.system_channel.send(embed=demoEmbed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):

        seconds = error.retry_after
        minutes = seconds / 60
        hours = seconds / 3600

        if seconds / 60 < 1:

            embed = discord.Embed(
                description=f'You\'re using this command too often! Try again in {str(int(seconds))} seconds!')
            await ctx.send(embed=embed)

        elif minutes / 60 < 1:

            embed = discord.Embed(
                description=f'You\'re using this command too often! Try again in {math.floor(minutes)} minutes and {(int(seconds) - math.floor(minutes) * 60)} seconds!')
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(
                description=f'You\'re using this command too often! Try again in {math.floor(hours)} hours, {(int(minutes) - math.floor(hours) * 60)} minutes, {(int(seconds) - math.floor(minutes) * 60)} seconds!')
            await ctx.send(embed=embed)

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(description='You do not have the permission to do this!')
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description='Missing arguments on your command! Please check and retry again!')
        await ctx.send(embed=embed)
        return

    raise error


@bot.command()
@commands.is_owner()
async def guildcheck(ctx):
    checklist = ''
    try:
        for guild in bot.guilds:
            checklist += f"{guild.name}: {guild.member_count} members"

        embed = discord.Embed(title="Guild List", description=checklist)
        await ctx.send(embed=embed)

    except:
        with open("Output.txt", "w", encoding='utf-8') as text_file:
            for guild in bot.guilds:
                print(f"{guild.name}: {guild.member_count} members\n", file=text_file)
        text_file.close()

@bot.command()
async def ping(ctx):
    embed = discord.Embed(description=f"Pong! Time taken: **{round(bot.latency, 3) * 1000} ms**!")
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def invite(ctx):
    embed = discord.Embed(
        description=f"Hello! **Ghost-chan** here! I'm a~~n Exorcist~~ Bot built by **{bot.get_user(624251187277070357)}**! =w=\n\nYou can add me to your server with the link below:", colour=cogs.functions.embedColour())
    embed.add_field(name="Ghost-chan's Invite Link",
                    value="[**Click here!**](https://discord.com/api/oauth2/authorize?client_id=699457008759472200&permissions=2080762944&scope=bot)",
                    inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/3Lgs39V.png")
    embed.set_footer(
        text="Made with Discord.py :: " + discord.__version__ + " and Python :: " + platform.python_version() + " | " + str(
            ctx.message.author), icon_url="https://i.imgur.com/UzTCxvF.png")
    await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)  # Command that shows the detail of Ghost-chan on Discord
async def about(ctx):

    async for guild in bot.fetch_guilds(limit=150):
        len([s for s in bot.guilds])

    m = sum(guild.member_count for guild in bot.guilds)
    m2 = ('{:,}'.format(m))  # Formatting integers to have , in them (e.g. 99,999)

    seconds = int(datetime.now(pytz.timezone("Singapore")).timestamp()) - now

    minutes = seconds / 60
    hours = seconds / 3600
    days = seconds / 86400

    if seconds < 60:
        uptime = (str(seconds) + str("s"))

    elif 60 < seconds < 3600:
        uptime = f"{math.floor(minutes)}m {(int(seconds) - math.floor(minutes) * 60)}s"

    elif 3600 < seconds < 86400:
        uptime = "{0}h {1}m {2}s".format(math.floor(hours), (int(minutes) - math.floor(hours) * 60), int(seconds) - math.floor(minutes) * 60)

    else:
        uptime = "{0}d {1}h {2}m {3}s".format(math.floor(days), (int(hours) - math.floor(days) * 24), (int(minutes) - math.floor(hours) * 60), int(seconds) - math.floor(minutes) * 60)

    embed = discord.Embed(
        title="👻 About :: Ghost-chan | ID :: 699457008759472200",
        description="Ghost-chan is a simple bot that requires very minimal customization or settings and specializes in protecting your server from ghost pings and trolls!", colour=cogs.functions.embedColour())

    embed.add_field(name="**Info**",
                    value="**Owner:** {0}\n**Uptime:** {1}".format(str(bot.get_user(624251187277070357)), str(uptime),
                                                                   inline=True))
    embed.add_field(name="**Counts**", value="{0} Users\n{1} Servers".format(m2, str(len([s for s in bot.guilds]))),
                    inline=True)
    embed.add_field(name="**Links**",
                    value="[**Ghost-chan's Invite Link**](https://discordapp.com/oauth2/authorize?client_id=699457008759472200&permissions=8&scope=bot)\n[**Vote for Ghost-chan**](https://top.gg/bot/699457008759472200/vote)\n[**Ghost-chan's Website**](https://himaa.xyz/ghost-chan)",
                    inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/3Lgs39V.png")
    embed.set_footer(
        text="Made with Discord.py :: " + discord.__version__ + " and Python :: " + platform.python_version() + " | " + str(
            ctx.message.author), icon_url="https://i.imgur.com/UzTCxvF.png")
    await ctx.send(embed=embed)


bot.remove_command('help')

if __name__ == "__main__":  # Loads all extension specified above on bot start-up.
    for extension in help_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')




bot.run(f'{bot_token}', bot=True, reconnect=True)




