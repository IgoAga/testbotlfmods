import discord
import os
from discord.ext import commands

prefix = "~" 
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
  print(f'{bot.user} has logged in.')
  bot.load_extension('music')

token = os.environ.get('Bot_Token') 
bot.run(str(token))
