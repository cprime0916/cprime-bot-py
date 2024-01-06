import discord
from discord.ext import commands
import configparser
import random
config = configparser.ConfigParser()
config.read('config.ini')

# defining constants
LEFT_PRAYER = "O Left,\nLord of AK,\nwhom leads to the truthful and righteous path.\nmay thou grant us the way to AK,\nthe path with AC'ing tasks in your name,\nMay we work as we worship you.\nIn the name of the mythical and legendary Left.\nAccepted."

class OtherCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.started_assem = False
        self.state = 1
        self.host_id = 0
    
    @commands.command()
    async def agree(self, ctx):
        await ctx.message.delete()
        det = random.randint(1, 5)
        if det == 1:
            await ctx.send("Indeed")
        elif det == 2:
            await ctx.send("fr")
        elif det == 3:
            await ctx.send("yeah")
        elif det == 4:
            await ctx.send("facts")
        elif det == 5:
            await ctx.send("Real")

    @commands.command()
    async def disagree(self, ctx):
        await ctx.message.delete()
        det = random.randint(1, 6)
        if det == 1:
            await ctx.send("nuh uh")
        elif det == 2:
            await ctx.send("naw")
        elif det == 3:
            await ctx.send("not real bruv")
        elif det == 4:
            await ctx.send("hell nah bruv this ain't it")
        elif det == 5:
            await ctx.send("you nigger")
        elif det == 6:
            await ctx.send("no u")
            
    @commands.command()
    async def say(self, ctx, *, s):
        await ctx.message.delete()
        if s != "`prayer`":
            await ctx.send(f"{s}")
        else:
            await ctx.send(LEFT_PRAYER)

    @commands.command()
    async def prayer(self, ctx):
        await ctx.send(LEFT_PRAYER)

    @commands.command()
    async def quote(self, ctx):
        det = random.randint(1, 6)
        if det == 1:
            await ctx.send(":nerd:")
        elif det == 2:
            q = '"I want, I like, I do."'
            await ctx.send(f"C' said, {q}")
        elif det == 3:
            await ctx.send("random AC technique is the best technique")
        elif det == 4:
            q = '"urmom"'
            await ctx.send(f"Momo said, {q}")
        elif det == 5:
            q = '"Less effort you made, more chance to <:ac:1171452943988428802>"'
            await ctx.send(f"Kiu said, {q}")
        elif det == 6:
            q = '"asfaf>>>>?????????ehzdvzdvzdv"'
            await ctx.send(f"partialdiff said, {q}")
    
    @commands.command()
    async def reply(self, ctx, message_id, *, reply_content):
        await ctx.message.delete()
        channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
            await message.reply(reply_content)
        except discord.NotFound:
            await ctx.send("Message not found.")

    @commands.command()
    @commands.cooldown(1, 5.0, commands.BucketType.user) 
    async def spam(self, ctx, text, num):
        await ctx.message.delete()
        if int(num) <= 10 and text[0] != '`':
            for _ in range(0, int(num)):
                await ctx.send(text)
        elif int(num) <= 10:
            if text == "`prayer`":
                for _ in range(0, int(num)):
                    await ctx.send(LEFT_PRAYER)
            else:
                await ctx.send("invalid command prompt.")
        else:
            await ctx.send("In `main.py` line 111, `MAX_LIMIT = 10`")

    @commands.group()
    async def assem(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name="Invalid command of `.assem` <:wa:1172511313168175235>", value="Use `.help assem` for commands")
            await ctx.send(embed=embed)
    
    @assem.command()
    async def start(self, ctx):
        if self.started_assem is False:
            self.started_assem = True
            self.host_id = ctx.author.id
            await ctx.send(f"assem hosted by {ctx.author.mention} officially starts!")
        else:
            await ctx.send("assem already started!")

    @assem.command()
    async def end(self, ctx):
        if self.started_assem is False and ctx.author.id == self.host_id:
            await ctx.send("assem isn't started, you can host one by `.assem start`.")
        elif self.started_assem is False:
            await ctx.send(f"assem's host is {ctx.author.mention}. Only the host is eligible to end ")
        else:
            self.started_assem = False
            await ctx.send("Successfully ended assem.")

    @assem.command()
    async def guide(self, ctx):
        embed = discord.Embed(color=discord.Color.blue(), title="Guide to Assembly")
        embed.add_field(name="Prayer", value="We start the assem with prayers to praise Left, the AK Lord.\n")
        embed.add_field(name="OI Discussion", value="And then we discuss about OI in Left's name.\n")
        embed.add_field(name="Bot speech", value="Then the bot will speak out the speech made by the assem host. Usually content to praise Left.\n")
        embed.add_field(name="End", value="We end the assem with a last prayer, begging for AC blessings, in the name of Left.\n")
        await ctx.send(embed=embed)

    @assem.command()
    async def start_prayer(self, ctx, s: str):
        if self.started_assem is True and self.host_id == ctx.author.id:
            await ctx.send("Prayer starts now!")
        else:
            await ctx.send("assem isn't started, you can host one by `.assem start`.")

async def setup(bot):
    await bot.add_cog(OtherCmd(bot))