import os
import json
import asyncio
import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='.', help_command=commands.DefaultHelpCommand(), intents=intents)
totalPages = 0

def load_config(file_path):
    with open(file_path) as file:
      config = json.load(file)
    return config

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    activity = discord.Activity(
        name="左經",
        type=discord.ActivityType.listening
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and ctx.message.content[1].isalpha() == True:
        embed = discord.Embed(title='Invalid Command', color=discord.Color.red())
        embed.add_field(name='Invalid cmd', value=f"The command `{ctx.message.content}` is not found in `main.py`")
        await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1153623930892976128)
    await channel.send(f"{member.mention}, Welcome to the server of **SMS Programming Team**.")
    
@bot.event
async def setup_hook():
    for filename in os.listdir("./cog"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cog.{filename[:-3]}")

bot.run(config.get("discord", "token"))

# @bot.command()
# async def temp(ctx):
#     id = 1171453621175595119
#     await ctx.send(f"<:finish_task:{id}>")
