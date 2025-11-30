---
description: Analyze the codebase and generate a comprehensive validation workflow (validate.md)
---

# Create Validation Workflow

**Attribution:** This workflow is based on the "Ultimate Validation Command" concept by [Cole Medin](https://github.com/coleam00/context-engineering-intro).

This workflow instructs the agent to analyze **any** current codebase (Python, Node, etc.) and generate a tailored `validate.md` workflow that ensures the project is production-ready. It adapts to the tools found (e.g., n8n, Discord, Pytest, Jest).

## Steps

1.  **Analyze Context & Workflows**
    *   **Goal:** Understand what needs to be validated.
    *   **Actions:**
        *   Read `README.md`, `DEPLOYMENT.md`, and any other documentation.
        *   Analyze `requirements.txt` or `package.json`.
        *   Check for **n8n workflow files** (`*.json`).
        *   **Check Credentials:** Look for the following in `.env`:
            *   `N8N_MCP_URL` & `N8N_MCP_TOKEN` (for API/MCP testing)
            *   `DISCORD_TEST_EMAIL` & `DISCORD_TEST_PASSWORD` (for Browser testing)

2.  **Generate `.agent/workflows/validate.md`**
    *   **Goal:** Create the executable validation suite.
    *   **Instruction:** Create a new workflow file at `.agent/workflows/validate.md` that includes the following phases:
        *   **Phase 1: Setup:** Install dev dependencies.
        *   **Phase 2: Linting:** Run static analysis tools.
        *   **Phase 3: Type Checking:** Run type checkers.
        *   **Phase 4: Unit Testing:** Run unit tests.
        *   **Phase 5: Config & Data Validation:** Validate n8n JSON syntax and scan for secrets.
        *   **Phase 6: Integration/E2E Verification (MCP):**
            *   If n8n credentials exist, generate a Python script to trigger workflows.
            *   If missing, add a "⚠️ **Setup Required**" note about `N8N_MCP_URL`/`TOKEN`.
        *   **Phase 7: Browser Verification (The "Ultimate" Test):**
            *   **If Discord credentials (`DISCORD_TEST_EMAIL`, `DISCORD_TEST_PASSWORD`) are found in `.env`:**
                *   Add a step: "Use the `browser_subagent` to log into Discord using credentials from `.env`, navigate to the test server, and verify the bot's response."
            *   **If missing:**
                *   Add a "⚠️ **Browser Test Setup Required**" note.
                *   Explain: "To enable Browser E2E, add `DISCORD_TEST_EMAIL` and `DISCORD_TEST_PASSWORD` to `.env`."
    *   **Constraint:** The generated commands must be valid and executable for *this* specific codebase.

3.  **Verify the Workflow**
    *   **Goal:** Ensure the new validation tool works.
    *   **Action:** Run the newly created `validate.md` workflow.
