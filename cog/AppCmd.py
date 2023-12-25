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
        await modules.contest.contests(self, interaction=interaction)
    
    @app_commands.command(name="ping", description="Outputs your ping")
    async def ping(self, interaction: discord.Interaction):
        latency =  self.bot.latency
        await interaction.response.send_message(content=":ping_pong: Pong!")
        await interaction.edit_original_response(content=f":ping_pong: Pong! `{int(latency*1000)} ms`")

async def setup(bot):
    await bot.add_cog(AppCmd(bot), guilds=[discord.Object(id=1153623382466768946)])