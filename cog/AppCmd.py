import discord
from discord import app_commands
from discord.ext import commands
import src.contest
import src.dse
FOO = '''```py
@app_commands.command(name="foo", description="foobar")
async def foo(interaction: discord.Interaction):
    # TODO: insert code here
```
'''

class AppCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        print(self.bot.guilds)
        fmt = await ctx.bot.tree.sync()
        print(f"{fmt}")
        print(f"synced {len(fmt)} commands.")
        await ctx.send(f"Synced {len(fmt)} commands.")

    @app_commands.command(name="contests", description="Sends the information of contests from multiple platforms. (ERROR)")
    async def contests(self, interaction: discord.Interaction):
        await src.contest.contests(self, interaction)
    
    @app_commands.command(name="ping", description="Pingpong!")
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency
        await interaction.response.send_message(content=":ping_pong: Pong!")
        await interaction.edit_original_response(content=f":ping_pong: Pong! `{int(latency*1000)} ms`")

    @app_commands.command(name="foo", description="foobar")
    async def foo(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue(), title="Sample discord slash command", description=FOO)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="eph", description="foobar")
    async def eph(self, interaction: discord.Interaction, text: str="gulu!"):
        await interaction.response.send_message(text, ephemeral=True)

    @app_commands.command(name="dse", description="provides hints for HKOI DSE question")
    async def dse(self, interaction: discord.Interaction, question: str):
        if question[0] != 'D':
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name="Invalid DSE question", value=f"Discord ID: {interaction.user.id}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(src.dse.DSE(question))

async def setup(bot):
    await bot.add_cog(AppCmd(bot))