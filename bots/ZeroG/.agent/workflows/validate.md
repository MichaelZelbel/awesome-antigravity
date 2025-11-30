---
description: Run the comprehensive validation suite (Lint, Type Check, Test, Config, Browser)
---

# Ultimate Validation Suite

This workflow validates the ZeroG bot codebase, configuration, and behavior using a multi-layered approach.

## Phases

1.  **Setup Dependencies**
    Install the required development tools.
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

2.  **Linting (Pylint)**
    Analyze code for errors and quality issues.
    ```bash
    pylint bridge.py --disable=C0111
    ```

3.  **Type Checking (Mypy)**
    Verify type safety.
    ```bash
    mypy bridge.py --ignore-missing-imports
    ```

4.  **Unit Testing (Pytest)**
    Run unit tests for the bridge script.
    ```bash
    pytest tests/test_bridge.py -v
    ```

5.  **Config & Data Validation**
    Validate n8n JSON syntax and check for secrets.
    ```bash
    # Validate JSON syntax for all workflows
    python -c "import json, glob; [json.load(open(f)) for f in glob.glob('workflows/*.json')]"
    ```

6.  **Integration Verification (MCP)**
    Test connection to n8n MCP server (credentials found in .env).
    ```bash
    pytest tests/test_n8n_e2e.py -v
    ```

7.  **Browser Verification (Discord E2E)**
    **Manual/Interactive Step**: Use the browser agent to verify the bot in Discord.
    
    **Instructions for Agent:**
    1.  Read `DISCORD_TEST_EMAIL`, `DISCORD_TEST_PASSWORD`, and `DISCORD_TEST_SERVER_URL` from `.env`.
    2.  Use the `browser_subagent` tool to:
        *   Navigate to `https://discord.com/login`.
        *   Log in with the test credentials.
        *   Navigate to the `DISCORD_TEST_SERVER_URL`.
        *   Send a test message (e.g., "Hello ZeroG").
        *   Wait and verify that the bot replies.
    
    *Note: This step requires the `browser_subagent` tool.*

## Checklist
- [ ] Dependencies installed?
- [ ] Pylint score 10/10?
- [ ] Mypy passed?
- [ ] Unit tests passed?
- [ ] JSON files valid?
- [ ] MCP connection verified?
- [ ] Browser test (Discord login & reply) successful?
