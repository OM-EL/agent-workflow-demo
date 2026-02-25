# agent-workflow-demo

A demonstration repository for [GitHub Agentic Workflows (`gh-aw`)](https://github.com/github/gh-aw) — AI-powered automation written in plain Markdown, compiled to GitHub Actions.

## What is this?

This repository showcases three ready-to-use agentic workflows built with `gh-aw`. Each workflow is a Markdown file with a YAML front-matter block that describes triggers, permissions, and tools. The `gh-aw` CLI compiles these `.md` files into standard GitHub Actions `.lock.yml` files that run in a sandboxed environment.

```
.github/workflows/
├── daily-repo-status.md        ← workflow source (edit this)
├── daily-repo-status.lock.yml  ← compiled GitHub Actions file (auto-generated)
├── issue-triage.md
├── issue-triage.lock.yml
├── update-docs.md
└── update-docs.lock.yml
```

## Included Workflows

### 🗓 Daily Repo Status

**File**: `.github/workflows/daily-repo-status.md`  
**Trigger**: Daily schedule + manual dispatch

Scans recent repository activity — issues, pull requests, discussions, releases, and code changes — then opens a labelled GitHub issue with an upbeat summary, productivity highlights, and actionable recommendations for maintainers.

---

### 🎯 Issue Triage

**File**: `.github/workflows/issue-triage.md`  
**Trigger**: Issue opened or reopened (also supports `👀` reaction)

Automatically triages new issues by:
1. Detecting spam or bot-generated content and exiting early.
2. Fetching available labels and similar open issues for context.
3. Applying the most relevant labels (up to 5).
4. Posting a structured triage comment with a summary, debugging hints, resource links, and an optional sub-task checklist.

---

### 📝 Update Docs

**File**: `.github/workflows/update-docs.md`  
**Trigger**: Push to `main` + manual dispatch

Analyzes every push to `main` to identify documentation gaps introduced by code changes. When gaps are found, it opens a **draft pull request** with updated documentation following the [Diátaxis framework](https://diataxis.fr/) and Google Developer Style Guide conventions.

---

## Getting Started

### Prerequisites

- [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated
- The `gh-aw` extension:

```bash
gh extension install github/gh-aw
```

### Use this repository as a template

Click **Use this template** on GitHub to create your own copy, or clone it directly:

```bash
git clone https://github.com/OM-EL/agent-workflow-demo.git
cd agent-workflow-demo
```

### Customize a workflow

Edit the `.md` source file, then recompile:

```bash
# Edit the workflow
$EDITOR .github/workflows/issue-triage.md

# Recompile to update the lock file
gh aw compile issue-triage

# Commit both files
git add .github/workflows/issue-triage.md .github/workflows/issue-triage.lock.yml
git commit -m "chore: update issue-triage workflow"
git push
```

### Run a workflow manually

```bash
# Trigger via GitHub CLI
gh workflow run "Daily Repo Status"

# Or open the Actions tab in the GitHub UI
```

### Debug a run

```bash
# Stream logs from the latest run
gh aw logs daily-repo-status

# Audit a specific run by ID
gh aw audit <run-id>
```

---

## VS Code Integration

The repository includes `.vscode/mcp.json` with pre-configured [MCP servers](https://modelcontextprotocol.io/) for local development:

| Server | Purpose |
|---|---|
| `microsoft/markitdown` | Convert documents to Markdown |
| `io.github.github/github-mcp-server` | GitHub API access |
| `io.github.upstash/context7` | Up-to-date library documentation |
| `microsoft/playwright-mcp` | Browser automation |
| `io.github.ChromeDevTools/chrome-devtools-mcp` | Chrome DevTools Protocol automation |
| `oraios/serena` | IDE assistant for code navigation and analysis |
| `io.github.netdata/mcp-server` | Infrastructure monitoring via Netdata Cloud |

To use these, open the repository in VS Code with the GitHub Copilot extension and supply the required API keys when prompted.

---

## Project Structure

```
agent-workflow-demo/
├── .github/
│   ├── agents/
│   │   └── agentic-workflows.agent.md   # Copilot agent for workflow authoring
│   ├── aw/
│   │   └── actions-lock.json            # Pinned action SHAs
│   └── workflows/
│       ├── copilot-setup-steps.yml      # Installs gh-aw in Copilot Agent env
│       ├── daily-repo-status.md
│       ├── daily-repo-status.lock.yml
│       ├── issue-triage.md
│       ├── issue-triage.lock.yml
│       ├── update-docs.md
│       └── update-docs.lock.yml
├── .vscode/
│   ├── mcp.json                         # MCP server configuration
│   └── settings.json
└── README.md
```

---

## Further Reading

- [gh-aw documentation](https://github.github.com/gh-aw/introduction/overview/)
- [gh-aw GitHub repository](https://github.com/github/gh-aw)
- [Diátaxis documentation framework](https://diataxis.fr/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

