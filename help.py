import discord
from discord.ext import commands
import sqlite3
from cogs.functions import embedColour

conn = sqlite3.connect('prefix.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row


class Help(commands.Cog, name="Help"):

    def __init__(self, bot):
        self.bot = bot
        print("help.py extension has loaded!")

    commands.command(
        name='help',
        description='The help command!',
        aliases=['commands', 'command'],
        usage='cog'
    )

    @commands.command()
    async def help(self, ctx):

        reactions = ['🛠️', '📝', '🎲', 'ℹ️', '<:hug:783848710353453077>']
        reactionsCogs = ["🛠️ Settings", "📝 Moderation", "🎲 Fun", 'ℹ️ Info', "<:hug:783848710353453077> Emotes"]

        cogs = [cog for cog in self.bot.cogs.keys()]

        prefixDictionary = {}

        for prefix in c.execute(f'SELECT guild_id, prefix FROM prefix'):
            prefixDictionary.update({prefix[0]: f"{prefix[1]}"})

        currentPrefix = prefixDictionary[ctx.message.guild.id]

        embed = discord.Embed(description=f"Type `{currentPrefix}myprefix` for this server's prefix.\nType `{currentPrefix}setprefix` to change the prefix for this server.", colour=embedColour())
        embed.set_author(name=f"{str(self.bot.user).partition('#')[0]}'s Commands and Help", icon_url=self.bot.user.avatar_url)
        embed.set_footer(
            text=f"React for more category help! :: {ctx.message.guild}'s prefix currently is {currentPrefix}",
            icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        hidden_cogs = ['Help', 'Functions', 'Jishaku', 'Status', 'TopGG', 'Delurking', 'Delurking2', 'TeaParty', "Owner Commands", 'Ghost']

        for cog in cogs:
            if cog not in hidden_cogs:

                cog_commands = self.bot.get_cog(cog).get_commands()
                commands_list = ''

                for comm in cog_commands:
                    description = comm.description.replace("`", "").replace("**", "")
                    commands_list += f'[`{comm}`](http://himaa.xyz/ghost-chan/#commands "{currentPrefix}{description}") '

                embed.add_field(name=cog, value=commands_list, inline=False)

        msg = await ctx.send(embed=embed)

        for react in reactions:
            await msg.add_reaction(react)

        def check(reaction, user):
            return str(reaction.emoji) in reactions and user == ctx.message.author and reaction.message.id == msg.id

        async def handle_reaction(reaction, msg, check):
            await msg.remove_reaction(reaction, ctx.message.author)
            reactionIndex = reactions.index(str(reaction.emoji))

            if str(reaction.emoji) == reactions[reactionIndex]:

                help_embed = discord.Embed(title=f'{reactionsCogs[reactionIndex]} Help', colour=embedColour())
                embed.set_footer(
                    text=f"React for more category help! :: {ctx.message.guild}'s prefix currently is {currentPrefix}",
                    icon_url=self.bot.user.avatar_url)

                cog_commands = self.bot.get_cog(f"{reactionsCogs[reactionIndex]}").get_commands()
                commands_list = ''

                for comm in cog_commands:

                    commands_list += f'**{comm.name}** - {comm.description}\n'
                    help_embed.add_field(name=comm, value=f"**{currentPrefix}{comm.description}", inline=True)
                await msg.edit(embed=help_embed)

            else:
                return

            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            await handle_reaction(reaction, msg, check)

        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
        await handle_reaction(reaction, msg, check)


def setup(bot):
    bot.add_cog(Help(bot))
