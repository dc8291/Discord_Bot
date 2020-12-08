import discord
from discord.ext import commands
from discord.ext.commands import Bot


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yeet(self, ctx):
        await ctx.send('yeetus')
