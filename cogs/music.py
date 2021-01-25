from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed

class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.volume = 40
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())


class MusicCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.controllers = {}
    self.bot.music = lavalink.Client(self.bot.user.id)
    self.bot.music.add_node('localhost', 2333, 'testing', 'eu', 'music-node')
    self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
    self.bot.music.add_event_hook(self.track_hook)


  @commands.command(name='play')
  async def play(self, ctx, *, query):
    print('The Bot has Joined')
    member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
    if member is not None and member.voice is not None:
      vc = member.voice.channel
      player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
      if not player.is_connected:
        player.store('channel', ctx.channel.id)
        await self.connect_to(ctx.guild.id, str(vc.id))

    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)
      query = f'ytsearch:{query}'
      results = await player.node.get_tracks(query)
      tracks = results['tracks'][0:10]
      i = 0
      query_result = ''
      for track in tracks:
        i = i + 1
        query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
      embed = Embed()
      embed.description = query_result

      await ctx.channel.send(embed=embed)

      def check(m):
        return m.author.id == ctx.author.id
      
      response = await self.bot.wait_for('message', check=check)
      track = tracks[int(response.content)-1]

      player.add(requester=ctx.author.id, track=track)
      if not player.is_playing:
        await player.play()

    except Exception as error:
      print(error)


  
  async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await self.connect_to(guild_id, None)
      
  async def connect_to(self, guild_id: int, channel_id: str):
    ws = self.bot._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)
  
  @commands.command(name='stop')
  async def stop(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        if player.is_playing:
          await player.stop()
          await ctx.send(f"{ctx.author.display_name} has stopped the music")
        else:
          await ctx.send("Nothing is playing")


  @commands.command(name='pause')
  async def pause(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

    
        if player.is_playing:
            await player.set_pause(True)
    

  @commands.command(name='resume')
  async def resume(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

    
        if not player.paused:
            return await ctx.send('I am not currently paused!', delete_after=15)

        await ctx.send('Resuming the player!', delete_after=15)
        await player.set_pause(False)
  
  
  @commands.command(aliases=['dc'])
  async def leave(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Disconnected.')
    
def setup(bot):
  bot.add_cog(MusicCog(bot))
  

