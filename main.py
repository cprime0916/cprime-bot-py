import os
import json
import asyncio
import datetime
import discord
from discord.ext import commands
import configparser
import random
from lifetime import lifetime

config = configparser.ConfigParser()
config.read('config.ini')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
activity = discord.Activity(type=discord.ActivityType.listening, name="String Quartet No. 8 in C minor")
bot = commands.Bot(command_prefix='.', activity=activity, intents=intents)
totalPages = 0


def load_config(file_path):
    with open(file_path) as file:
      config = json.load(file)
    return config

# bot events
@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Logged in as', bot.user.name)

@bot.event
async def on_command_error(ctx, error):
    msg = ctx.message.content
    msg = msg.replace(".", "")
    if isinstance(error, commands.CommandNotFound) and msg[0].isalpha() == True:
        embed = discord.Embed(title='Invalid Command', color=discord.Color.red())
        embed.add_field(name='Invalid cmd', value=f"The command `{msg}` is not found in `main.py`")
        await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1153623930892976128)
    await channel.send(f"{member.mention}, Welcome to the server of **SMS Programming Team**.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = message.author.name
        user_id = message.author.id
        s = message.content
        id = message.id
        with open("log.txt", 'a') as f:
            f.write(f"{time} {username} <{user_id}> sent DM {id} (Content: {s})\n")
        det = random.randint(1, 4)
        if det == 1:
            await message.channel.send("屌你老母")
        elif det == 2:
            await message.channel.send("做乜撚嘢DM我啊on9仔")
        elif det == 3:
            await message.channel.send("係唔係咁撚得閒")
        elif det == 4:
            await message.channel.send("dllmch")
    
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    username = ctx.author.name
    user_id = ctx.author.id
    cmd = ctx.command
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", 'a') as f:
        f.write(f"{time} {username} <{user_id}> used command {cmd}.\n")

@bot.event
async def setup_hook():
    for filename in os.listdir("./cog"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cog.{filename[:-3]}")

# bot commands (without class)
@bot.command()
@commands.is_owner()
async def load_cog(ctx, cog):
    try:
        await bot.load_extension(f"cog.{cog}")
        embed = discord.Embed(title="Successful", description="LOAD_COG operation successful.", color=discord.Color.green())
        await ctx.send(embed=embed)
    except commands.ExtensionError as e:
        await ctx.send(f"Error: {e}")

@bot.command()
@commands.is_owner()
async def unload_cog(ctx, cog):
    try:
        await bot.unload_extension(f"cog.{cog}")
        embed = discord.Embed(title="Successful", description="UNLOAD_COG operation successful.", color=discord.Color.green())
        await ctx.send(embed=embed)
    except commands.ExtensionError as e:
        await ctx.send(f"Error: {e}")

@bot.command()
@commands.is_owner()
async def reload_cog(ctx, cog):
    try:
        await bot.reload_extension(f"cog.{cog}")
        await ctx.send(f"The cog `{cog}` has been reloaded.")
    except commands.ExtensionError as e:
        await ctx.send(f"Error: {e}")

lifetime()
bot.run(config.get("discord", "token"))
