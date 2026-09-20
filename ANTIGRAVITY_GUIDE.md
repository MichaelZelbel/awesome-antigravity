# 🪐 Google Antigravity: The Unofficial Guide

**Welcome to the Agent-First Era.**

> Compiled from Google's official docs and the linked posts on 2026-09-21. Not run inside the desktop program. Every corrected statement links the page that proves it.

This document compiles helpful instructions, best practices, and workflows for **Google Antigravity**, Google's agentic development platform. It is no longer one IDE. The [docs](https://antigravity.google/docs/home/) describe three programs you work in: **Antigravity 2.0** (a standalone desktop app for running agents), the **Antigravity CLI** (`agy`, in your terminal) and the **Antigravity IDE**, plus extensions for VS Code, Visual Studio, JetBrains, Zed and Xcode. There is also a Python SDK.

---

## 🚀 Getting Started

### 1. Installation
*   **Antigravity 2.0 and the IDE**: Get the installer from [antigravity.google/download](https://antigravity.google/download). The [Getting Started page](https://antigravity.google/docs/getting-started/) lists the system requirements. If the installer asks whether to keep both or replace an older Antigravity, the docs say to select "Replace".
*   **Antigravity CLI**: The [install page](https://antigravity.google/docs/cli/install/) gives one command per system:
    *   macOS and Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
    *   Windows (PowerShell): `irm https://antigravity.google/cli/install.ps1 | iex`
    *   Then open a terminal in your project folder and run `agy`.
*   **Model**: You sign in with your Google Account. The docs name no recommended model. The [Models page](https://antigravity.google/docs/models/) lists what your plan offers, and you pick one in the selector under the prompt box.

### 2. The three programs
*   **Antigravity 2.0**: A desktop app that is your agents' command center. You start agents inside Projects and run several in parallel. The [overview](https://antigravity.google/docs/overview/) says it replaces the earlier Agent Manager and works without an IDE.
*   **Antigravity CLI**: The same agent capabilities as a terminal interface, suited to fast interactions and SSH sessions ([overview](https://antigravity.google/docs/cli/overview/)).
*   **Antigravity IDE**: A VS Code-like editor with an agent side panel ([overview](https://antigravity.google/docs/ide/overview/)).

---

## 🧠 Core Concepts

### Agents & Autonomy
Antigravity isn't just a chatbot. It has **Agents** that can:
*   **Plan**: Create "To-Do" lists before coding.
*   **Execute**: Write code, create files, and run terminal commands.
*   **Browse**: Open and drive a local Chrome browser to test web apps, take screenshots and record what it did ([Browser docs](https://antigravity.google/docs/ide/browser/)).

### Artifacts
Agents produce **Artifacts** to show their work. The [Artifacts docs](https://antigravity.google/docs/artifacts/) name implementation plans, code diffs, architecture diagrams, images and browser recordings. Two you will see most:
*   [Implementation Plan](https://antigravity.google/docs/implementation-plan/): The roadmap for a task, written before the agent changes anything.
*   [Walkthrough](https://antigravity.google/docs/walkthrough/): A summary of the changes once the task is done. For browser work it often holds screenshots and recordings.

---

## 💡 Best Practices (The "Antigravity Way")

### 1. Specificity Wins
Vague prompts lead to vague code. Be hyper-specific.
*   ❌ "Make the button look better."
*   ✅ "Update the primary button to use a gradient from `#00F` to `#0F0`, add a 4px border-radius, and a drop-shadow on hover."

### 2. Context is Currency
Agents need to know *where* they are working.
*   **@mention files**: Always reference specific files when asking for changes.
*   **Explain the "Why"**: Give the agent the broader goal so it can make smart architectural decisions.

### 3. Review the Plan
Always review the **Implementation Plan** before letting the agent loose. It's easier to fix a plan than to revert 50 changed files.

---

## 🛠️ Workflows

**Workflows are deprecated.** Google's docs say workflows are deprecated in favor of Agent Skills and will be retired on November 1, 2026. The [migration guide](https://antigravity.google/docs/migration/workflows-to-skills/) explains the move, and the `/migrate-workflows` command converts existing workflows for you. For anything new, write a skill (see the next section).

Until then, a workflow is a Markdown file of steps that you call with `/workflow-name`.

### Structure
Create a `.md` file in `.agents/workflows/` in your workspace (e.g., `deploy.md`). The older `.agent/` folder name is the legacy spelling: the docs say Antigravity defaults to `.agents/` and still reads `.agent/` for [rules](https://antigravity.google/docs/rules-workflows/) and [skills](https://antigravity.google/docs/skills/).

For global workflows the sources differ. The migration guide gives `~/.gemini/config/workflows/`. Mete Atamel of Google found `~/.gemini/config/global_workflows/` in [his tests of 2026-07-13](https://atamel.dev/posts/2026/07-13_where_agy_rules_workflows/), and reports that the CLI lists workflows but cannot trigger them with `/`.

```markdown
---
description: Deploy the app to Coolify
---

1. Run the build script: `npm run build`
2. Docker build: `docker build -t my-app .`
3. Push to registry...
```

### Example: "The Refactor Loop"
A common workflow for cleaning up code:
1.  **Analyze**: "Scan `src/` for unused imports and legacy patterns."
2.  **Plan**: "List all files to be modified."
3.  **Execute**: "Apply changes one file at a time."
4.  **Verify**: "Run `npm test` after every change."

---

## 🧩 Extending Antigravity

The 2025 version of this guide knew only workflows. Today the docs describe a whole set of ways to extend the agent:

*   [Skills](https://antigravity.google/docs/skills/): A folder with a `SKILL.md` file. Workspace skills live in `.agents/skills/<skill-folder>/`. The global folder is `~/.gemini/config/skills/` for Antigravity 2.0 and the IDE, and `~/.gemini/antigravity-cli/skills/` for the CLI.
*   [Rules](https://antigravity.google/docs/rules-workflows/): Markdown files with constraints the agent follows, up to 12,000 characters each. Workspace rules live in `.agents/rules/`, global rules in `~/.gemini/GEMINI.md`.
*   [MCP](https://antigravity.google/docs/mcp/): Connections to outside tools and data.
*   [Plugins](https://antigravity.google/docs/plugins/): Bundles that package skills, subagents, rules, MCP servers and hooks in one folder.
*   [Hooks](https://antigravity.google/docs/hooks/): Scripts that run at fixed points in the agent's work.
*   [Subagents](https://antigravity.google/docs/subagents/): Background agents you hand parallel work to.

---

## 🤖 Prompt Library (from Antigravity AI Directory)

**Project Analysis**
> "Analyze my entire project structure and create a README.md that explains the architecture, key technologies used, and how to start the development server."

**Code Explanation**
> "Open `utils.py` and explain what the `process_data` function does. Create a text Artifact summarizing its inputs, outputs, and side effects."

**Frontend Polish**
> "I want this landing page to feel more 'cyberpunk'. Update the CSS variables to use neon greens and dark purples, and add a glowing effect to all primary buttons. Verify the look using the browser."

**Debugging**
> "I'm getting this error: [paste stack trace]. Analyze the traceback, identify the file and line number responsible, and explain why it crashed."
