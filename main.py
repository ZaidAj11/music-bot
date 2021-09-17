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




client.run('ODg3MTIyNjkyNzYxODYyMTY0.YT_jYw.CtUP_0Rqy6OxYRu7_yzVj_EvbR4')