import discord
from discord.ext import commands
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
WORDLE_FILE_PATH = "../src/wordle.txt"
class GameCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_wordle = False
        self.id = 0
        self.word = ""
    
    @commands.group()
    async def wordle(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name="Invalid command of `.wordle` <:wa:1172511313168175235>", value="Use `.help wordle` for commands")
            await ctx.send(embed=embed)
    
    @wordle.command()
    async def start(self, ctx):
        if self.start_wordle == False:
            self.start_wordle = True
            with open(WORDLE_FILE_PATH, 'r') as file:
                pass # TODO: find random word as answer
            await ctx.send("Game starts!\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜")
        else:
            embed = discord.Embed(title="ERROR", color=discord.Color.red())
            embed.add_field(name="Wordle game already in progress! <:re:1176472670183899246>", value=f"Discord ID: {ctx.author.id}")
            await ctx.send(embed=embed)
    
    @wordle.command()
    async def delete(self, ctx):
        if self.start_wordle == False:
            await ctx.send("```std::wordle_exception thrown, \nIn wordle.cp line 32, ResetWordleMethod.throw(std::wordle_exception);\n ResetWordleMethod only limits argument to be true```")
        else:
            self.start_wordle = False
            embed = discord.Embed(title="Success", color=discord.Color.green(), description="RESET_WORDLE Operation Successful")
            await ctx.send(embed=embed)
    
    @wordle.command()
    async def ans(self, ctx, word):
        if self.start_wordle == False:
            await ctx.send("```std::wordle_exception thrown, \n In wordle.cp line 41, AnswerWordle.throw(std::wordle_exception); \n Wordle method has not started yet.```")
        else:
            with open(WORDLE_FILE_PATH, 'r') as file:
                content = file.read()
                if word not in content:
                    await ctx.send("Invalid word.")
                else:
                    pass # TODO: use wordle notation for checking words

            await ctx.send("work in progress I am nigger!") # test message, later del.


async def setup(bot):
    await bot.add_cog(GameCmd(bot))