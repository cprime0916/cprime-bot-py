import os
import json
import asyncio
import datetime
import discord
from discord.ext import commands
import configparser
import random

config = configparser.ConfigParser()
config.read('config.ini')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
totalPages = 0

bot.remove_command("help")

def load_config(file_path):
    with open(file_path) as file:
      config = json.load(file)
    return config

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    activity = discord.Activity(
        name="左經",
        type=discord.ActivityType.custom
    )
    await bot.change_presence(activity=activity)

@bot.command()
@commands.is_owner()
async def reload_cog(ctx, cog_name):
    try:
        await bot.reload_extension(cog_name)
        await ctx.send(f"The cog `{cog_name}` has been reloaded.")
    except commands.ExtensionError as e:
        await ctx.send(f"An error occurred while reloading the cog: {e}")

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


bot.run(config.get("discord", "token"))
