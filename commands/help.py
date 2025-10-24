import discord
from discord.ext import commands
from helpers.command_dict import add_command, get_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        add_command('help', 'Shows this message')

    @commands.command(name='help')
    async def Help(self, ctx):
        command_dict = get_commands()

        embed = discord.Embed(
            title="KMusic Commands",
            description="Here is a list of all available commands:",
            color=discord.Color.purple()
        )

        if not command_dict:
            embed.description = "No commands are available at this time."
        else:
            for name, description in command_dict.items():
                embed.add_field(name=name, value=description, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
