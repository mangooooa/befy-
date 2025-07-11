import os
import discord
from discord.ext import tasks, commands
import asyncio
import datetime

# User ID to message
TARGET_USER_ID = 810656057461964841

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message content (if you add commands later)
intents.members = True # Required to fetch user information by ID

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # Start the scheduled task when the bot is ready
    send_scheduled_dm.start()

@tasks.loop(hours=48) # 48 hours = 2 days
async def send_scheduled_dm():
    try:
        user = await bot.fetch_user(TARGET_USER_ID)
        if user:
            await user.send("Hi!")
            print(f"DM sent to {user.name} (ID: {TARGET_USER_ID}) at {datetime.datetime.now()}")
        else:
            print(f"Could not find user with ID: {TARGET_USER_ID}")
    except discord.Forbidden:
        print(f"Could not send DM to user {TARGET_USER_ID}. They might have DMs disabled or blocked the bot.")
    except Exception as e:
        print(f"An error occurred while sending DM: {e}")

@send_scheduled_dm.before_loop
async def before_send_scheduled_dm():
    await bot.wait_until_ready()
    print("Waiting for bot to be ready before starting DM loop...")

# Get the bot token from environment variables
# It's crucial to use environment variables for sensitive information like tokens
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    print("Error: DISCORD_BOT_TOKEN environment variable not set.")
    print("Please set the DISCORD_BOT_TOKEN environment variable with your bot's token.")
else:
    bot.run(BOT_TOKEN)
