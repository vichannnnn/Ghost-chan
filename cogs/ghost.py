from discord.ext import commands
import discord
import aiohttp
from io import BytesIO
from PIL import Image
from datetime import datetime
import sqlite3
import cogs.functions

conn = sqlite3.connect('settings.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

class Ghost(commands.Cog, name="Ghost"):

    """ The main function of Ghost-chan! """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.mentions:
            return

        global guild_id
        channel_id_database = [guild_id[0] for guild_id in c.execute(f'SELECT channel_id FROM settings WHERE server_id = {message.guild.id}')]

        if message.channel.id in channel_id_database:  # Only disabled channel will be in channel id database, thus stopping the function if they are triggered in a disabled channel.
            return

        elif message.author.bot:  # Prevents Ghost-chan from issuing alerts from other bot's pinging!
            return

        elif message.content.startswith('!') or message.content.startswith('~') or message.content.startswith('-') or message.content.startswith('.kicker'):
            return

        elif len(message.mentions) > 1:  # Prevents loophole by pinging bot first and then pinging user
            if message.mentions and message.attachments:  # If message deleted has both attachment and mention

                try:
                    embed = discord.Embed(title='Ghost Ping Alert!',
                                          description=f'<@{message.mentions[0].id}>, you have been ghost pinged by <@{message.author.id}> in {message.channel.mention} with the following message: \n\n{message.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                    embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)

                    async with aiohttp.ClientSession() as session:
                        async with session.get(message.attachments[0].url) as response:
                            image_bytes = await response.read()

                    with Image.open(BytesIO(image_bytes)) as my_image:

                        if my_image.mode in ("RGBA", "P"):
                            my_image = my_image.convert("RGB")

                        rotated = my_image.rotate(0, expand=True)
                        buffer = BytesIO()
                        rotated.save(buffer, "jpeg", optimize=True)
                        buffer.seek(0)

                    file = discord.File(fp=buffer, filename="image.jpg")
                    embed.set_image(url="attachment://image.jpg")
                    await message.channel.send(file=file, embed=embed)

                except:
                    embed = discord.Embed(title='Ghost Ping Alert!',
                                          description=f'<@{message.mentions[0].id}>, you have been ghost pinged by <@{message.author.id}> in {message.channel.mention} with the following message: \n\n{message.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                    embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)

            elif message.mentions:  # If message deleted only has mention
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{message.mentions[0].id}>, you have been ghost pinged by <@{message.author.id}> in {message.channel.mention} with the following message: \n\n{message.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)

        elif message.role_mentions: # Prevents role mentions from triggering
            return

        elif message.mention_everyone: # Prevents @everyone and @here mentions from triggering
            return

        elif message.channel_mentions:  # Prevents channel mentions from triggering the bot
            return

        elif message.mentions[0].bot:  # Prevents trigger from just pinging a bot alone
            return

        elif message.mentions and message.attachments:  # If message deleted has both attachment and mention
            try:
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{message.mentions[0].id}>, you have been ghost pinged by <@{message.author.id}> in {message.channel.mention} with the following message: \n\n{message.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)

                async with aiohttp.ClientSession() as session:
                    async with session.get(message.attachments[0].url) as response:
                        image_bytes = await response.read()

                with Image.open(BytesIO(image_bytes)) as my_image:

                    if my_image.mode in ("RGBA", "P"):
                        my_image = my_image.convert("RGB")

                    rotated = my_image.rotate(0, expand=True)
                    buffer = BytesIO()
                    rotated.save(buffer, "jpeg", optimize=True)
                    buffer.seek(0)

                file = discord.File(fp=buffer, filename="image.jpg")
                embed.set_image(url="attachment://image.jpg")
                await message.channel.send(file=file, embed=embed)

            except:
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{message.mentions[0].id}>, you have been ghost pinged by <@{message.author.id}> in {message.channel.mention} with the following message: \n\n{message.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)


        elif message.mentions:  # If message deleted only has mention
            try:
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{message.mentions[0].id}>, you have been ghost pinged by <@{message.author.id}> in {message.channel.mention} with the following message: \n\n{message.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)

            except:
                embed = discord.Embed(title='Ghost Ping Alert!', description=f'{message.content}', colour=cogs.functions.embedColour(),
                                      timestamp=datetime.utcnow())
                embed.add_field(name="User mentioned:", value=f"<@{message.mentions[0].id}>")
                embed.set_footer(text="Message ID: " + str(message.id), icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not before.mentions and not after.mentions:
            return

        global guild_id
        channel_id_database = [guild_id[0] for guild_id in c.execute(f'SELECT channel_id FROM settings WHERE server_id = {before.guild.id}')]

        if before.channel.id in channel_id_database:  # Only disabled channel will be in channel id database, thus stopping the function if they are triggered in a disabled channel.
            return

        elif before.author.bot or after.author.bot: # Prevents bot from interacting
            return

        elif before.channel_mentions: # Prevents channel mentions from triggering
            return

        elif before.mentions and after.mentions: # This is to prevent legitimate typo message edit cases from triggering
            return

        elif len(before.mentions) > 1:  # Prevents loophole by pinging bot first and then pinging user
            if before.mentions and before.attachments:  # If message deleted has both attachment and mention
                try:
                    embed = discord.Embed(title='Ghost Ping Alert!',
                                          description=f'<@{before.mentions[0].id}>, you have been ghost pinged by <@{before.author.id}> in {before.channel.mention} with the following message: \n\n{before.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())

                    embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)

                    async with aiohttp.ClientSession() as session:
                        async with session.get(before.attachments[0].url) as response:
                            image_bytes = await response.read()

                    with Image.open(BytesIO(image_bytes)) as my_image:
                        if my_image.mode in ("RGBA", "P"):
                            my_image = my_image.convert("RGB")

                        rotated = my_image.rotate(0, expand=True)
                        buffer = BytesIO()
                        rotated.save(buffer, "jpeg", optimize=True)
                        buffer.seek(0)

                    file = discord.File(fp=buffer, filename="image.jpg")
                    embed.set_image(url="attachment://image.jpg")
                    await before.channel.send(file=file, embed=embed)


                except:
                    embed = discord.Embed(title='Ghost Ping Alert!',
                                          description=f'<@{before.mentions[0].id}>, you have been ghost pinged by <@{before.author.id}> in {before.channel.mention} with the following message: \n\n{before.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                    embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)
                    await before.channel.send(embed=embed)

            elif before.mentions:  # If before deleted only has mention
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{before.mentions[0].id}>, you have been ghost pinged by <@{before.author.id}> in {before.channel.mention} with the following message: \n\n{before.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)
                await before.channel.send(embed=embed)

        elif before.channel_mentions:  # Prevents channel mentions from triggering the bot
            return

        elif before.role_mentions: # Prevents role mention from triggering
            return

        elif before.mention_everyone: # Prevents @everyone and @here from triggering
            return

        elif before.channel_mentions:  # Prevents channel mentions from triggering the bot
            return

        elif before.mentions[0].bot:  # Prevents trigger from just pinging a bot alone
            return

        elif before.mentions and before.attachments:  # If before deleted has both attachment and mention
            try:
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{before.mentions[0].id}>, you have been ghost pinged by <@{before.author.id}> in {before.channel.mention} with the following message: \n\n{before.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)

                async with aiohttp.ClientSession() as session:
                    async with session.get(before.attachments[0].url) as response:
                        image_bytes = await response.read()

                with Image.open(BytesIO(image_bytes)) as my_image:
                    if my_image.mode in ("RGBA", "P"):
                        my_image = my_image.convert("RGB")

                    rotated = my_image.rotate(0, expand=True)
                    buffer = BytesIO()
                    rotated.save(buffer, "jpeg", optimize=True)
                    buffer.seek(0)

                file = discord.File(fp=buffer, filename="image.jpg")
                embed.set_image(url="attachment://image.jpg")
                await before.channel.send(file=file, embed=embed)


            except:
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{before.mentions[0].id}>, you have been ghost pinged by <@{before.author.id}> in {before.channel.mention} with the following message: \n\n{before.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)
                await before.channel.send(embed=embed)

        elif before.mentions:  # If edited message contains a mention
            try:
                embed = discord.Embed(title='Ghost Ping Alert!',
                                      description=f'<@{before.mentions[0].id}>, you have been ghost pinged by <@{before.author.id}> in {before.channel.mention} with the following message: \n\n{before.content}', colour=cogs.functions.embedColour(), timestamp=datetime.utcnow())
                embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)
                await before.channel.send(embed=embed)

            except:
                embed = discord.Embed(title='Ghost Ping Alert!', description=f'{before.content}', colour=cogs.functions.embedColour(),
                                      timestamp=datetime.utcnow())
                embed.add_field(name="User mentioned:", value=f"<@{before.mentions[0].id}>")
                embed.set_footer(text="Message ID: " + str(before.id), icon_url=before.author.avatar_url)
                await before.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Ghost(bot))
