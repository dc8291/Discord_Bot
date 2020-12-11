import discord
from discord.ext import commands
import re

class BasicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    #When someone types "i'm in" send the i'm in image
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        match = re.search("(i'?m\s*in)", message.content.lower())
        if  match:
            await message.channel.send(file=discord.File('./pics/im_in.jpg'))

def setup(client):
    client.add_cog(BasicCommands(client))
