import asyncio
import discord
from typing import Optional
from discord.ext import commands
from helpers.youtube_fetch import get_audio_stream_url
from helpers.play_stream import play_stream
from helpers.youtube_query import search_youtube_urls
from helpers.youtube_url_checker import is_valid_youtube_url
from helpers.youtube_video_info import get_video_info
from helpers.command_dict import add_command
from helpers.queue import get_queue, pop_from_queue, add_to_queue

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        add_command('play', 'Plays audio from a YouTube URL or search query')

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        await self._play_audio_logic(ctx, query=query)

    async def _play_audio_logic(self, ctx, *, query: str, vidInfo: Optional[dict] = None, forcePlay: bool = False):
        if not ctx.author.voice:
            # Error embed for not in VC
            embed = discord.Embed(
                description="You are not connected to a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # "Loading" embed
        embed = discord.Embed(
            description=f"Loading `{query}`...",
            color=discord.Color.purple()
        )
        message = await ctx.send(embed=embed)
        
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)
        
        url = query
        if not is_valid_youtube_url(query):
            urls = await asyncio.to_thread(search_youtube_urls, query, 1) 
            
            if urls and len(urls) > 0:
                url = urls[0]
            else:
                # Error embed for no results
                embed = discord.Embed(
                    description=f"Could not find a valid YouTube video from your query `{query}`",
                    color=discord.Color.red()
                )
                await message.edit(embed=embed)
                return
        
        if not forcePlay and (voice_client.is_playing() or voice_client.is_paused()):
            info = { "webpage_url": url }
            add_to_queue(ctx.guild.id, info)
            
            # "Added to Queue" embed
            embed = discord.Embed(
                title="Added to Queue",
                description=f"{url}",
                color=discord.Color.purple()
            )
            if info.get('thumbnail'):
                embed.set_thumbnail(url=info['thumbnail'])
            embed.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url
            )
            await message.edit(embed=embed)
            return
        
        info = vidInfo
        if vidInfo is None:
            info = await asyncio.to_thread(get_video_info, url)
        
        async def after_playing(_):
            try:
                await message.delete() 
            except discord.errors.NotFound: 
                pass # Message was already deleted
            except Exception:
                pass # Handle other potential errors
            
            if get_queue(ctx.guild.id):
                nextInfo = pop_from_queue(ctx.guild.id)
                await self._play_audio_logic(ctx, query=nextInfo['webpage_url'], vidInfo=nextInfo, forcePlay=True)

        stream_url = await asyncio.to_thread(get_audio_stream_url, url)

        if not stream_url:
            # Error embed for no stream
            embed = discord.Embed(
                description=f"Could not find a playable audio stream from {url}",
                color=discord.Color.red()
            )
            await message.edit(embed=embed)
            return
            
        error = await play_stream(
            ctx,
            stream_url,
            after=lambda e: asyncio.run_coroutine_threadsafe(after_playing(e), self.bot.loop)
        )

        if error:
            # Error embed for playback error
            embed = discord.Embed(
                description=str(error),
                color=discord.Color.red()
            )
            await message.edit(embed=embed)
        else:
            # "Now Playing" embed
            embed = discord.Embed(
                title="▶️ Now Playing",
                description=f"**[{info['title']}]({info['webpage_url']})**",
                color=discord.Color.purple()
            )
            
            if info.get('thumbnail'):
                embed.set_thumbnail(url=info['thumbnail'])
            
            # Add uploader if available
            if info.get('uploader'):
                embed.add_field(name="Uploader", value=info['uploader'], inline=True)
            
            # Format and add duration
            duration = info.get('duration_string')
            if not duration and info.get('duration'):
                # Basic formatter for seconds -> MM:SS or HH:MM:SS
                secs = info['duration']
                m, s = divmod(secs, 60)
                h, m = divmod(m, 60)
                duration = f"{h:d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            
            if duration:
                embed.add_field(name="Duration", value=duration, inline=True)

            embed.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url
            )
            
            await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))
