# Awesome Antigravity [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/X3um7vxX8J)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A curated list of skills, tools and resources for **[Google Antigravity](https://antigravity.google)**, Google's agent-first IDE.

Every link below was opened and checked in September 2026. Projects that only exist to share accounts, dodge quotas or get around regional limits are left out on purpose. If something here is dead or missing, open a pull request.

## Contents

- [Common questions](#common-questions)
- [Official](#official)
- [Skill collections](#skill-collections)
- [Single skills worth installing](#single-skills-worth-installing)
- [Spec-driven development](#spec-driven-development)
- [Memory and context](#memory-and-context)
- [Code intelligence](#code-intelligence)
- [Quota and usage monitors](#quota-and-usage-monitors)
- [Safety](#safety)
- [Running several agents](#running-several-agents)
- [Fixes and quality of life](#fixes-and-quality-of-life)
- [Guides and tips](#guides-and-tips)
- [In this repository](#in-this-repository)
- [Other lists](#other-lists)
- [Community](#community)
- [From the maintainer](#from-the-maintainer)
- [Contributing](#contributing)

## Common questions

Questions people asked in the Antigravity forums in September 2026, each with the place that answers it.

- **How do I keep memory between conversations?** See [Memory and context](#memory-and-context). To carry one long session into a fresh one, the handoff skill listed there writes it up as a file the next agent reads.
- **How do I see how much quota I have left?** In the CLI, type [`/usage`](https://antigravity.google/docs/cli/commands/usage/). For a view that stays on screen, see [Quota and usage monitors](#quota-and-usage-monitors).
- **How do I fork or copy a conversation?** In the CLI, [`/fork`](https://antigravity.google/docs/cli/conversations/) clones the conversation up to the current turn into a new session. It copies the thread, not your files.
- **Which rules and workflows do people use?** See [Guides and tips](#guides-and-tips).
- **How do I switch between several accounts?** Tools that swap or share accounts are left out of this list on purpose.

## Official

- [Antigravity](https://antigravity.google) - Home page and [download](https://antigravity.google/download).
- [Documentation](https://antigravity.google/docs) - Start with [Skills](https://antigravity.google/docs/skills), [Rules and Workflows](https://antigravity.google/docs/rules-workflows) and [MCP](https://antigravity.google/docs/mcp).
- [Changelog](https://antigravity.google/changelog) and [blog](https://antigravity.google/blog) - What shipped and when.
- [google-antigravity on GitHub](https://github.com/google-antigravity) - Google's own open-source projects for Antigravity.
- [antigravity-cli](https://github.com/google-antigravity/antigravity-cli) - The Antigravity agent in your terminal, without the IDE.
- [antigravity-sdk-python](https://github.com/google-antigravity/antigravity-sdk-python) - Python library for building your own agents on Antigravity.
- [Agent Skills standard](https://agentskills.io) - The open `SKILL.md` format Antigravity reads. A skill written for it also runs in Claude Code, Codex, Cursor and Gemini CLI.

## Skill collections

Antigravity loads skills from a folder of `SKILL.md` files, so most collections written for other agents work here too.

- [rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills) - A curated set put together for Antigravity first.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) - Engineering skills by Addy Osmani: reviews, testing, performance, shipping.
- [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) - A registry where every skill is validated and security-checked before it is listed.
- [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) - Over two thousand skills with a CLI and a local MCP server to search them.
- [wshobson/agents](https://github.com/wshobson/agents) - Plugin marketplace that installs into Antigravity, Claude Code, Codex, Cursor and others.
- [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) - Google Labs skills for working with the Stitch design MCP server.
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) - 165 skills for research work: biology, chemistry, medicine, scientific databases.
- [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) - Hand-written skills aimed at better agent output, with a code-review flow included.
- [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang) - Go skills from the author of `lo`.
- [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) - 73 game development skills for Godot, Unity, Unreal, three.js and more, with a router that picks the right one.
- [Pranav-Nexus/antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - Converts skills written for Claude Code or Cursor into Antigravity plugins: swaps the tool names, reads `GEMINI.md` and `AGENTS.md`, adds the `plugin.json`.

## Single skills worth installing

- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - Design knowledge for building interfaces that do not look generated.
- [Nanako0129/sepia](https://github.com/Nanako0129/sepia) - Rewrites prose so it stops reading as machine-written. Has a native Antigravity plugin.
- [amElnagdy/delegate-skills](https://github.com/amElnagdy/delegate-skills) - Hand a task to a second coding agent, review its diff, land the commit yourself.
- [n8n vibe coding skill](intelligence/skills/n8n-vibe-coding-skill.md) - Build n8n workflows from inside the agent. Lives in this repository.

## Spec-driven development

- [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor) - Specify, plan, then implement. Works in Antigravity and Claude Code.
- [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) - A small harness that turns an approved spec into a long autonomous run.

## Memory and context

- [CaviraOSS/LongMemory](https://github.com/CaviraOSS/LongMemory) - Local memory store your agent keeps between sessions.
- [mksglu/context-mode](https://github.com/mksglu/context-mode) - Keeps bulky tool output out of the context window and persists session memory.
- [ctxrs/ctx](https://github.com/ctxrs/ctx) - Search the agent sessions already on your machine. Git blame for agent history.
- [mattpocock/skills: handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) - A skill you call by name. It writes up a long session as one Markdown file so a fresh agent, another tool or a colleague can continue the work. Matt Pocock [explains when to use it](https://www.aihero.dev/skills-handoff).

## Code intelligence

- [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) - A local, pre-indexed graph of your code so the agent needs fewer tool calls.
- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) - Turns a codebase with its docs, schemas and PDFs into a knowledge graph you can query.
- [zzet/gortex](https://github.com/zzet/gortex) - Code-intelligence engine over CLI, MCP and API for 257 languages and several repositories at once.

## Quota and usage monitors

- [jlcodes99/vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - Extension with a dashboard of your Antigravity model quotas.
- [wusimpl/AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - Extension that watches your Antigravity model quota.
- [Dunphil692/antigravity-context-meter](https://github.com/Dunphil692/antigravity-context-meter) - Shows how full the context window is, as a macOS floating capsule or an IDE status bar item. Reads the local transcript, so it costs no tokens.
- [Javis603/token-monitor](https://github.com/Javis603/token-monitor) - Desktop widget for tokens, cost and limits across many coding tools.
- [xiufengsun/TokenTracker](https://github.com/xiufengsun/TokenTracker) - Local usage and cost tracker that never reads your prompts.
- [vinzdg/codenotch](https://github.com/vinzdg/codenotch) - macOS app that pins your usage limits to a screen edge.
- [tddworks/ClaudeBar](https://github.com/tddworks/ClaudeBar) - macOS menu bar monitor for Claude, Codex, Antigravity and Gemini.

## Safety

- [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net) - Blocks destructive git and file commands before the agent runs them. Supports Antigravity CLI.
- [google/mantis](https://github.com/google/mantis) - Google's toolkit for agents that find, reproduce and patch vulnerabilities.

## Running several agents

- [awslabs/cli-agent-orchestrator](https://github.com/awslabs/cli-agent-orchestrator) - Coordinates several coding CLIs in separate tmux sessions.
- [codeaholicguy/ai-devkit](https://github.com/codeaholicguy/ai-devkit) - One control plane for the coding agents on your machine.
- [Observal/Observal](https://github.com/Observal/Observal) - Self-hosted registry to share skills, MCP servers and agents inside a team.
- [WFD Faro](https://btcwfd.github.io/wfd-faro-site/) - Windows desktop panel for many projects at once: git health, kanban, scripts. Closed source, free tier. The live view of your Antigravity subagents is part of the paid plan.

## Fixes and quality of life

- [FutureisinPast/antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - Repairs missing and out-of-order conversation history.
- [PeonPing/peon-ping](https://github.com/PeonPing/peon-ping) - A Warcraft peon tells you when the agent is done, so you can stop watching the terminal.

## Guides and tips

- [ykdojo/antigravity-cli-tips](https://github.com/ykdojo/antigravity-cli-tips) - Practical tips for the Antigravity CLI (`agy`) by YK Sugi of CS Dojo: aliases, a custom status line, an agent-run development cycle.
- [The unofficial Antigravity guide](ANTIGRAVITY_GUIDE.md) - Setup, core concepts and working habits. Lives in this repository.

## In this repository

- [The unofficial Antigravity guide](ANTIGRAVITY_GUIDE.md) - Setup, core concepts and working habits.
- [Prompts](intelligence/prompts) - Mission briefs for coding agents, a bug investigation brief, a code review assistant, a test-first policy.
- [Workflows](intelligence/workflows) - Reusable Antigravity workflows, starting with validation.
- [Gravilo](bots/Gravilo) - The Discord bot that answers questions in our community, built with n8n and Supabase. Full source and deployment notes.

## Other lists

- [ZhangYu-zjut/awesome-Antigravity](https://github.com/ZhangYu-zjut/awesome-Antigravity) - A guide-style list with a focus on tuning agents and rate limits.
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - Written for Claude, but most of these skills load in Antigravity unchanged.

## Community

The [Antigravity Community Discord](https://discord.gg/X3um7vxX8J) is where we trade prompts, skills and fixes. Gravilo, the bot from this repository, answers there too.

## From the maintainer

I'm Michael Zelbel. Apart from this list I build a personal AI that runs on my own machines: it remembers what I tell it, does the small repeated jobs on its own and messages me first when something needs me. The whole thing is free and open: [teach-it-once-kit](https://github.com/MichaelZelbel/teach-it-once-kit).

I write about what I build and what broke on [Substack](https://michaelzelbel.substack.com). New skills show up there first.

## Contributing

1. Fork this repository.
2. Add your link to the section where it fits, one line, saying what it does and not how great it is.
3. Open a pull request.

Please follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).
