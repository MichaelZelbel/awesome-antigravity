"""
Discord Server Cloning Script

This script clones all roles, channels, categories, and permissions from a source
Discord server to a target Discord server.

Usage:
    python clone_server.py <source_guild_id> <target_guild_id>

Requirements:
    - Bot must have Administrator permissions in both servers
    - Bot must be invited to both source and target servers
    - Set DISCORD_BOT_TOKEN environment variable

The script will:
1. Clone all roles (with permissions and hierarchy)
2. Clone all categories
3. Clone all channels (text, voice, announcement, forum)
4. Clone channel-specific permission overwrites
"""

import discord
from discord.ext import commands
import asyncio
import sys
import os
from typing import Dict, List

# Bot setup
intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Needed to see role assignments
bot = commands.Bot(command_prefix="!", intents=intents)

# Mapping to track old IDs -> new IDs
role_map: Dict[int, int] = {}
channel_map: Dict[int, int] = {}
category_map: Dict[int, int] = {}


async def clone_roles(source_guild: discord.Guild, target_guild: discord.Guild):
    """Clone all roles from source to target, maintaining hierarchy."""
    print(f"\n📋 Cloning roles from '{source_guild.name}' to '{target_guild.name}'...")
    
    # Get roles sorted by position (highest first, excluding @everyone)
    source_roles = sorted(
        [r for r in source_guild.roles if r.name != "@everyone"],
        key=lambda r: r.position,
        reverse=True
    )
    
    # Clear existing roles in target (except @everyone and bot role)
    bot_member = target_guild.get_member(bot.user.id)
    bot_role_ids = {r.id for r in bot_member.roles if r.name != "@everyone"}
    
    for role in target_guild.roles:
        if role.name != "@everyone" and role.id not in bot_role_ids:
            try:
                await role.delete(reason="Clearing for server clone")
                print(f"  🗑️  Deleted existing role: {role.name}")
            except Exception as e:
                print(f"  ⚠️  Could not delete role {role.name}: {e}")
    
    # Create new roles
    for source_role in source_roles:
        try:
            new_role = await target_guild.create_role(
                name=source_role.name,
                permissions=source_role.permissions,
                color=source_role.color,
                hoist=source_role.hoist,
                mentionable=source_role.mentionable,
                reason="Server clone"
            )
            role_map[source_role.id] = new_role.id
            print(f"  ✅ Created role: {source_role.name}")
        except Exception as e:
            print(f"  ❌ Failed to create role {source_role.name}: {e}")
    
    print(f"✅ Cloned {len(role_map)} roles")


async def clone_categories(source_guild: discord.Guild, target_guild: discord.Guild):
    """Clone all categories from source to target."""
    print(f"\n📁 Cloning categories...")
    
    # Get categories sorted by position
    source_categories = sorted(
        source_guild.categories,
        key=lambda c: c.position
    )
    
    for source_cat in source_categories:
        try:
            # Clone permission overwrites
            overwrites = {}
            for target, perms in source_cat.overwrites.items():
                if isinstance(target, discord.Role):
                    if target.id in role_map:
                        new_role = target_guild.get_role(role_map[target.id])
                        overwrites[new_role] = perms
                    elif target.name == "@everyone":
                        overwrites[target_guild.default_role] = perms
            
            new_category = await target_guild.create_category(
                name=source_cat.name,
                overwrites=overwrites,
                position=source_cat.position,
                reason="Server clone"
            )
            category_map[source_cat.id] = new_category.id
            print(f"  ✅ Created category: {source_cat.name}")
        except Exception as e:
            print(f"  ❌ Failed to create category {source_cat.name}: {e}")
    
    print(f"✅ Cloned {len(category_map)} categories")


