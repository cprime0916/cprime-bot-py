import discord
from discord.ext import commands
import configparser
import random
config = configparser.ConfigParser()
config.read('config.ini')

class OtherCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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
    async def say(self, ctx, *, s):
        await ctx.message.delete()
        if s != "`prayer`":
            await ctx.send(f"{s}")
        else:
            await ctx.send('''oh Left is so genius it is undoubtable that Left is always the truth, the myth, the legendary holy Left. It is our luck that we are blessed by Left and receiving his guidance''')

    @commands.command()
    async def prayer(self, ctx):
        await ctx.send('''oh Left is so genius it is undoubtable that Left is always the truth, the myth, the legendary holy Left. It is our luck that we are blessed by Left and receiving his guidance''')
    
    @commands.command()
    async def lp(self, ctx):
        await ctx.send('''Our LeftLeft in Atcoder, 
Hallowed be thy handle,
Thy contests come,
Thy AK be done,
On HKOI as in IOI,
Give us our daily AC.
And forgive our WA spams,
As we forgive those who hacked against us.
Do not bring us to the Methforces trials
But deliever us from stupidity.
For the IOI Gold, the IQ,
And the AK are thine,
Now and Forever. 
Accepted.''')

    @commands.command()
    async def quote(self, ctx):
        det = random.randint(1, 5)
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
    async def spam(self, ctx, text, num):
        if int(num) <= 10 and text[0] != '`':
            for _ in range(0, int(num)):
                await ctx.send(text)
        elif int(num) <= 10:
            if text == "`prayer`":
                for _ in range(0, int(num)):
                    await ctx.send('''oh Left is so genius it is undoubtable that Left is always the truth, the myth, the legendary holy Left. It is our luck that we are blessed by Left and receiving his guidance''')
            elif text == "`left_prayer`":
                for _ in range(0, int(num)):
                    await ctx.send('''Our LeftLeft in Atcoder, 
Hallowed be thy handle,
Thy contests come,
Thy AK be done,
On HKOI as in IOI,
Give us our daily AC.
And forgive our WA spams,
As we forgive those who hacked against us.
Do not bring us to the Methforces trials
But deliever us from stupidity.
For the IOI Gold, the IQ,
And the AK are thine,
Now and Forever. 
Accepted.''')
            else:
                await ctx.send("invalid command prompt.")
        else:
            await ctx.send("In `main.py`, MAX_LIMIT = 10")

async def setup(bot):
    await bot.add_cog(OtherCmd(bot))