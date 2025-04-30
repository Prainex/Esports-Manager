import logging
import os
import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv


load_dotenv()

OWNER = int(os.getenv('BUGS_ID'))
TOKEN = os.getenv('DISCORD_TOKEN')
TASK_CHANNEL= int(os.getenv('TASKS_ID'))
BOT_LOG = int(os.getenv('LOG_CHANNEL'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.command()
async def goodboy(ctx):
    await ctx.send("I'm a Goodboy, bark bark")

@client.tree.command(name="assign_task", description="Assign a task to a user")
async def create_task(interaction: discord.Interaction, task: str, deadline: str, assignee: str, description: str):
    await interaction.response.send_message(f'Creating task: {task}')
    await client.get_channel(BOT_LOG).send(f'Assigned {assignee} to complete task: {task}. They are expected to finish by {deadline}. Description: {description}')
    await client.get_channel(TASK_CHANNEL).send(f'Assigned {assignee} to complete task: {task}. They are expected to finish by {deadline}. Description: {description}')
    # await client.get_user(assignee).send(f'You have been assigned to complete task: {task}. You are expected to finish by {deadline}. Description: {description}')


@client.tree.command(name="report_bug", description="report a bug")
async def report(interaction: discord.Interaction, command: str, description: str):
    await client.get_channel(OWNER).send(f'Bug reported: {command} \n Description: {description}')
    await interaction.response.send_message("Your bug report has been submitted successfully!")

@client.event
async def on_ready():
    print(f'We have logged onto, {client.user}, and are ready to go!')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@client.event
async def on_member_join(member):
    await member.send(f'Welcome to the server {member.mention}!')

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)