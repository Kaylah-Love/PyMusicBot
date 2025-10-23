from discord.ext import commands
from helpers.queue import clear_queue

class Dc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dc')
    async def dc(self, ctx):
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            await ctx.send("I am not connected to a voice channel")
            return

        clear_queue(ctx.guild.id)
        voice_client.stop()
        await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Dc(bot))
