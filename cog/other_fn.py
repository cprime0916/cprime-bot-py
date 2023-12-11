import discord
from discord.ext import commands
import configparser
import random
config = configparser.ConfigParser()
config.read('config.ini')

class other_fn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def agree(self, ctx):
        await ctx.message.delete()
        det = random.randint(1, 5)
        if det == 1:
            await ctx.send("Indeed")
        elif det == 2:
            await ctx.send("fr")
        elif det == 3:
            await ctx.send("yeah")
        elif det == 4:
            await ctx.send("facts")
        elif det == 5:
            await ctx.send("Real")

    @commands.command()
    async def say(self, ctx, *, s):
        await ctx.message.delete()
        if s != "`prayer`":
            await ctx.send(f"{s}")
        else:
            await ctx.send('''oh Left is so genius it is undoubtable that Left is always the truth, the myth, the legendary holy Left. It is our luck that we are blessed by Left and receiving his guidance''')

    @commands.command()
    async def prayer(self, ctx):
        await ctx.send('''oh Left is so genius it is undoubtable that Left is always the truth, the myth, the legendary holy Left. It is our luck that we are blessed by Left and receiving his guidance''')
    
    @commands.command()
    async def quote(self, ctx):
        det = random.randint(1, 3)
        if det == 1:
            await ctx.send(":nerd:")
        elif det == 2:
            q = '"I want, I like, I do."'
            await ctx.send(f"C' said, {q}")
        elif det == 3:
            await ctx.send("random AC technique is the best technique")
    
    @commands.command()
    async def reply(self, ctx, message_id, *, reply_content):
        await ctx.message.delete()
        channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
            await message.reply(reply_content)
        except discord.NotFound:
            await ctx.send("Message not found.")

async def setup(bot):
    await bot.add_cog(other_fn(bot))