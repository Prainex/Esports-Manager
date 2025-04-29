import logging
import os

import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv


load_dotenv()

OWNER_ID = int(os.getenv('ORG_OWNER'))
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.command()
async def goodboy(ctx):
    await ctx.send("I'm a Goodboy, bark bark")
    await



@client.event
async def on_ready():
    print(f'We have logged onto, {client.user}, and are ready to go!')

@client.event
async def on_member_join(member):
    await member.send(f'Welcome to the server {member.mention}!')

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)