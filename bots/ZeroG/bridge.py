import os
import sys
import json
import logging
import discord
import requests
import aiohttp  # NEW: async HTTP client for Gravilo sync

# Your n8n Webhook URL (The "Ear" of your flow)
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# Gravilo SaaS sync configuration
GRAVILO_BASE_URL = os.getenv("GRAVILO_BASE_URL")  # e.g. https://gravilo.ai
DISCORD_BOT_SYNC_SECRET = os.getenv("DISCORD_BOT_SYNC_SECRET")

# Basic config
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # NEW: ensure guild join/remove events work
client = discord.Client(intents=intents)


async def gravilo_sync(path: str, payload: dict):
    """
    Send a JSON payload to the Gravilo SaaS backend for server sync.

    path: "server-sync" or "server-disconnected"
    payload: dict containing discord_server_id and other metadata
    """
    if not GRAVILO_BASE_URL or not DISCORD_BOT_SYNC_SECRET:
        logging.warning(
            "[Gravilo Sync] Missing GRAVILO_BASE_URL or DISCORD_BOT_SYNC_SECRET — skipping sync"
        )
        return

    url = f"{GRAVILO_BASE_URL.rstrip('/')}/api/discord/{path}"
    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": DISCORD_BOT_SYNC_SECRET,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(payload)) as resp:
                if 200 <= resp.status < 300:
                    logging.info(
                        f"[Gravilo Sync] {path} succeeded for guild {payload.get('discord_server_id')} "
                        f"(status {resp.status})"
                    )
                else:
                    body = await resp.text()
                    logging.warning(
                        f"[Gravilo Sync] {path} FAILED for guild {payload.get('discord_server_id')}: "
                        f"status {resp.status}, body: {body}"
                    )
    except Exception as e:
        logging.error(
            f"[Gravilo Sync] Exception during {path} for guild {payload.get('discord_server_id')}: {e}"
        )


@client.event
async def on_ready():
    """Called when the bot is ready."""
    print(f'Logged in as {client.user}')
    if not N8N_WEBHOOK_URL:
        print("WARNING: N8N_WEBHOOK_URL environment variable is not set!")

    if not GRAVILO_BASE_URL or not DISCORD_BOT_SYNC_SECRET:
        print("WARNING: Gravilo sync disabled, missing GRAVILO_BASE_URL or DISCORD_BOT_SYNC_SECRET")

    # Optionally sync all guilds on startup
    for guild in client.guilds:
        payload = {
            "discord_server_id": str(guild.id),
            "name": guild.name,
            "icon_url": guild.icon.url if guild.icon else None,
            "owner_discord_id": str(getattr(guild, "owner_id", None)) or None,
        }
        client.loop.create_task(gravilo_sync("server-sync", payload))


@client.event
async def on_guild_join(guild: discord.Guild):
    """Called when the bot joins a new guild."""
    payload = {
        "discord_server_id": str(guild.id),
        "name": guild.name,
        "icon_url": guild.icon.url if guild.icon else None,
        "owner_discord_id": str(getattr(guild, "owner_id", None)) or None,
    }
    client.loop.create_task(gravilo_sync("server-sync", payload))


@client.event
async def on_guild_remove(guild: discord.Guild):
    """Called when the bot is removed from a guild."""
    payload = {"discord_server_id": str(guild.id)}
    client.loop.create_task(gravilo_sync("server-disconnected", payload))


@client.event
async def on_message(message):
    """Called when a message is received."""
    # 1. Don't listen to yourself or other bots (avoids infinite loops)
    if message.author.bot:
        return

    # 2. Heuristic: mention, DM, or reply
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
            "channel_name": message.channel.name,
            "server_id": str(message.guild.id) if message.guild else None,
        }

        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
            if response.status_code == 200:
                bot_answer = response.text
                await message.channel.send(bot_answer)
            else:
                print(f"n8n returned status {response.status_code}: {response.text}")
        except requests.RequestException as e:
            print(f"Failed to communicate with n8n: {e}")


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable is not set.")
        sys.exit(1)

    client.run(TOKEN)
