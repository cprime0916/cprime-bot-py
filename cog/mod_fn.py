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

async def setup(bot):
    await bot.add_cog(mod_fn(bot))