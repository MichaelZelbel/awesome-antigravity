import os
import sys
import json
import logging
import asyncio
import discord
import requests

# n8n message processing webhook
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Supabase guild sync
DISCORD_GUILD_SYNC_URL = os.getenv("DISCORD_GUILD_SYNC_URL")
DISCORD_BOT_SYNC_SECRET = os.getenv("DISCORD_BOT_SYNC_SECRET")

# Correct Supabase usage increment endpoint
SERVER_USAGE_INCREMENT_URL = os.getenv("SERVER_USAGE_INCREMENT_URL")  # should be discord-message-usage


# Basic config
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("bridge")


def _build_guild_icon_url(guild: discord.Guild):
    icon_url = None
    icon_attr = getattr(guild, "icon", None)
    if icon_attr is not None:
        icon_url = getattr(icon_attr, "url", None) or str(icon_attr)
    else:
        legacy_icon = getattr(guild, "icon_url", None)
        if legacy_icon:
            icon_url = str(legacy_icon)
    return icon_url


def guild_sync_request(guild: discord.Guild):
    if not DISCORD_GUILD_SYNC_URL or not DISCORD_BOT_SYNC_SECRET:
        logger.warning("[Guild Sync] Missing guild sync config — skipping")
        return

    payload = {
        "discord_guild_id": str(guild.id),
        "discord_owner_id": str(getattr(guild, "owner_id", "")),
        "name": guild.name,
        "icon_url": _build_guild_icon_url(guild),
        "message_limit": 3000,
    }

    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": DISCORD_BOT_SYNC_SECRET,
    }

    try:
        resp = requests.post(
            DISCORD_GUILD_SYNC_URL, headers=headers, data=json.dumps(payload), timeout=10
        )
        if resp.status_code < 300:
            logger.info("[Guild Sync] Synced guild %s (%s)", guild.name, guild.id)
        else:
            logger.warning(
                "[Guild Sync] FAILED: status %s body=%s", resp.status_code, resp.text
            )
    except Exception as e:
        logger.error("[Guild Sync] Exception: %s", e)


async def guild_sync(guild: discord.Guild):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, guild_sync_request, guild)


async def increment_usage(server_id, amount=1):
    """Call Supabase usage tracking function."""
    if not SERVER_USAGE_INCREMENT_URL or not DISCORD_BOT_SYNC_SECRET:
        logger.warning("[Usage] Missing SERVER_USAGE_INCREMENT_URL or DISCORD_BOT_SYNC_SECRET")
        return

    payload = {
        "discord_guild_id": str(server_id),
        "messages": int(amount),
    }

    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": DISCORD_BOT_SYNC_SECRET,
    }

    try:
        resp = requests.post(SERVER_USAGE_INCREMENT_URL, json=payload, headers=headers, timeout=10)
        logger.info("[Usage] Incremented guild %s by %s (status=%s)", server_id, amount, resp.status_code)
    except Exception as e:
        logger.error("[Usage] Error: %s", e)


@client.event
async def on_ready():
    logger.info("Logged in as %s", client.user)

    logger.info("[Guild Sync] Backfilling %d guild(s)...", len(client.guilds))
    for guild in client.guilds:
        asyncio.create_task(guild_sync(guild))


@client.event
async def on_guild_join(guild: discord.Guild):
    logger.info("[Discord] Joined guild %s (%s)", guild.name, guild.id)
    asyncio.create_task(guild_sync(guild))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    channel_name = getattr(message.channel, "name", "DM")

    logger.info(
        "[bridge] Incoming message from %s in #%s (guild=%s): %r",
        message.author,
        channel_name,
        getattr(message.guild, "id", None),
        message.content,
    )

    if not N8N_WEBHOOK_URL:
        logger.warning("N8N_WEBHOOK_URL missing; skipping")
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
            bot_answer = response.text.strip()

            if bot_answer:
                await message.channel.send(bot_answer)

            if message.guild:
                await increment_usage(server_id=message.guild.id, amount=1)

        else:
            logger.warning("n8n returned %s: %s", response.status_code, response.text)

    except Exception as e:
        logger.error("Failed to communicate with n8n: %s", e)


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN is not set.")
        sys.exit(1)
    client.run(token)
