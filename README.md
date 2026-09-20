# Awesome Antigravity [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/X3um7vxX8J)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A curated list of skills, tools and resources for **[Google Antigravity](https://antigravity.google)**, Google's agentic development platform. It comes as three programs: [Antigravity 2.0](https://antigravity.google/docs/overview/), a desktop app for running agents, the [Antigravity CLI](https://antigravity.google/docs/cli/overview/) (`agy`) for the terminal, and the [Antigravity IDE](https://antigravity.google/docs/ide/overview/), plus [extensions](https://antigravity.google/docs/ide/extensions/) for VS Code, Visual Studio, JetBrains, Zed and Xcode.

Every link below was opened and checked in September 2026 ([check log](maintenance/link-check.md)). Projects that only exist to share accounts, dodge quotas or get around regional limits are left out on purpose. If something here is dead or missing, open a pull request.

A tag such as `CLI` or `IDE` after an entry names the Antigravity program it works in, as stated by the project. No tag means the project does not say.

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
- [Known CLI problems](#known-cli-problems)
- [Guides and tips](#guides-and-tips)
- [In this repository](#in-this-repository)
- [Other lists](#other-lists)
- [Community](#community)
- [From the maintainer](#from-the-maintainer)

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

Antigravity loads skills from `.agents/skills/` in your workspace, one folder with a `SKILL.md` file per skill, so most collections written for other agents work here too. The global folder differs by program: [skill locations in the docs](https://antigravity.google/docs/skills/#skills-by-surface).

- [rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills) - A curated set put together for Antigravity first.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) - Engineering skills by Addy Osmani: reviews, testing, performance, shipping. `CLI`
- [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) - A registry where every skill is validated and security-checked before it is listed.
- [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) - Over two thousand skills with a CLI and a local MCP server to search them. `CLI` `IDE`
- [wshobson/agents](https://github.com/wshobson/agents) - Plugin marketplace that installs into Antigravity, Claude Code, Codex, Cursor and others. `CLI`
- [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) - Google Labs skills for working with the Stitch design MCP server.
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) - 165 skills for research work: biology, chemistry, medicine, scientific databases.
- [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) - Hand-written skills aimed at better agent output, with a code-review flow included. `CLI`
- [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang) - Go skills from the author of `lo`.
- [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) - 73 game development skills for Godot, Unity, Unreal, three.js and more, with a router that picks the right one.
- [Pranav-Nexus/antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - Converts skills written for Claude Code or Cursor into Antigravity plugins: swaps the tool names, reads `GEMINI.md` and `AGENTS.md`, adds the `plugin.json`.

## Single skills worth installing

- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - Design knowledge for building interfaces that do not look generated.
- [Nanako0129/sepia](https://github.com/Nanako0129/sepia) - Rewrites prose so it stops reading as machine-written. Has a native Antigravity plugin. `CLI`
- [amElnagdy/delegate-skills](https://github.com/amElnagdy/delegate-skills) - Hand a task to a second coding agent, review its diff, land the commit yourself. `CLI`
- [strip-ai-tells](https://github.com/MichaelZelbel/teach-it-once-kit/blob/main/skills/strip-ai-tells.md) - Edits prose so it stops sounding machine-written and hands back the edited text, not a report. By the maintainer of this list. A folder ready to copy into `.agents/skills/` (Antigravity, Codex) or `.claude/skills/` (Claude Code) is [in this repository](intelligence/skills/strip-ai-tells).
- [n8n vibe coding skill](intelligence/skills/n8n-vibe-coding-skill.md) - Build n8n workflows from inside the agent. Lives in this repository.

## Spec-driven development

- [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor) - Specify, plan, then implement. Works in Antigravity and Claude Code. `CLI`
- [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) - A small harness that turns an approved spec into a long autonomous run.

## Memory and context

- [CaviraOSS/LongMemory](https://github.com/CaviraOSS/LongMemory) - Local memory store your agent keeps between sessions.
- [mksglu/context-mode](https://github.com/mksglu/context-mode) - Keeps bulky tool output out of the context window and persists session memory. `CLI` `IDE`
- [ctxrs/ctx](https://github.com/ctxrs/ctx) - Search the agent sessions already on your machine. Git blame for agent history.
- [mattpocock/skills: handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) - A skill you call by name. It writes up a long session as one Markdown file so a fresh agent, another tool or a colleague can continue the work. Matt Pocock [explains when to use it](https://www.aihero.dev/skills-handoff).

## Code intelligence

- [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) - A local, pre-indexed graph of your code so the agent needs fewer tool calls. `IDE`
- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) - Turns a codebase with its docs, schemas and PDFs into a knowledge graph you can query.
- [zzet/gortex](https://github.com/zzet/gortex) - Code-intelligence engine over CLI, MCP and API for 257 languages and several repositories at once.

## Quota and usage monitors

- [jlcodes99/vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - Extension with a dashboard of your Antigravity model quotas.
- [wusimpl/AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - Extension that watches your Antigravity model quota. `IDE`
- [Dunphil692/antigravity-context-meter](https://github.com/Dunphil692/antigravity-context-meter) - Shows how full the context window is, as a macOS floating capsule or an IDE status bar item. Reads the local transcript, so it costs no tokens. `IDE`
- [Javis603/token-monitor](https://github.com/Javis603/token-monitor) - Desktop widget for tokens, cost and limits across many coding tools.
- [xiufengsun/TokenTracker](https://github.com/xiufengsun/TokenTracker) - Local usage and cost tracker that never reads your prompts.
- [vinzdg/codenotch](https://github.com/vinzdg/codenotch) - macOS app that pins your usage limits to a screen edge.
- [tddworks/ClaudeBar](https://github.com/tddworks/ClaudeBar) - macOS menu bar monitor for Claude, Codex, Antigravity and Gemini.

## Safety

- [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net) - Blocks destructive git and file commands before the agent runs them. Supports Antigravity CLI. `CLI`
- [google/mantis](https://github.com/google/mantis) - Google's toolkit for agents that find, reproduce and patch vulnerabilities.

## Running several agents

- [awslabs/cli-agent-orchestrator](https://github.com/awslabs/cli-agent-orchestrator) - Coordinates several coding CLIs in separate tmux sessions. `CLI`
- [codeaholicguy/ai-devkit](https://github.com/codeaholicguy/ai-devkit) - One control plane for the coding agents on your machine.
- [Observal/Observal](https://github.com/Observal/Observal) - Self-hosted registry to share skills, MCP servers and agents inside a team. `CLI`
- [WFD Faro](https://btcwfd.github.io/wfd-faro-site/) - Windows desktop panel for many projects at once: git health, kanban, scripts. Closed source, free tier. The live view of your Antigravity subagents is part of the paid plan.

## Fixes and quality of life

- [FutureisinPast/antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - Repairs missing and out-of-order conversation history. `IDE`
- [PeonPing/peon-ping](https://github.com/PeonPing/peon-ping) - A Warcraft peon tells you when the agent is done, so you can stop watching the terminal.

## Known CLI problems

Compiled on 2026-09-21 from the most discussed threads on Google's own [issue tracker for the CLI](https://github.com/google-antigravity/antigravity-cli/issues), which had 662 open issues that day. Nothing here was tested or reproduced by this list. Each line gives the error as reported, its status, and the thread. Google's [troubleshooting page](https://antigravity.google/docs/cli/troubleshooting/) covers four other things: the shell PATH, keyring permissions, clipboard forwarding and the self-updater.

- [#44 "Agent execution terminated due to error"](https://github.com/google-antigravity/antigravity-cli/issues/44) - Open since 2026-05-20. The reporter says it happens every time and that signing in again does not help.
- [#415 "1.0.9 update breaks authentication"](https://github.com/google-antigravity/antigravity-cli/issues/415) - After the update the CLI stops at "Eligibility check failed". Closed on 2026-09-18 as obsolete. The maintainer asks for a new issue if it still happens on 1.2.6.
- [#76 `agy --print` drops its output when not run in a terminal](https://github.com/google-antigravity/antigravity-cli/issues/76) - Hits pipes, subprocesses and redirects. Closed. A maintainer names 1.0.15 for the Windows part and 1.1.1 for silent server errors and hangs in scripts.
- [#34 "Illegal instruction" during install](https://github.com/google-antigravity/antigravity-cli/issues/34) - Closed on 2026-06-24. Users on a Raspberry Pi 4 report it fixed in 1.0.10.
- [#105 "Subagents Not Registering"](https://github.com/google-antigravity/antigravity-cli/issues/105) - Closed on 2026-07-28. No fixed version is named in the thread. Users share workarounds there.
- [#103 "User skills aren't picked up from ~/.agents/skills"](https://github.com/google-antigravity/antigravity-cli/issues/103) - Open since 2026-05-21. The docs name `~/.gemini/antigravity-cli/skills/` as the CLI's global skills folder.

## Guides and tips

- [ykdojo/antigravity-cli-tips](https://github.com/ykdojo/antigravity-cli-tips) - Practical tips for the Antigravity CLI (`agy`) by YK Sugi of CS Dojo: aliases, a custom status line, an agent-run development cycle.
- [The unofficial Antigravity guide](ANTIGRAVITY_GUIDE.md) - Setup, core concepts and working habits. Lives in this repository.

### Where do skills, rules, plugins and MCP settings go?

- [Summary: Where does Antigravity look for configurations?](https://atamel.dev/posts/2026/08-21_where_agy_configuration_summary/) - Mete Atamel's one-page map of the folders for skills, MCP servers, rules, workflows, hooks, sidecars, agents and plugins in Antigravity 2.0, the CLI and the IDE.
- [Where does Antigravity look for Agent Skills?](https://atamel.dev/posts/2026/07-01_where_agy_agent_skills/) - His experiments on which skill folders each of the three products reads, with a recommendation on where to install skills.
- [Where does Antigravity look for Rules and Workflows?](https://atamel.dev/posts/2026/07-13_where_agy_rules_workflows/) - The workspace and global folders for rules and workflows, and how far each of the three products supports them.
- [Where does Antigravity look for Plugins?](https://atamel.dev/posts/2026/08-18_where_agy_plugins/) - How a plugin packages agents, skills, MCP servers, rules and hooks, where plugins are stored, and a sample plugin to copy.
- [kwrkb/agy-plugins](https://github.com/kwrkb/agy-plugins) - MCP plugins for the Antigravity CLI: GitHub, GitLab, ast-grep, gopls and more, plus a kit for writing your own.

### How do I set up MCP servers?

- [Where does Antigravity look for MCP Servers?](https://atamel.dev/posts/2026/07-10_where_agy_mcp_servers/) - The two config file locations, and the cache that keeps a removed server showing up.
- [Configuring MCP Servers and Skills for Antigravity CLI and IDE](https://dev.to/gde/configuring-mcp-servers-and-skills-for-antigravity-cli-and-ide-2bh0) - Dazbo (Darren Lester) on sharing one MCP and skills setup between the CLI and the IDE.
- [Google Workspace MCP servers in Antigravity](https://codelabs.developers.google.com/google-workspace-mcp-antigravity) - Google codelab that connects Gmail, Drive, Docs, Sheets, Calendar and Chat to Antigravity 2.0, the IDE or the CLI. Needs a Google Cloud project in the Workspace Developer Preview Program.

### How do I write a skill?

- [Authoring Google Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) - Google codelab that explains the skill format and builds several skills, from a Git formatter to tool code scaffolding.

### Does it work under Windows and WSL?

- [Resolving WSL friction with Antigravity 2.0 and the IDE](https://dev.to/gde/resolving-wsl-friction-with-google-antigravity-the-agy-20-and-agy-ide-edition-59im) - Dazbo's fixes for two WSL problems: interactive commands that cannot be run or approved, and a broken browser agent.

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

The rules for new entries are in [contributing.md](contributing.md), and the pull request form shows them as a short checklist.
