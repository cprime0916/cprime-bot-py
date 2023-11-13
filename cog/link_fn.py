import discord
import json
from discord.ext import commands
from discord import Embed
import requests
import sqlite3
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
dbf = 'database.db'
db = sqlite3.connect(dbf)
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
class link_fn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_codeforces_username(self, username):
        api_url = f"https://codeforces.com/api/user.info?handles={username}"
        response = requests.get(api_url)
        data = response.json()
        return response.status_code == 200 and data['status'] == 'OK' and data['result']
    
    @commands.command()
    async def link(self,ctx, username):
        is_username_valid = self.check_codeforces_username(username)
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

    @commands.group() # commands to unlink all codeforces acc
    async def unlink(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='ERROR', color=discord.Color.red())
            embed.add_field(name='Invalid command of `.unlink`', value='Use `.help unlink` for commands')
            await ctx.send(embed=embed)

    @unlink.command()
    async def all(self, ctx):
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
    async def user(self, ctx, cfUser):
        print('I am summoned')
        discord_id = ctx.message.author.id
        cf = cfUser
        sql = "DELETE FROM accounts WHERE discord_id = ? AND cf = ?"
        print('?')
        val = (discord_id, cf,)
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

async def setup(bot):
    await bot.add_cog(link_fn(bot))