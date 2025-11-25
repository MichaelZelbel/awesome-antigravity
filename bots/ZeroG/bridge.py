import discord
import requests
import os

# Your n8n Webhook URL (The "Ear" of your flow)
# REPLACE THIS with your actual n8n webhook URL
# Your n8n Webhook URL (The "Ear" of your flow)
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# Basic config
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not N8N_WEBHOOK_URL:
        print("WARNING: N8N_WEBHOOK_URL environment variable is not set!")

@client.event
async def on_message(message):
    # 1. Don't listen to yourself or other bots (avoids infinite loops)
    if message.author.bot:
        return

    # 2. (Optional) Only listen in specific Channel IDs (e.g., #help, #general)
    # allowed_channels = [123456789, 987654321]
    # if message.channel.id not in allowed_channels:
    #     return

    # 3. Simple Heuristic: Is this a question?
    # This saves n8n executions. You can make this smarter later.
    content = message.content.lower()
    is_question = "?" in content or any(w in content for w in ["error", "bug", "help", "fix", "fail", "broken"])

    if is_question and N8N_WEBHOOK_URL:
        payload = {
            "content": message.content,
            "author": message.author.name,
            "author_id": str(message.author.id),
            "channel_id": str(message.channel.id),
            "channel_name": message.channel.name, # Context!
            "server_id": str(message.guild.id)
        }
        # Send to n8n and forget (don't wait for response)
        try:
            requests.post(N8N_WEBHOOK_URL, json=payload, timeout=1)
        except Exception as e:
            print(f"Failed to send to n8n: {e}")

client.run(os.getenv('DISCORD_TOKEN'))
