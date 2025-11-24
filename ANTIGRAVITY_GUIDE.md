# 🪐 Google Antigravity: The Unofficial Guide

**Welcome to the Agent-First Era.**

This document compiles helpful instructions, best practices, and workflows for **Google Antigravity**, the new AI-powered IDE designed to let autonomous agents handle the heavy lifting of software development.

---

## 🚀 Getting Started

### 1. Installation
*   **Download**: Get the installer from [antigravity.google/download](https://antigravity.google/download).
*   **Setup**: Run the installer. You'll need to link your Google Account and select a model (Gemini 3 Pro is recommended).
*   **Import**: You can import settings/keybindings from VS Code or Cursor during setup.

### 2. The Interface
*   **Editor View**: Familiar VS Code-like interface.
*   **Agent Sidebar**: Your chat interface with the AI.
*   **Manager View**: "Mission Control" for orchestrating multiple agents running in parallel.

---

## 🧠 Core Concepts

### Agents & Autonomy
Antigravity isn't just a chatbot. It has **Agents** that can:
*   **Plan**: Create "To-Do" lists before coding.
*   **Execute**: Write code, create files, and run terminal commands.
*   **Browse**: Use a built-in headless browser to test web apps, take screenshots, and verify UI.

### Artifacts
Agents produce **Artifacts** to show their work:
*   `implementation_plan.md`: The roadmap for a task.
*   `task.md`: A checklist of progress.
*   `walkthrough.md`: Proof of work (screenshots, logs) after verification.

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

Antigravity uses `.agent/workflows` to define reusable processes.

### Structure
Create a `.md` file in `.agent/workflows/` (e.g., `deploy.md`).

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

## 🤖 Prompt Library (from Antigravity AI Directory)

**Project Analysis**
> "Analyze my entire project structure and create a README.md that explains the architecture, key technologies used, and how to start the development server."

**Code Explanation**
> "Open `utils.py` and explain what the `process_data` function does. Create a text Artifact summarizing its inputs, outputs, and side effects."

**Frontend Polish**
> "I want this landing page to feel more 'cyberpunk'. Update the CSS variables to use neon greens and dark purples, and add a glowing effect to all primary buttons. Verify the look using the browser."

**Debugging**
> "I'm getting this error: [paste stack trace]. Analyze the traceback, identify the file and line number responsible, and explain why it crashed."
