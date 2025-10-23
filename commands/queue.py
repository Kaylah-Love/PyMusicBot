from discord.ext import commands
from helpers.queue import get_queue

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='queue')
    async def queue(self, ctx):
        if ctx.guild.voice_client is None:
            await ctx.send("I am not connected to a voice channel")
            return
        
        guildQueue = get_queue(ctx.guild.id)
        if guildQueue:
            for i, video in enumerate(guildQueue):
                await ctx.send(f"{i + 1}. {video['title']}")
        else:
            await ctx.send("The queue is empty")

async def setup(bot):
    await bot.add_cog(Queue(bot))
