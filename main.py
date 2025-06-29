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
EVENTS_CHANNEL = int(os.getenv('EVENTS_ID'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.command()
async def goodboy(ctx):
    await ctx.send("I'm a Goodboy, bark bark")


#Create events command
@client.tree.command(name="post_event", description="Create an upcoming event")
async def post_event(
    interaction: discord.Interaction, 
    name: str, 
    date: str,
    link: str
):
    await interaction.response.send_message(f'Created event: {name} on {date} at {link}')
    log_message = (
        f'Event created: **{name}**\n'
        f'Date: **{date}**\n'
        f'Link: {link}'
    )
    await client.get_channel(EVENTS_CHANNEL).send(log_message)
    await client.get_channel(BOT_LOG).send(log_message)


#Create tasks command
@client.tree.command(name="assign_task", description="Assign a task to a user")
async def assign_task(
    interaction: discord.Interaction,
    task: str,
    deadline: str,
    assignee: discord.User,
    description: str
):
    await interaction.response.send_message(f'Creating task: {task}')

    log_message = (
        f'Assigned {assignee.mention} to complete task: **{task}**.\n'
        f'Deadline: **{deadline}**\nDescription: {description}'
    )

    await client.get_channel(BOT_LOG).send(log_message)
    await client.get_channel(TASK_CHANNEL).send(log_message)

    try:
        await assignee.send(
            f"You have been assigned a task:\n"
            f"**Task**: {task}\n**Deadline**: {deadline}\n**Description**: {description}"
        )
    except discord.Forbidden:
        await interaction.followup.send(
            f"⚠️ Could not DM {assignee.mention}. They may have DMs disabled.", ephemeral=True
        )

#Report bugs command
@client.tree.command(name="report_bug", description="Report a bug in the bot")
async def report_bug(
    interaction: discord.Interaction,
    command: str, 
    description: str
):
    await interaction.response.send_message(f'Bug reported: {command} \n Description: {description}')
    log_message = (
        f"Bug reported: {command} \n" 
        f"Description: {description}"
    )
    await client.get_channel(OWNER).send(log_message)


@client.event
async def on_ready():
    print(f'We have logged onto, {client.user}, and are ready to go!')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
        for cmd in client.tree.get_commands():
            print(f"Registered command: {cmd.name} - {cmd.description}")

    except Exception as e:
        print(f"Error syncing commands: {e}")

@client.event
async def on_member_join(member):
    await member.send(f'Welcome to the server {member.mention}!')

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
