import os
import discord
from discord.ext import commands
import music


intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())
cogs = [music]
@client.event 
async def on_ready():
  print('Logged in as {0.user}'.format(client))

for i in range(len(cogs)):
  cogs[i].setup(client)

my_secret = os.getenv('token')

client.run(my_secret)
