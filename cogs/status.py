import discord
import random
from discord.ext import tasks, commands
import traceback



class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    @tasks.loop(seconds=600)
    async def change_status(self):

        try:
            m = sum(guild.member_count for guild in self.bot.guilds)
            m2 = ('{:,}'.format(m))
            name = [f"=w=help | Exorcising {len([s for s in self.bot.guilds])} servers!", "and exorcising the ghosts!", "for your ghost pings..", "Violet-chan struggling with bugs!", "https://himaa.xyz", "Hima..?"]
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(name)))   # Ghost-chan's playing status
        except:
            traceback.print_exc()

    @change_status.before_loop
    async def before_status(self):
        print('Waiting...')
        await self.bot.wait_until_ready()



def setup(bot):
    bot.add_cog(Status(bot))
