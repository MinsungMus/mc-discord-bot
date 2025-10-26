import os
import discord
from discord.ext import commands
from mcstatus import JavaServer
from dotenv import load_dotenv

# Load environment variables (only needed if running locally; Render uses its own env vars)
load_dotenv()

TOKEN = os.getenv("discord_token")  # Make sure Render environment key matches this
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Optional: if you want a default channel
SERVER_IP = os.getenv("SERVER_IP")       # Your Minecraft server IP
SERVER_PORT = int(os.getenv("SERVER_PORT", 25565))  # Default Minecraft port if not specified

intents = discord.Intents.default()
intents.message_content = True  # Required if you read message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Command to manually check server status
@bot.command(name="mcstatus")
async def mcstatus(ctx):
    server = JavaServer(SERVER_IP, SERVER_PORT)
    try:
        status = server.status()
        msg = (
            f"🟢 Server is online!\n"
            f"Players: {status.players.online}/{status.players.max}\n"
            f"MOTD: {status.description}"
        )
    except Exception as e:
        msg = f"🔴 Server is offline or unreachable. ({e})"
    await ctx.send(msg)

bot.run(TOKEN)


