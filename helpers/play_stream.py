import discord

async def play_stream(ctx, stream_url, after=None):
    """
    Plays a stream to the voice channel the bot is currently in for the given context's guild.
    Assumes the bot is already connected to a voice channel.
    """
    voice_client = ctx.guild.voice_client
    if not voice_client:
        return "I am not connected to a voice channel."

    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    try:
        player = discord.FFmpegPCMAudio(stream_url, executable='ffmpeg', **ffmpeg_options)

        if (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()
        voice_client.play(player, after=after)
        return None
    except Exception as e:
        print(f"Error in play_stream: {e}")
        return f"An error occurred while trying to play the stream."
