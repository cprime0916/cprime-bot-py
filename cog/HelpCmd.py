import discord
from discord.ext import commands
from discord import Embed
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
class HelpCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = Embed(title="Help Command", color=discord.Color.blue(), description="You may visit the documentation below (both work in progress) \n https://github.com/cprime0916/cprime-bot/blob/main/DOC.md \n https://github.com/cprime0916/cprime-bot/wiki")
        embed.add_field(value=f"Discord ID: {ctx.author.id}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCmd(bot))