import os
import sys
import json
import logging
import asyncio
import discord
import requests

# n8n webhook for message handling
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Guild sync config (Supabase Edge Function)
DISCORD_GUILD_SYNC_URL = os.getenv("DISCORD_GUILD_SYNC_URL")
DISCORD_BOT_SYNC_SECRET = os.getenv("DISCORD_BOT_SYNC_SECRET")

# Usage tracking config (Supabase Edge Function)
# Example:
# SERVER_USAGE_INCREMENT_URL=https://sohyviltwgpuslbjzqzh.supabase.co/functions/v1/discord-message-usage
SERVER_USAGE_INCREMENT_URL = os.getenv("SERVER_USAGE_INCREMENT_URL")
N8N_USAGE_SECRET = os.getenv("N8N_USAGE_SECRET")

# Basic config
intents = discord.Intents.default()
intents.message_content = True   # needed for on_message
intents.guilds = True            # needed for guild join/remove
client = discord.Client(intents=intents)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("bridge")


def _build_guild_icon_url(guild: discord.Guild):
    """Safely get an icon URL across discord.py versions."""
    icon_url = None
    icon_attr = getattr(guild, "icon", None)
    if icon_attr is not None:
        # discord.py 2.x: guild.icon is an Asset with .url
        icon_url = getattr(icon_attr, "url", None) or str(icon_attr)
    else:
        legacy_icon = getattr(guild, "icon_url", None)
        if legacy_icon:
            icon_url = str(legacy_icon)
    return icon_url


def guild_sync_request(guild: discord.Guild):
    """
    Synchronous HTTP call to Supabase Edge Function to sync guild metadata.
    """
    if not DISCORD_GUILD_SYNC_URL or not DISCORD_BOT_SYNC_SECRET:
        logger.warning(
            "[Guild Sync] Missing DISCORD_GUILD_SYNC_URL or DISCORD_BOT_SYNC_SECRET — skipping sync"
        )
        return

    payload = {
        "discord_guild_id": str(guild.id),
        "discord_owner_id": str(getattr(guild, "owner_id", "")),
        "name": guild.name,
        "icon_url": _build_guild_icon_url(guild),
        # optional, but matches Lovable’s example
        "message_limit": 3000,
    }

    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": DISCORD_BOT_SYNC_SECRET,
    }

    try:
        resp = requests.post(
            DISCORD_GUILD_SYNC_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=10,
        )
        if 200 <= resp.status_code < 300:
            logger.info(
                "[Guild Sync] Synced guild %s (%s), status %s",
                guild.name,
                guild.id,
                resp.status_code,
            )
        else:
            logger.warning(
                "[Guild Sync] FAILED for guild %s (%s): status %s, body: %s",
                guild.name,
                guild.id,
                resp.status_code,
                resp.text,
            )
    except Exception as e:
        logger.error(
            "[Guild Sync] Exception during sync for guild %s (%s): %s",
            guild.name,
            guild.id,
            e,
        )


async def guild_sync(guild: discord.Guild):
    """
    Async wrapper to run guild_sync_request in a thread.
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, guild_sync_request, guild)


async def increment_usage(server_id, amount=1):
    """
    Async helper to increment usage via Supabase Edge Function.
    Expects the discord-message-usage function with:
      - Header: x-bot-secret
      - Body: { "discord_guild_id": "...", "messages": <int> }
    """
    if not SERVER_USAGE_INCREMENT_URL or not N8N_USAGE_SECRET:
        logger.warning("[Usage] Missing SERVER_USAGE_INCREMENT_URL or N8N_USAGE_SECRET")
        return

    payload = {
        "discord_guild_id": str(server_id),
        "messages": int(amount),
    }

    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": N8N_USAGE_SECRET,
    }

    try:
        resp = requests.post(
            SERVER_USAGE_INCREMENT_URL,
            json=payload,
            headers=headers,
            timeout=10,
        )
        logger.info(
            "[Usage] Incremented guild %s by %s (status %s, body=%r)",
            server_id,
            amount,
            resp.status_code,
            resp.text,
        )
    except Exception as e:
        logger.error("[Usage] Error incrementing usage: %s", e)


@client.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info("Logged in as %s", client.user)
    if not N8N_WEBHOOK_URL:
        logger.warning("N8N_WEBHOOK_URL environment variable is not set!")
    if not DISCORD_GUILD_SYNC_URL or not DISCORD_BOT_SYNC_SECRET:
        logger.warning(
            "Guild sync disabled, missing DISCORD_GUILD_SYNC_URL or DISCORD_BOT_SYNC_SECRET"
        )

    # Backfill: sync all guilds the bot is already in
    logger.info("[Guild Sync] Backfilling %d guild(s)...", len(client.guilds))
    for guild in client.guilds:
        asyncio.create_task(guild_sync(guild))


@client.event
async def on_guild_join(guild: discord.Guild):
    """Called when the bot joins a new guild."""
    logger.info("[Discord] Joined guild %s (%s)", guild.name, guild.id)
    asyncio.create_task(guild_sync(guild))


@client.event
async def on_message(message):
    """Called when a message is received."""
    # 1. Don't listen to yourself or other bots (avoids infinite loops)
    if message.author.bot:
        return

    channel_name = getattr(message.channel, "name", "DM")
    guild_id = getattr(message.guild, "id", None)

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
            # increment usage for this server after a successful reply
            if message.guild:
                await increment_usage(server_id=message.guild.id, amount=1)
        else:
            logger.warning(
                "n8n returned status %s: %s", response.status_code, response.text
            )
    except requests.RequestException as e:
        logger.error("Failed to communicate with n8n: %s", e)


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        logger.error("DISCORD_TOKEN environment variable is not set.")
        sys.exit(1)
    client.run(TOKEN)
