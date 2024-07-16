from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
from responses import search_muse
from meta import Meta
from yahoo.functionality import get_standings, get_scoreboard

# Step 0: Load token somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Step 1: Bot Setup
intents: Intents = Intents.default()
intents.message_content = True # NOQA
bot = commands.Bot(command_prefix="!", intents=intents)

# Command functionality
@bot.command(name='muse')
async def muse(ctx, *, user_text: str):
    result = search_muse(user_text)
    if result:
        await ctx.send(result)
    else:
        await ctx.send('Sorry, I could not retrieve this statistic.')

@bot.command(name="standings")
async def standings(ctx):
    standings = get_standings()
    if standings:
        await ctx.send(embed=standings)
    else:
        await ctx.send('Sorry, there seems to be an issue.') 

@bot.command(name='scoreboard')
async def scoreboard(ctx):
    scoreboard = get_scoreboard()
    if scoreboard:
        await ctx.send(embed=scoreboard)
    else:
        await ctx.send('Sorry, there seems to be an issue.')

#########################
### TRANSACTIONS LOOP ###
#########################

# Startup
@bot.event
async def on_ready() -> None:
     print(f'{bot.user} is now running!')

# Handling incoming messages
@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await bot.process_commands(message)  # Process commands if the message contains a command

# Load the Meta cog
async def load_extensions():
    await bot.add_cog(Meta(bot))
    await bot.tree.sync()

# Step 5: Main entry point
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()