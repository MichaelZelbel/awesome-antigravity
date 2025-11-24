# ZeroG 🤖

**ZeroG** is the official AI-powered Discord bot for the Antigravity Community. He's your nerdy developer buddy, here to help with technical questions and share a laugh.

## 📂 Structure

This bot is built using **n8n** workflows.

-   `/workflows`: Contains the JSON workflow files to import into n8n.

## 🚀 Setup

### n8n Workflows
1.  **Import Workflows**: Import the JSON files from the `workflows` directory into your n8n instance.
2.  **Credentials**: Set up Google Gemini API credentials in n8n.
3.  **Update Placeholders**: Replace `YOUR_PROJECT_ID`, `YOUR_CORPUS_ID`, and credential IDs in the workflows.

### Bridge Script (The Listener)
1.  **Deploy to Coolify**: Follow the instructions in `DEPLOYMENT.md`.
2.  **Environment Variables**:
    -   `DISCORD_TOKEN`: Your Discord bot token.
    -   `N8N_WEBHOOK_URL`: Your n8n webhook URL (from the `Discord_Handler` workflow).
3.  **Enable Discord Intent**: Go to Discord Developer Portal → Your App → Bot → Enable **MESSAGE CONTENT INTENT**.

## 🧠 Persona

-   **Name**: ZeroG
-   **Vibe**: Nerdy, helpful, intelligent humor.
-   **Catchphrases**: "Compiling...", "Deploying fix...", "In the pipe, five by five."
