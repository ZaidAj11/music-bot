import discord
from discord.ext import commands 
import youtube_dl
intents = discord.Intents.default()
intents.members = True

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.song_queue = []
    self.now_on = False
    self.FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.YDL_OPTIONS = {'format':'bestaudio'}
    self.vc = ""

  def search(self, sen):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
        try: 
            info = ydl.extract_info("ytsearch:%s" % sen, download=False)['entries'][0]
        except Exception: 
            return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}

  # loop
  async def check_queue(self):
    if len(self.song_queue) > 0:
      self.now_on = True
      url = self.song_queue[0][0]['source']
      if self.vc == "" or not self.vc.is_connected():
          self.vc = await self.song_queue[0][1].connect()
      else:
          await self.vc.move_to(self.song_queue[0][1])
      self.song_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS),after = lambda e: self.play_next())

    else:
      self.now_on = False

  def play_next(self):
      if len(self.song_queue) > 0:
          self.now_on = True

          url = self.song_queue[0][0]['source']

          self.song_queue.pop(0)
          print("gonna start")
          self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())


      else:
          self.now_on = False

  @commands.command()
  async def join(self,ctx):
    if ctx.author.voice is None:
      await ctx.send("YOUR NOT IN A VC RETARD")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def leave(self,ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
      await voice_channel.connect()

    else:
      await ctx.voice_client.disconnect()


  @commands.command(aliases = ['p'])
  async def play(self,ctx,*inp):
    sen = " ".join(inp)

    voice_channel = ctx.author.voice.channel

    if voice_channel is None:
      await ctx.send("You're not in a voice channel")

    else:

      song = self.search(sen)
      await ctx.send("Song added to the queue")
      self.song_queue.append([song, voice_channel])
      print(self.song_queue[0][0]['title'])

      if self.now_on == False:
        await self.check_queue()



  @commands.command()
  async def pause(self,ctx):
    await ctx.voice_client.pause()
    ctx.send("Audio paused")


  @commands.command()
  async def resume(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("Audio resumed")




def setup(client):
  client.add_cog(music(client))
