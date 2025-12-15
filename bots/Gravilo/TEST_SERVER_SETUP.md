# Gravilo Test Server - ACTUAL Working Solution

## The Real Problem

Gravilo is a Discord bot that runs as `bridge.py`. The OAuth2 invite succeeded, but the bot appears **offline** because:

- `bridge.py` is deployed to Coolify and connected to Discord with one bot token
- That same bot token works across ALL servers the bot is invited to
- **The bot is already running and will work on the test server too**

## Why You Don't See It

Discord shows bots as "offline" until they connect to the gateway. Since `bridge.py` is already running in Coolify:

1. Check if `bridge.py` is actually running in Coolify
2. Check the Coolify logs - it should say "Logged in as Gravilo"
3. If it's running, **Gravilo should already appear online on your test server**

## Quick Test

Go to "Antigravity Test" server and:
1. Check the member list on the right - is Gravilo there (even if offline)?
2. In any channel, type: `@Gravilo test`
3. Check if Gravilo responds

If Gravilo doesn't appear in the member list at all after the successful OAuth2 invite, **this is a Discord caching bug**.

## Fix: Discord Cache Bug

If the invite said "Success" but Gravilo doesn't appear:

1. **Close Discord completely** (not just minimize - actually quit)
2. Reopen Discord
3. Go to "Antigravity Test" server
4. Check member list again

OR

1. Right-click "Antigravity Test" server icon
2. **Leave Server**
3. Rejoin using an invite link
4. Check member list

## Verify Bot is Running

Check your Coolify deployment:

1. Go to Coolify Dashboard
2. Find the Gravilo bridge service
3. Check the logs
4. Look for: `Logged in as Gravilo#XXXX`

If you see that, the bot IS connected to Discord and IS online on both production and test servers.

## The Bot Works on Both Servers

Once `bridge.py` is running with the token, Gravilo automatically:
- Connects to Discord's gateway
- Appears online on ALL servers it's been invited to
- Listens for messages on ALL those servers
- Responds via n8n webhook

**You don't need separate instances.** One running `bridge.py` = works everywhere.

## If You Need Different Behavior Per Server

If you want Gravilo to behave differently on test vs production:

The current [`bridge.py`](file:///c:/Dev/AntigravityCommunity/bots/Gravilo/bridge.py#L51) already captures `server_id`:

```python
"server_id": str(message.guild.id)
```

Your n8n workflow can use this to:
- Route to different databases
- Use different prompts
- Apply different logic

**No code changes needed** - just configure your n8n workflow to check `server_id`.

## Bottom Line

1. Make sure `bridge.py` is running in Coolify (check logs)
2. Restart Discord client to clear cache
3. Gravilo should appear online on test server
4. Test with `@Gravilo hello`

That's it. No separate deployment, no pip, no python needed. Just make sure the existing deployment is running.
