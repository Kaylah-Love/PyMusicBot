import discord
from discord.ext import commands
from helpers.command_dict import add_command
from helpers.queue import clear_queue

class Dc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        add_command('dc', 'Disconnects the bot from it\'s active channel')

    @commands.command(name='dc')
    async def dc(self, ctx):
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
        await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Dc(bot))
