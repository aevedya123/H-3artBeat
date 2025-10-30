import os
import discord
import asyncio
from discord.ext import tasks
from flask import Flask
from threading import Thread
from datetime import datetime

# Flask app to keep Render service alive
app = Flask(__name__)

@app.route('/')
def home():
    return "❤️ HeartBeat bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Discord bot setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LINKBOT_ID = os.getenv("LINKBOT_ID")  # LinkBot’s Discord ID
TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print(f"[{datetime.utcnow()}] ✅ Logged in as {client.user}")
    if not heartbeat.is_running():
        heartbeat.start()
    print("❤️ Heartbeat loop started!")

@tasks.loop(minutes=3)
async def heartbeat():
    try:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            timestamp = datetime.now().strftime("%H:%M:%S")
            msg = f"<@{LINKBOT_ID}> 💓 Beating at {timestamp}!"
            await channel.send(msg)
            print(f"[{timestamp}] ✅ Sent heartbeat ping to LinkBot.")
        else:
            print("⚠️ Channel not found. Check CHANNEL_ID.")
    except Exception as e:
        print("❌ Heartbeat failed:", e)

# Run Flask in a background thread
Thread(target=run_flask).start()

# Run Discord bot
client.run(TOKEN)
