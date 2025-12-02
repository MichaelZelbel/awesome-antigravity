import os
import sys
import json
import logging
import asyncio
import discord
import requests

# Your n8n Webhook URL (The "Ear" of your flow)
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# Gravilo SaaS sync configuration
GRAVILO_BASE_URL = os.getenv("GRAVILO_BASE_URL")
DISCORD_BOT_SYNC_SECRET = os.getenv("DISCORD_BOT_SYNC_SECRET")

# Basic config
intents = discord.Intents.default()
intents.message_content = True   # needed for on_message
intents.guilds = True            # needed for guild join/remove
client = discord.Client(intents=intents)

# Make sure logging goes to stdout with INFO level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("bridge")


def gravilo_sync_request(path: str, payload: dict):
    """
    Synchronous HTTP call to Gravilo SaaS for server sync.
    This is run in a background thread so it does not block the event loop.
    """
    if not GRAVILO_BASE_URL or not DISCORD_BOT_SYNC_SECRET:
        logger.warning(
            "[Gravilo Sync] Missing GRAVILO_BASE_URL or DISCORD_BOT_SYNC_SECRET — skipping sync"
        )
        return

    url = f"{GRAVILO_BASE_URL.rstrip('/')}/api/discord/{path}"
    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": DISCORD_BOT_SYNC_SECRET,
    }

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if 200 <= resp.status_code < 300:
            logger.info(
                "[Gravilo Sync] %s succeeded for guild %s (status %s)",
                path,
                payload.get("discord_server_id"),
                resp.status_code,
            )
        else:
            logger.warning(
                "[Gravilo Sync] %s FAILED for guild %s: status %s, body: %s",
                path,
                payload.get("discord_server_id"),
                resp.status_code,
                resp.text,
            )
    except Exception as e:
        logger.error(
            "[Gravilo Sync] Exception during %s for guild %s: %s",
            path,
            payload.get("discord_server_id"),
            e,
        )


async def gravilo_sync(path: str, payload: dict):
    """
    Async wrapper that runs gravilo_sync_request() in a thread executor.
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, gravilo_sync_request, path, payload)


@client.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info("Logged in as %s", client.user)
    if not N8N_WEBHOOK_URL:
        logger.warning("N8N_WEBHOOK_URL environment variable is not set!")
    if not GRAVILO_BASE_URL or not DISCORD_BOT_SYNC_SECRET:
        logger.warning("Gravilo sync disabled, missing GRAVILO_BASE_URL or DISCORD_BOT_SYNC_SECRET")


@client.event
async def on_guild_join(guild: discord.Guild):
    """Called when the bot joins a new guild."""
    # Safely derive icon_url across discord.py versions
    icon_url = None
    icon_attr = getattr(guild, "icon", None)
    if icon_attr is not None:
        icon_url = getattr(icon_attr, "url", None) or str(icon_attr)
    else:
        legacy_icon = getattr(guild, "icon_url", None)
        if legacy_icon:
            icon_url = str(legacy_icon)

    owner_id = getattr(guild, "owner_id", None)

    payload = {
        "discord_server_id": str(guild.id),
        "name": guild.name,
        "icon_url": icon_url,
        "owner_discord_id": str(owner_id) if owner_id is not None else None,
    }

    logger.info("[Discord] Joined guild %s (%s)", guild.name, guild.id)
    asyncio.create_task(gravilo_sync("server-sync", payload))


@client.event
async def on_guild_remove(guild: discord.Guild):
    """Called when the bot is removed from a guild."""
    payload = {
        "discord_server_id": str(guild.id),
    }
    logger.info("[Discord] Removed from guild %s (%s)", guild.name, guild.id)
    asyncio.create_task(gravilo_sync("server-disconnected", payload))


@client.event
async def on_message(message):
    """Called when a message is received."""
    # 1. Don't listen to yourself or other bots (avoids infinite loops)
    if message.author.bot:
        return

    channel_name = getattr(message.channel, "name", "DM")
    guild_id = getattr(message.guild, "id", None)

    # DEBUG: show that we see messages at all
    logger.info(
        "[bridge] Incoming message from %s in #%s (guild=%s): %r",
        message.author,
        channel_name,
        guild_id,
        message.content,
    )

    if not N8N_WEBHOOK_URL:
        logger.warning("N8N_WEBHOOK_URL is not set, skipping message.")
        return

    # 2. Forward EVERY non-bot message to n8n
    payload = {
        "content": message.content,
        "author": message.author.name,
        "author_id": str(message.author.id),
        "channel_id": str(message.channel.id),
        "channel_name": channel_name,
        "server_id": str(message.guild.id) if message.guild else None,
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
        if response.status_code == 200:
            bot_answer = response.text
            await message.channel.send(bot_answer)
        else:
            logger.warning("n8n returned status %s: %s", response.status_code, response.text)
    except requests.RequestException as e:
        logger.error("Failed to communicate with n8n: %s", e)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        logger.error("DISCORD_TOKEN environment variable is not set.")
        sys.exit(1)
    client.run(TOKEN)
