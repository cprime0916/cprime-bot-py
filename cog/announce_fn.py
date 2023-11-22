import datetime
import configparser
import requests
import discord
from discord.ext import commands
config = configparser.ConfigParser()
config.read('config.ini')
class announce_fn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # @commands.command()
    async def set(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(announce_fn(bot))