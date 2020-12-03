import sqlite3

from discord.ext import commands

emoteConn = sqlite3.connect('emotes.db', timeout=5.0)
emoteC = emoteConn.cursor()
emoteConn.row_factory = sqlite3.Row

emoteC.execute('''CREATE TABLE IF NOT EXISTS hug (`gifLink` INT) ''')
emoteC.execute('''CREATE TABLE IF NOT EXISTS kiss (`gifLink` INT) ''')
emoteC.execute('''CREATE TABLE IF NOT EXISTS slap (`gifLink` INT) ''')
emoteC.execute('''CREATE TABLE IF NOT EXISTS poke (`gifLink` INT) ''')
emoteC.execute('''CREATE TABLE IF NOT EXISTS pat (`gifLink` INT) ''')
emoteC.execute('''CREATE TABLE IF NOT EXISTS lick (`gifLink` INT) ''')

class ownerCommands(commands.Cog, name="Owner Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def hugadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO hug VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def kissadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO kiss VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def slapadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO slap VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def pokeadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO poke VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def patadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO pat VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def lickadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO lick VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")

    @commands.command(description="Bla bla bla bla.")
    @commands.is_owner()
    async def biteadd(self, ctx, link):
        emoteC.execute('''INSERT OR REPLACE INTO bite VALUES (?) ''', (link,))
        emoteConn.commit()

        await ctx.send("Added!")


def setup(bot):
    bot.add_cog(ownerCommands(bot))
