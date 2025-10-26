import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_IDS = os.getenv("CHANNEL_IDS").split(",")  # list of channel IDs as strings
MC_SERVER = "your.minecraftserver.com"  # Replace this with your server address

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to check Minecraft server status
from mcstatus import JavaServer

def get_server_status():
    try:
        # Ping the local Minecraft server directly
        server = JavaServer.lookup("localhost:25565")  # change port if different
        status = server.status()
        return f"✅ Server is **Online** — {status.players.online}/{status.players.max} players!"
    except Exception as e:
        return "❌ Server is **Offline**."


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    check_server_status.start()

#@tasks.loop(minutes=5)
#async def check_server_status():
    message = get_server_status()
    print(message)  # For debugging
    for id_str in CHANNEL_IDS:
        try:
            channel = bot.get_channel(int(id_str.strip()))
            if channel:
                await channel.send(message)
            else:
                print(f"⚠️ Could not find channel {id_str}")
        except Exception as e:
            print(f"Error sending to {id_str}: {e}")

# Optional: Allow manual status check
@bot.command()
async def status(ctx):
    await ctx.send(get_server_status())

bot.run(TOKEN)

