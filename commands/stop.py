import discord
from discord.ext import commands
from helpers.command_dict import add_command
from helpers.queue import clear_queue

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        
        add_command('skip', 'Stops the currently playing song and removes the queue')

    @commands.command(name='stop')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            embed = discord.Embed(
                description="I am not connected to a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        clear_queue(ctx.guild.id)
        voice_client.stop()

async def setup(bot):
    await bot.add_cog(Stop(bot))
