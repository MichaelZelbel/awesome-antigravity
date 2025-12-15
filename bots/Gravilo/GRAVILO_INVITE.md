# Gravilo Bot - Permanent Invite URL

## Current Permissions Required

Based on Gravilo's n8n workflow functionality, the bot needs:

### Required Permissions
- **Read Messages/View Channels** - See channels and messages
- **Send Messages** - Respond to user queries  
- **Read Message History** - Access conversation context
- **Mention Everyone** - (if Gravilo needs to @mention users/roles)
- **Add Reactions** - (if Gravilo provides reactions)
- **Attach Files** - (if Gravilo shares images/documents)
- **Embed Links** - Display rich embeds in responses

### Permission Integer
The above permissions translate to: **379968** (basic read/send)  
Or with additional powers: **534723947584** (recommended)

## Permanent OAuth2 Invite URL

**CORRECT URL (Generated from OAuth2 page):**

```
https://discord.com/api/oauth2/authorize?client_id=1442892578264715385&permissions=379968&scope=bot
```

This URL includes:
- `scope=bot` - Makes it a proper bot (creates bot role)
- `permissions=379968` - View Channels, Send Messages, Read Message History, Embed Links, Attach Files

### How to Use This URL

1. **To invite Gravilo to a new server:**
   - Copy the URL above
   - Paste it into your browser
   - Select the target server from dropdown
   - Click "Authorize"

2. **To update Gravilo's permissions on an existing server:**
   - Use the same URL
   - Re-authorize on the server
   - Discord will update the bot's permissions

## Why This Works

Unlike the "Add App" dialog in Discord which uses simplified integration:
- This OAuth2 URL explicitly requests specific permissions
- The permissions are encoded directly in the URL
- It won't change unless you generate a new URL with different permissions
- It's immune to Developer Portal permission checkbox issues

## Regenerating the URL

If you need different permissions in the future:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications/1442892578264715385/bot)
2. Click **OAuth2** → **URL Generator** (not the Bot page)
3. Check scopes: `bot`
4. Check the permissions you need
5. Copy the generated URL
6. Update this file

## Testing

After inviting Gravilo to "Antigravity Test" with this URL:

1. Verify bot appears online
2. Send: `@Gravilo test message`
3. Check n8n webhook receives the message
4. Verify bot can respond

## Troubleshooting

**Bot shows as offline:**
- Check that the bridge.py or n8n workflow is running
- Verify the bot token hasn't been regenerated

**Bot can't send messages:**
- Re-invite using the URL above
- Check channel-specific permissions aren't blocking the bot
- Ensure bot role is above any restricted roles

**Permissions keep resetting:**
- Stop using "Add App" dialog - always use this OAuth2 URL
- Don't modify permissions in the Developer Portal Bot page (they don't persist to servers)
