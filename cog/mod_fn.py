import sqlite3
import configparser
import requests
import discord
from discord.ext import commands
modlist = [1045289757040722021]
config = configparser.ConfigParser()
config.read('config.ini')
dbf = 'database.db'
db = sqlite3.connect(dbf)
cursor = db.cursor()
db.commit()
class mod_fn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def check_codeforces_username(self, username):
        api_url = f"https://codeforces.com/api/user.info?handles={username}"
        response = requests.get(api_url)
        data = response.json()
        return response.status_code == 200 and data['status'] == 'OK' and data['result']
    @commands.command()
    async def delete_ln(self, ctx, user):
        if ctx.message.author.id not in modlist:
            embed = discord.Embed(title='ERROR', color=discord.Color.red())
            embed.add_field(name='Invalid User', value=f"Initialized user not in moderator list\nDiscord ID: {ctx.message.author.id}")
            await ctx.send(embed=embed)
        else:
            discord_id = user
            sql = "DELETE FROM accounts WHERE discord_id = ?"
            val = (discord_id,)
            cursor.execute(sql, val)
            db.commit()
            if cursor.rowcount > 0:
                embed = discord.Embed(title='Success', color=discord.Color.green())
                embed.add_field(name='All codeforces accounts unlinked', value=f"Mod ID: {discord_id}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='ERROR', color=discord.Color.red())
                embed.add_field(name='No account linked', value=f"Mod ID: {discord_id}")
                await ctx.send(embed=embed)

    @commands.command()
    async def add_ln(self, ctx, id, cfUser):
        if ctx.message.author.id not in modlist:
            embed = discord.Embed(title='ERROR', color=discord.Color.red())
            embed.add_field(name='Invalid User', value=f"Initialized user not in moderator list\nDiscord ID: {ctx.message.author.id}")
            await ctx.send(embed=embed)
        else:
            if not self.check_codeforces_username(cfUser):
                embed = discord.Embed(title='ERROR', color=discord.Color.red()) # ERR EMBED
                embed.add_field(name='Invalid Codeforces username', value=cfUser)
                await ctx.send(embed=embed)
            else:
                acc_link = "https://codeforces.com/profile/" + cfUser
                sql = "INSERT INTO accounts (discord_id, acc_link, username) VALUES (?, ?, ?)"
                val = (id, acc_link, cfUser)
                cursor.execute(sql, val)
                db.commit()
                embed = discord.Embed(title='Success', color=discord.Color.green())
                embed.add_field(name='Codeforces account linked', value=cfUser)
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(mod_fn(bot))