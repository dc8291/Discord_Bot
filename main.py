import discord
import datetime
from discord.ext import commands
from cogs.basic_commands import BasicCommands
import re

token = 'token'

bot = commands.Bot("$")

bot.add_cog(BasicCommands(bot))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('[{}] I\'m in!'.format(datetime.datetime.now()))
    print('----')

#When someone types "i'm in" send the i'm in image
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    match = re.search("(i'*m\s*in)", message.content.lower())
    if  match:
        await message.channel.send(file=discord.File('im_in.jpg'))

    await bot.process_commands(message)


bot.run(token, bot=True)
