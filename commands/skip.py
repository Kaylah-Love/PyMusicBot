from discord.ext import commands

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='skip')
    async def skip(self, ctx):
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            await ctx.send("I am not connected to a voice channel")
            return
        
        voice_client.stop()

async def setup(bot):
    await bot.add_cog(Skip(bot))
