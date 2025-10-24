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
        'options': (
            '-vn '                         # No video
            '-ar 48000 '                   # Resample to 48kHz
            '-ac 2 '                       # Set to 2-channel stereo
            '-af "loudnorm=I=-16:TP=-1.5:LRA=11"' # Apply loudness normalization
        )
    }

    try:
        player = discord.FFmpegPCMAudio(stream_url, executable='ffmpeg', **ffmpeg_options)
        guild_volume = 0.1
        player_with_volume = discord.PCMVolumeTransformer(player, volume=guild_volume)

        if (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()

        voice_client.play(player_with_volume, after=after)
        return None
    except Exception as e:
        print(f"Error in play_stream: {e}")
        return f"An error occurred while trying to play the stream."
