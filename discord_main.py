import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 
BOT_PREFIX = '!' 

# Client Setup
intents = discord.Intents.default()
intents.message_content = True

class MusicBot(commands.Bot):
    async def setup_hook(self):
        """This runs once when the bot starts and loads all commands."""
        print("--- Loading Commands ---")
        for filename in os.listdir('./commands'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'commands.{filename[:-3]}')
                    print(f"Successfully loaded: {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
        print("--- All commands loaded ---")

bot = MusicBot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Prints a message when the bot successfully connects to Discord."""
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found. Make sure you have a .env file with your token.")