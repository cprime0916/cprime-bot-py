import discord
import datetime
from discord.ext import commands
from discord import Embed
import requests
import sqlite3
import json
from contests_fn import getcn
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', help_command=commands.DefaultHelpCommand(), intents=intents)
totalPages = 0
dbf = 'database.db'
db = sqlite3.connect(dbf)
hosts = ["codeforces.com", "atcoder.jp"]
upcoming_contests = getcn(hosts)
# Create a cursor to execute SQL statements
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id INTEGER,
        acc_link TEXT,
        username TEXT
    )
""")
db.commit()

def load_config(file_path):
    with open(file_path) as file:
      config = json.load(file)
    return config

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    activity = discord.Activity(
        name="Leftian Scriptures",
        type=discord.ActivityType.listening
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and ctx.message.content[1].isalpha() == True:
        embed = discord.Embed(title='Invalid Command', color=discord.Color.red())
        embed.add_field(name='Invalid cmd', value=f"The command `{ctx.message.content}` is not found in `main.py`")
        await ctx.send(embed=embed)


def check_codeforces_username(username):
  api_url = f"https://codeforces.com/api/user.info?handles={username}"
  response = requests.get(api_url)
  data = response.json()
  return response.status_code == 200 and data['status'] == 'OK' and data['result']

@bot.command()
async def contests(ctx):
  print("run func")
  hosts = ["codeforces.com", "atcoder.jp"]
  upcoming_contests = getcn(hosts)

  page_size = 5
  total_pages = (len(upcoming_contests) + page_size - 1) // page_size
  totalPages = total_pages
  emoji_list = ["⬅️", "➡️"] 

  current_page = 0

  def generate_embed(page):
      start_index = page * page_size
      end_index = min((page + 1) * page_size, len(upcoming_contests))

      embed = discord.Embed(title=f"Upcoming Contests (Page {page + 1}/{total_pages})", color=discord.Color.blue())

      for i in range(start_index, end_index):
          contest = upcoming_contests[i]
          embed.add_field(name=f"{contest['event']}", value=f"Start Time: {contest['start']}\n[Contest Link]({contest['href']})", inline=False)

      return embed

  message = await ctx.send(embed=generate_embed(current_page))

  for emoji in emoji_list:
      await message.add_reaction(emoji)

  def check(reaction, user):
      return (
          user == ctx.message.author
          and reaction.message.id == message.id
          and str(reaction.emoji) in emoji_list
      )

  while True:
      try:
          reaction, user = await bot.wait_for(
              "reaction_add", check=check
          )

          if str(reaction.emoji) == emoji_list[0]:  # Previous page
              current_page -= 1
              if current_page < 0:
                  current_page = total_pages - 1
              await message.edit(embed=generate_embed(current_page))

          elif str(reaction.emoji) == emoji_list[1]:  # Next page
              current_page += 1
              if current_page == total_pages:
                  current_page = 0
              await message.edit(embed=generate_embed(current_page))

          await message.remove_reaction(reaction, user)

      except TimeoutError as e:
          print(f"{e}")
          break

@bot.command()
async def link(ctx, username):
  is_username_valid = check_codeforces_username(username)
  if not is_username_valid:
      embed = discord.Embed(title='ERROR', color=discord.Color.red()) # ERR EMBED
      embed.add_field(name='Invalid Codeforces username', value=username)
      await ctx.send(embed=embed)
  else:
      # Insert the link into the database
      discord_id = ctx.message.author.id
      acc_link = "https://codeforces.com/profile/" + username
      sql = "INSERT INTO accounts (discord_id, acc_link, username) VALUES (?, ?, ?)"
      val = (discord_id, acc_link, username)
      cursor.execute(sql, val)
      db.commit()

      # Build and send a success embed message
      embed = discord.Embed(title='Success', color=discord.Color.green())
      embed.add_field(name='Codeforces account linked', value=username)
      await ctx.send(embed=embed)

@bot.group() # commands to unlink all codeforces acc
async def unlink(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title='ERROR', color=discord.Color.red())
        embed.add_field(name='Invalid command of `.unlink`', value='Use `.help unlink` for commands')
        await ctx.send(embed=embed)

@unlink.command()
async def all(ctx):
    discord_id = ctx.message.author.id
    sql = "DELETE FROM accounts WHERE discord_id = ?"
    val = (discord_id,)
    cursor.execute(sql, val)
    db.commit()
    if cursor.rowcount > 0:
        embed = discord.Embed(title='Success', color=discord.Color.green())
        embed.add_field(name='All codeforces accounts unlinked', value=f"Discord ID: {discord_id}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='ERROR', color=discord.Color.red())
        embed.add_field(name='No account linked', value=f"Discord ID: {discord_id}")
        await ctx.send(embed=embed)

@unlink.command()
async def user(ctx, cfUser):
    print('I am summoned')
    discord_id = ctx.message.author.id
    cf = cfUser
    sql = "DELETE FROM accounts WHERE discord_id = ? AND cf = ?"
    print('?')
    val = (discord_id, cf)
    print('?2')
    cursor.execute(sql, val)
    print('?3')
    db.commit()
    # print('?')
    if cursor.rowcount > 0:
        embed = discord.Embed(title='Success', color=discord.Color.green())
        embed.add_field(name=f'Unlinked {cfUser} from {ctx.message.author.name}', value=f"Discord ID: {discord_id}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='ERROR', color=discord.Color.red())
        embed.add_field(name=f'This account may not be linked to {ctx.message.author.name}', value=f"Discord ID: {discord_id}")
        await ctx.send(embed=embed)

emoji_list = ["⬅️", "➡️"] 
def generate_embed(page, total_pages, upcoming_contests):
    page_size = 10
    start_index = page * page_size
    end_index = min((page + 1) * page_size, len(upcoming_contests))

    embed = discord.Embed(title=f"Upcoming Contests (Page {page + 1}/{total_pages})", color=discord.Color.blue())

    for i in range(start_index, end_index):
        contest = upcoming_contests[i]
        embed.add_field(name=f"{contest['event']}", value=f"Start Time: {contest['start']}\n[Contest Link]({contest['href']})", inline=False)

    return embed

@bot.command()
async def set(ctx, time):
    pass

bot.run('MTE2NjcwNDA3MjY5MTI5MDE3Mw.GyCnFK.uWf0lgcFs4M6w9MMInT41NafhKKrMmR31FrJ4k')