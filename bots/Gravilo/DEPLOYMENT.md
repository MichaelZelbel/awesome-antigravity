# 🚀 Gravilo Bridge - Coolify Deployment Guide

This guide will help you deploy the **Gravilo Bridge** (the "Ears" of your bot) to your **Coolify** instance.

## Prerequisites
-   Access to your Coolify Dashboard.
-   Your **Discord Bot Token** (from Discord Developer Portal).
-   Your **n8n Webhook URL** (from your `Discord_Handler` workflow).

---

## Step 1: Prepare your Repository
Ensure your GitHub repository (`awesome-antigravity`) is synced with the latest changes, including:
-   `bots/Gravilo/bridge.py`
-   `bots/Gravilo/Dockerfile`
-   `bots/Gravilo/requirements.txt`

## Step 2: Create a New Resource in Coolify
1.  Go to your **Coolify Dashboard**.
2.  Select your **Project** and **Environment**.
3.  Click **+ New**.
4.  Select **Git Repository** (Public or Private).
5.  Select your `awesome-antigravity` repository.
    *   *Note: If it's private, make sure you've added the Coolify Deploy Key to your GitHub repo settings.*

## Step 3: Configure the Service
1.  **Branch**: `main` (or your working branch).
2.  **Build Pack**: Select **Dockerfile**.
3.  **Base Directory**: `/bots/Gravilo` (This is crucial! It tells Coolify where to find the Dockerfile).
4.  Click **Continue**.

## Step 4: Environment Variables
Before deploying, you need to set the secrets.
1.  Go to the **Environment Variables** (or Secrets) tab of your new service.
2.  Add the following variables:
    *   `DISCORD_TOKEN`: `your_discord_bot_token_here`
    *   `N8N_WEBHOOK_URL`: `https://your-n8n-instance.com/webhook/discord-listener` (Replace with your actual URL)

## Step 5: Deploy
1.  Click **Deploy**.
2.  Watch the logs. Coolify will build the Docker image and start the container.
3.  Once it says "Healthy" or "Running", your bridge is live!

## Step 6: Verify
1.  Go to your Discord Server.
2.  Type a question (e.g., "How do I use the file search?").
3.  Check your **n8n Executions** list. You should see a new execution for `Discord_Handler`.
4.  Gravilo should reply!

---

### 🛑 Troubleshooting
-   **Bot not responding?**
    -   Check Coolify logs: Is the python script running? Did it say "Logged in as..."?
    -   Check Discord Developer Portal: Did you enable **MESSAGE CONTENT INTENT**?
    -   Check n8n: Is the workflow active? Is the webhook URL correct?
-   **NameResolutionError / DNS Issues?**
    -   If you see `Failed to resolve '...'`, your Docker container cannot see the public internet domain of your n8n instance.
    -   **Fix:** Use the internal Docker Gateway IP instead of the domain.
    -   Change `N8N_WEBHOOK_URL` to: `http://172.17.0.1:[N8N_PORT]/webhook/zerog`
    -   *(Check your n8n service in Coolify to find the public mapped port, usually 5678).*
