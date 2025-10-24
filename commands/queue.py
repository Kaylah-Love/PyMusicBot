import discord
from discord.ext import commands
from helpers.command_dict import add_command
from helpers.queue import get_queue

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        add_command('queue', 'Displays the current queue')

    @commands.command(name='queue')
    async def queue(self, ctx):
        if ctx.guild.voice_client is None:
            embed = discord.Embed(
                description="I am not connected to a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        guildQueue = get_queue(ctx.guild.id)
        
        if not guildQueue:
            embed = discord.Embed(
                description="The queue is empty",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            return
        
        display_limit = 15
        track_list = [
            f"**{i + 1}.** {video['webpage_url']}" 
            for i, video in enumerate(guildQueue[:display_limit])
        ]

        description = "\n".join(track_list)

        embed = discord.Embed(
            title="🎵 Music Queue",
            description=description,
            color=discord.Color.purple()
        )

        total_songs = len(guildQueue)
        if total_songs > display_limit:
            embed.set_footer(text=f"Showing {display_limit} of {total_songs} songs")
        else:
            embed.set_footer(text=f"Total songs: {total_songs}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Queue(bot))