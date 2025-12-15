# Discord Server Cloning - README

## The Problem

Discord's native tools for server cloning are unreliable:
- **Server Templates**: Doesn't accurately copy roles, doesn't copy bots  
- **Xenon Bot**: Claims to delete old roles but doesn't, creates duplicates and mess

## The Solution

We built a custom Python script that actually works: [`clone_server.py`](file:///c:/Dev/AntigravityCommunity/bots/Gravilo/clone_server.py)

This script uses the Discord API directly to:
- ✅ Clone all roles with exact permissions and hierarchy
- ✅ Clone all categories with permissions
- ✅ Clone all channels (text, voice, forum) with permissions
- ✅ Clear existing target server content first (no duplicates)
- ✅ Maintain permission overwrites for roles

## Quick Start

### 1. Install Dependencies

```powershell
cd c:\Dev\AntigravityCommunity\bots\Gravilo
pip install discord.py
```

### 2. Set Bot Token

```powershell
$env:DISCORD_BOT_TOKEN="your_zerog_bot_token_here"
```

(Get the token from the [Discord Developer Portal](https://discord.com/developers/applications/1442892578264715385/bot))

### 3. Get Server IDs

**Production Server ID ("Antigravity Community"):**
- Right-click server icon → Copy Server ID
- (Enable Developer Mode in Discord settings if you don't see this option)

**Test Server ID ("Antigravity Test"):**
- Right-click server icon → Copy Server ID

### 4. Run the Clone Script

```powershell
python clone_server.py <production_server_id> <test_server_id>
```

Example:
```powershell
python clone_server.py 123456789012345678 987654321098765432
```

### 5. Re-invite Bots

After cloning, manually re-invite Gravilo using the permanent invite URL:

**Gravilo Permanent Invite URL:**
```
https://discord.com/api/oauth2/authorize?client_id=1442892578264715385&permissions=534723947584&scope=bot
```

See [`ZEROG_INVITE.md`](file:///c:/Dev/AntigravityCommunity/bots/Gravilo/ZEROG_INVITE.md) for full details and troubleshooting.

## What Gets Cloned

✅ **Roles**
- All custom roles with exact permissions
- Role colors
- Role hierarchy (position)
- Hoisted roles
- Mentionable settings

✅ **Categories**
- All category channels
- Category-level permission overwrites
- Position

✅ **Channels**
- Text channels (with topics, NSFW, slowmode)
- Voice channels (with bitrate, user limits)
- Forum channels
- Channel-level permission overwrites
- Position within categories

## What Doesn't Get Cloned

❌ Members (you'll need to invite test users manually)  
❌ Messages (not needed for testing)  
❌ Server boosts  
❌ Emojis (could be added if needed)  
❌ Bots (must be re-invited manually)

## How It Works

The script:

1. **Connects** to Discord using Gravilo's bot token
2. **Deletes** existing roles/channels in target server (clean slate)
3. **Creates roles** in reverse hierarchy order (top roles first)
4. **Creates categories** with cloned permission overwrites
5. **Creates channels** within categories with permissions
6. **Maps** old IDs to new IDs to maintain permission references

## Troubleshooting

**"Bot is not in source/target server"**
- Make sure Gravilo bot is invited to BOTH servers
- Use the permanent invite URL from `ZEROG_INVITE.md`

**"Permission denied" errors**
- Bot needs Administrator permissions in both servers
- Check bot role is high enough in role hierarchy

**Channels/roles not deleting**
- Some channels may be protected by Discord
- Manually delete them before running script

**Script hangs or times out**
- Discord API has rate limits
- Script includes delays, be patient for large servers

## Re-running the Clone

You can run the script multiple times. It will:
1. Delete everything in the target server
2. Re-clone from source

This is useful if you update the production server and want to refresh the test environment.

---

## Files in This Solution

- [`clone_server.py`](file:///c:/Dev/AntigravityCommunity/bots/Gravilo/clone_server.py) - Main cloning script
- [`ZEROG_INVITE.md`](file:///c:/Dev/AntigravityCommunity/bots/Gravilo/ZEROG_INVITE.md) - Permanent bot invite URL and permissions
- `CLONE_README.md` - This file
