#########################################################
### THIS FILE CONTAINTS DESCRIPTIONS OF BOT FUNCTIONS ###
### SENT TO USERS WHEN THE '!help' FUNCTION IS CALLED ###
#########################################################
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="View available commands")
    async def help(self, interaction: discord.Interaction):
        logger.info("Help command triggered")
        embed = discord.Embed(
            title="Marcy",
            description="Yahoo Fantasy Football Bot for McCallie League",
        )
        embed.add_field(
            name="/ping", value="Gives the latency of Marcy", inline=False
        )
        embed.add_field(
            name="/standings", value="Gives the current league standings", inline=False
        )
        embed.add_field(
            name="/stats player_name", value="Gives the player statistics of the given player", inline=False
        )
        embed.add_field(
            name="/muse query", value="Returns statistics based on user query", inline=False
        )
        await interaction.response.send_message(embed=embed)
        logger.info("Help message sent")

    @app_commands.command(name="ping", description="Gives the latency of Marcy")
    async def ping(self, interaction: discord.Interaction):
        logger.info("Ping command triggered")
        await interaction.response.send_message(f'Pong! Latency: {self.bot.latency * 1000:.2f}ms')
        logger.info("Ping message sent")

async def setup(bot):
    await bot.add_cog(Meta(bot))
