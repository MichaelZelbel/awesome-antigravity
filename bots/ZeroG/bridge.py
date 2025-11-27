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

    # 3. Heuristic: Is this a mention, a DM, or a reply to the bot?
    is_mention = client.user.mentioned_in(message)
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_reply_to_bot = (
        message.reference is not None and 
        message.reference.resolved and 
        message.reference.resolved.author.id == client.user.id
    )

    if (is_mention or is_dm or is_reply_to_bot) and N8N_WEBHOOK_URL:
        payload = {
            "content": message.content,
            "author": message.author.name,
            "author_id": str(message.author.id),
            "channel_id": str(message.channel.id),
            "channel_name": message.channel.name, # Context!
            "server_id": str(message.guild.id)
        }
        # Send to n8n and wait for the bot's response
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
            if response.status_code == 200:
                # Extract the bot's answer from n8n response
                bot_answer = response.text
                # Send the answer back to the Discord channel
                await message.channel.send(bot_answer)
            else:
                print(f"n8n returned status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Failed to communicate with n8n: {e}")

client.run(os.getenv('DISCORD_TOKEN'))
