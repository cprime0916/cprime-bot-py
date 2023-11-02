import discord
from discord.ext import commands
from discord import Embed
import requests
import sqlite3
import json
from contests_fn import getcn
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', help_command=commands.DefaultHelpCommand(), intents=intents)

dbf = 'database.db'
db = sqlite3.connect(dbf)
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
async def contests(self, ctx):
  hosts = ["codeforces.com", "atcoder.jp"]
  upcoming_contests = getcn(hosts)

  page_size = 3
  total_pages = (len(upcoming_contests) + page_size - 1) // page_size

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
          reaction, user = await self.bot.wait_for(
              "reaction_add", timeout=60.0, check=check
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

      except TimeoutError:
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

bot.run('MTE2NjcwNDA3MjY5MTI5MDE3Mw.GyCnFK.uWf0lgcFs4M6w9MMInT41NafhKKrMmR31FrJ4k')