import discord
from discord.ext import commands
from helpers.command_dict import add_command

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        add_command('skip', 'Skips the currently playing song')

    @commands.command(name='skip')
    async def skip(self, ctx):
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            embed = discord.Embed(
                description="I am not connected to a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        voice_client.stop()

async def setup(bot):
    await bot.add_cog(Skip(bot))
