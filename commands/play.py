import asyncio
from typing import Optional
from discord.ext import commands
from helpers.youtube_fetch import get_audio_stream_url
from helpers.play_stream import play_stream
from helpers.youtube_query import search_youtube_urls
from helpers.youtube_url_checker import is_valid_youtube_url
from helpers.youtube_video_info import get_video_info
from helpers.queue import get_queue, pop_from_queue, add_to_queue

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        """Plays audio from a YouTube URL or search query"""
        await self._play_audio_logic(ctx, query=query)

    async def _play_audio_logic(self, ctx, *, query: str, vidInfo: Optional[dict] = None, forcePlay: bool = False):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return
        
        # Create message before potentially connecting to channel
        message = await ctx.send(f"Searching for `{query}`")
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)
        
        # Determine URL
        url = query
        if not is_valid_youtube_url(query):
            urls = search_youtube_urls(query, 1)
            if urls and len(urls) > 0:
                url = urls[0]
            else:
                await message.edit(content=f"Could not find a valid youtube video from your query `{query}`")
                return
            
        # Get video info
        info = vidInfo if vidInfo is not None else get_video_info(url)
        
        # Handle queuing
        if not forcePlay and (voice_client.is_playing() or voice_client.is_paused()):
            add_to_queue(ctx.guild.id, info)
            await message.edit(content=f"Added to queue: {info['title']}")
            return
        
        async def after_playing(_):
            await message.delete() 
            if get_queue(ctx.guild.id):
                nextInfo = pop_from_queue(ctx.guild.id)
                # Recursively call the internal logic for the next item
                await self._play_audio_logic(ctx, query=nextInfo['webpage_url'], vidInfo=nextInfo, forcePlay=True)

        # Get the stream URL
        stream_url = get_audio_stream_url(url)
        if not stream_url:
            await message.edit(content=f"Could not find a playable audio stream from {url}") 
            return
            
        # Play the stream
        error = await play_stream(
            ctx,
            stream_url,
            # Pass the local async function 'after_playing' into the threadsafe execution
            after=lambda e: asyncio.run_coroutine_threadsafe(after_playing(e), self.bot.loop)
        )

        if error:
            await message.edit(content=error)
        else:
            await message.edit(content=f"Now playing: {info['title']}")

async def setup(bot):
    await bot.add_cog(Play(bot))