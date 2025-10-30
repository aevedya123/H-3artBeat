import os
import threading
import discord
from discord.ext import tasks
from flask import Flask
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

# --- Flask web server to keep port 8080 alive ---
app = Flask(__name__)
@app.route('/')
def home():
    return "💓 BeatBot is alive!"
def run_web():
    app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run_web).start()

# --- Discord client ---
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    heartbeat.start()

@tasks.loop(seconds=30)
async def heartbeat():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="💓 Heartbeat",
            description="BeatBot is alive!",
            color=0x57F287,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Made by SAB-RS")
        await channel.send(embed=embed)
    else:
        print("⚠️ Channel not found")

client.run(TOKEN)