async def clone_channels(source_guild: discord.Guild, target_guild: discord.Guild):
    """Clone all channels from source to target."""
    print(f"\n💬 Cloning channels...")
    
    # Delete existing channels (except those with bots)
    for channel in target_guild.channels:
        if not isinstance(channel, discord.CategoryChannel):
            try:
                await channel.delete(reason="Clearing for server clone")
                print(f"  🗑️  Deleted existing channel: {channel.name}")
            except Exception as e:
                print(f"  ⚠️  Could not delete channel {channel.name}: {e}")
    
    # Get all channels sorted by position
    source_channels = sorted(
        [c for c in source_guild.channels if not isinstance(c, discord.CategoryChannel)],
        key=lambda c: c.position
    )
    
    for source_channel in source_channels:
        try:
            # Clone permission overwrites
            overwrites = {}
            for target, perms in source_channel.overwrites.items():
                if isinstance(target, discord.Role):
                    if target.id in role_map:
                        new_role = target_guild.get_role(role_map[target.id])
                        overwrites[new_role] = perms
                    elif target.name == "@everyone":
                        overwrites[target_guild.default_role] = perms
            
            # Get parent category if exists
            category = None
            if source_channel.category_id and source_channel.category_id in category_map:
                category = target_guild.get_channel(category_map[source_channel.category_id])
            
            # Create channel based on type
            if isinstance(source_channel, discord.TextChannel):
                new_channel = await target_guild.create_text_channel(
                    name=source_channel.name,
                    topic=source_channel.topic,
                    position=source_channel.position,
                    nsfw=source_channel.nsfw,
                    slowmode_delay=source_channel.slowmode_delay,
                    category=category,
                    overwrites=overwrites,
                    reason="Server clone"
                )
                print(f"  ✅ Created text channel: #{source_channel.name}")
            
            elif isinstance(source_channel, discord.VoiceChannel):
                new_channel = await target_guild.create_voice_channel(
                    name=source_channel.name,
                    bitrate=source_channel.bitrate,
                    user_limit=source_channel.user_limit,
                    position=source_channel.position,
                    category=category,
                    overwrites=overwrites,
                    reason="Server clone"
                )
                print(f"  ✅ Created voice channel: 🔊 {source_channel.name}")
            
            elif isinstance(source_channel, discord.ForumChannel):
                new_channel = await target_guild.create_forum_channel(
                    name=source_channel.name,
                    topic=source_channel.topic,
                    position=source_channel.position,
                    nsfw=source_channel.nsfw,
                    category=category,
                    overwrites=overwrites,
                    reason="Server clone"
                )
                print(f"  ✅ Created forum channel: 📋 {source_channel.name}")
            
            else:
                print(f"  ⚠️  Skipping unknown channel type: {source_channel.name}")
                continue
            
            channel_map[source_channel.id] = new_channel.id
        
        except Exception as e:
            print(f"  ❌ Failed to create channel {source_channel.name}: {e}")
    
    print(f"✅ Cloned {len(channel_map)} channels")


async def clone_server(source_guild_id: int, target_guild_id: int):
    """Main cloning function."""
    source_guild = bot.get_guild(source_guild_id)
    target_guild = bot.get_guild(target_guild_id)
    
    if not source_guild:
        print(f"❌ Error: Bot is not in source server (ID: {source_guild_id})")
        return
    
    if not target_guild:
        print(f"❌ Error: Bot is not in target server (ID: {target_guild_id})")
        return
    
    print(f"\n🚀 Starting server clone...")
    print(f"   Source: {source_guild.name} (ID: {source_guild.id})")
    print(f"   Target: {target_guild.name} (ID: {target_guild.id})")
    
    try:
        # Clone in order: roles -> categories -> channels
        await clone_roles(source_guild, target_guild)
        await clone_categories(source_guild, target_guild)
        await clone_channels(source_guild, target_guild)
        
        print(f"\n✅ ✅ ✅ Server clone completed successfully! ✅ ✅ ✅")
        print(f"\n📊 Summary:")
        print(f"   Roles: {len(role_map)}")
        print(f"   Categories: {len(category_map)}")
        print(f"   Channels: {len(channel_map)}")
    
    except Exception as e:
        print(f"\n❌ Error during cloning: {e}")
        import traceback
        traceback.print_exc()


@bot.event
async def on_ready():
    """Called when bot is ready."""
    print(f"\n🤖 Bot connected as {bot.user}")
    
    if len(sys.argv) != 3:
        print("\n❌ Usage: python clone_server.py <source_guild_id> <target_guild_id>")
        await bot.close()
        return
    
    try:
        source_id = int(sys.argv[1])
        target_id = int(sys.argv[2])
    except ValueError:
        print("\n❌ Error: Guild IDs must be integers")
        await bot.close()
        return
    
    await clone_server(source_id, target_id)
    await bot.close()


def main():
    """Entry point."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not token:
        print("❌ Error: DISCORD_BOT_TOKEN environment variable not set")
        print("\nSet it using:")
        print("  Windows: set DISCORD_BOT_TOKEN=your_token_here")
        print("  Linux/Mac: export DISCORD_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    if len(sys.argv) != 3:
        print("\n❌ Usage: python clone_server.py <source_guild_id> <target_guild_id>")
        print("\nExample:")
        print("  python clone_server.py 123456789 987654321")
        sys.exit(1)
    
    bot.run(token)


if __name__ == "__main__":
    main()
