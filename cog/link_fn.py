import discord
import json
from discord.ext import commands
from discord import Embed
from lxml import html
import requests
import sqlite3
import configparser
API_URL = "https://codeforces.com/api/user.status"
PROFILE_URL = "https://codeforces.com/profile"
config = configparser.ConfigParser()
config.read("config.ini")
dbf = "database.db"
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
        return response.status_code == 200 and data["status"] == "OK" and data["result"]

    @commands.command()
    async def link(self,ctx, username):
        is_username_valid = self.check_codeforces_username(username)
        if not is_username_valid:
            embed = discord.Embed(title="ERROR", color=discord.Color.red()) # ERR EMBED
            embed.add_field(name="Invalid Codeforces username <:wa:1172511313168175235>", value=username)
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
            embed = discord.Embed(title="Success", color=discord.Color.green())
            embed.add_field(name="Codeforces account linked", value=username)
            await ctx.send(embed=embed)

    @commands.group() # commands to unlink all codeforces acc
    async def unlink(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name="Invalid command of `.unlink` <:wa:1172511313168175235>", value="Use `.help unlink` for commands")
            await ctx.send(embed=embed)

    @unlink.command()
    async def all(self, ctx):
        discord_id = ctx.message.author.id
        sql = "DELETE FROM accounts WHERE discord_id = ?"
        val = (discord_id,)
        cursor.execute(sql, val)
        db.commit()
        if cursor.rowcount > 0:
            embed = discord.Embed(title="Success", color=discord.Color.green())
            embed.add_field(name="All codeforces accounts unlinked", value=f"Discord ID: {discord_id}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name="No account linked <:wa:1172511313168175235>", value=f"Discord ID: {discord_id}")
            await ctx.send(embed=embed)

    @unlink.command()
    async def user(self, ctx, cfUser):
        print("I am summoned")
        discord_id = ctx.message.author.id
        cf = cfUser
        sql = "DELETE FROM accounts WHERE discord_id = ? AND username = ?"
        print("?")
        val = (discord_id, cf,)
        print("?2")
        cursor.execute(sql, val)
        print("?3")
        db.commit()
        # print("?")
        if cursor.rowcount > 0:
            embed = discord.Embed(title="Success", color=discord.Color.green())
            embed.add_field(name=f"Unlinked {cfUser} from {ctx.message.author.name}", value=f"Discord ID: {discord_id}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name=f"This account may not be linked to {ctx.message.author.name}", value=f"Discord ID: {discord_id}")
            await ctx.send(embed=embed)
    @commands.command()
    async def linked(self, ctx):
        discord_id = ctx.message.author.id
        sql = "SELECT username FROM accounts WHERE discord_id = ?"
        print("?")
        val = (discord_id,)
        print("?2")
        cursor.execute(sql, val)
        db.commit()
        results = cursor.fetchall()
        print("?3")
        if results:
            print("?4")
            usernames = [result[0] for result in results]
            usernames = set(usernames)
            embed = discord.Embed(title="Linked accounts", description="\n".join(usernames), color=discord.Color.green())
            embed.add_field(name="Discord ID", value=discord_id)
            await ctx.send(embed=embed)
        else:
            print("?4.2")
            embed = discord.Embed(title="ERROR", name="No linked accounts", value=f"{discord_id}")
            await ctx.send(embed=embed)

    @commands.command()
    async def ac(self, ctx):
        # print("ac run")
        discordID = ctx.message.author.id
        discordName = ctx.message.author.name
        err = 0
        usernameList = []
        sql = "SELECT username FROM accounts WHERE discord_id = ?"
        val = (discordID,)
        cursor.execute(sql, val)
        db.commit()
        results = cursor.fetchall()
        usernames = [result[0] for result in results]
        # print(usernames)
        usernames = set(usernames)
        for username in usernames:
            response = requests.get(f"{PROFILE_URL}/{username}")
            # print(response.status_code)
            # print("diu lei lou mou")
            if response.status_code == 200:
                content = response.content
                # print("?1")
                tree = html.fromstring(content)
                # print("?2")
                element = tree.xpath('//*[@id="pageContent"]/div[4]/div/div[3]/div[1]/div[1]/div[1]')
                if element:
                    # print("?3")
                    ac = element[0].text_content()
                    ac = ac.replace(" problems", "")
                    usernameList.append((username, ac))
                else:
                    # print("?3.2")
                    err = 2
            else:
                err = 1
        if err == 1:
            embed = discord.Embed(title="ERROR", name="Abnormal response signal", value=f"{discordID}", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif err == 2:
            embed = discord.Embed(title="ERROR", name="Element not found at XPath", value=f"{discordID}", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            # print("?69")
            embed = discord.Embed(title=f"{ctx.author.name}'s AC count", description="\n".join([' '.join(t) for t in usernameList]), color=discord.Color.blue())
            await ctx.send(embed=embed)
    
    # @commands.command()
    # async def rank(self, ctx):
    #     userList = []
    #     sql = "SELECT username FROM accounts"
    #     cursor.execute(sql)
    #     cfRets = cursor.fetchall()
    #     db.commit()
    #     globunames = [result[0] for result in cfRets]
    #     globunames = set(globunames)
    #     for usernames in globunames:


            
                



async def setup(bot):
    await bot.add_cog(link_fn(bot))