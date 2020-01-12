import discord
import datetime
from discord.ext import commands
from cogs.basic_commands import BasicCommands

token = 'NjY1OTg5MTA5NjI1Mzg5MDU2.XhuTTA.KnZbn_Rgsb4LJ0HWwojtlrwM06s'

bot = commands.Bot("$")

bot.add_cog(BasicCommands(bot))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('[{}] I\'m in!'.format(datetime.datetime.now()))
    print('----')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "i\'m in" in message.content.lower():
        await message.channel.send("I\'m in")
        await message.channel.send(file=discord.File('im_in.jpg'))

    await bot.process_commands(message)


bot.run(token, bot=True)
