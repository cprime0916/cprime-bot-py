import discord
from discord.ext import commands
from discord import Embed
import requests
import sqlite3
import os
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', help_command=commands.DefaultHelpCommand(), intents=intents)


name = os.environ.get('DATABASE_NAME')
db = sqlite3.connect(str(name))
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
@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)

def check_codeforces_username(username):
  api_url = f"https://codeforces.com/api/user.info?handles={username}"
  response = requests.get(api_url)
  data = response.json()
  return response.status_code == 200 and data['status'] == 'OK' and data['result']

@bot.command()
async def link(ctx, username):
  is_username_valid = check_codeforces_username(username)
  if not is_username_valid:
      # Build and send an embed message
      embed = discord.Embed(title='ERROR', color=discord.Color.red())
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

bot.run('MTE2NjcwNDA3MjY5MTI5MDE3Mw.GLd7W_.7CmHiOdeCrUcApsN0Um09010g7A5ZuFx9bBYoQ')
