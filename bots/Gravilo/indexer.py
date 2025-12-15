import discord
import requests
import os
import asyncio
from datetime import datetime, timedelta

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
# New Webhook for Ingestion (Create this in n8n: Gravilo_Ingest_Discord)
N8N_INGEST_WEBHOOK_URL = os.getenv('N8N_INGEST_WEBHOOK_URL') 
DAYS_TO_INDEX = 30  # How far back to go?
BATCH_SIZE = 50     # Messages per n8n request

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)

async def process_channel(channel):
    print(f"Indexing channel: #{channel.name} ({channel.id})")
    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_INDEX)
    
    messages_batch = []
    count = 0

    try:
        async for message in channel.history(limit=None, after=cutoff_date):
            if message.author.bot:
                continue # Skip bots
            
            if not message.content.strip():
                continue # Skip empty messages (e.g. just images without text)

            # Construct Discord Message URL
            # https://discord.com/channels/{guild_id}/{channel_id}/{message_id}
            message_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

            msg_data = {
                "content": message.content,
                "metadata": {
                    "source": "discord",
                    "author": message.author.name,
                    "author_id": str(message.author.id),
                    "channel": channel.name,
                    "channel_id": str(channel.id),
                    "server_id": str(message.guild.id),
                    "timestamp": message.created_at.isoformat(),
                    "url": message_url
                }
            }
            
            messages_batch.append(msg_data)
            count += 1

            if len(messages_batch) >= BATCH_SIZE:
                await send_batch(messages_batch)
                messages_batch = []
        
        # Send remaining
        if messages_batch:
            await send_batch(messages_batch)
            
        print(f"  -> Indexed {count} messages from #{channel.name}")

    except Exception as e:
        print(f"  -> Error indexing #{channel.name}: {e}")

async def send_batch(batch):
    if not N8N_INGEST_WEBHOOK_URL:
        print("  [Dry Run] Batch ready (N8N_INGEST_WEBHOOK_URL not set)")
        return

    try:
        # Extract server_id from first message in batch
        server_id = batch[0]["metadata"]["server_id"] if batch else None
        payload = {"server_id": server_id, "messages": batch}
        
        response = requests.post(N8N_INGEST_WEBHOOK_URL, json=payload, timeout=30)
        if response.status_code != 200:
            print(f"  -> Failed to send batch: {response.status_code} {response.text}")
    except Exception as e:
        print(f"  -> Error sending batch: {e}")

@client.event
async def on_ready():
    print(f'Indexer logged in as {client.user}')
    print(f'Starting index of last {DAYS_TO_INDEX} days...')
    
    for guild in client.guilds:
        print(f"Processing Server: {guild.name}")
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).read_message_history:
                await process_channel(channel)
    
    print("Indexing complete. Shutting down.")
    await client.close()

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not set.")
    else:
        client.run(DISCORD_TOKEN)
