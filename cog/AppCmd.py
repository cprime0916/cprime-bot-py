import discord
from discord import app_commands
from discord.ext import commands
import modules.contest
class AppCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands.")


    @app_commands.command(name="contests", description="Sends the information of contests from multiple platforms.")
    async def contests(self, interaction: discord.Interaction):
        modules.contest.contests(self, interaction=interaction)

async def setup(bot):
    await bot.add_cog(AppCmd(bot), guilds=[discord.Object(id=1153623382466768946)])