# agent-workflow-demo

A showcase project for **GitHub Agentic Workflows** (`gh-aw`) — AI-powered CI/CD pipelines where a Copilot agent runs as a first-class GitHub Actions step: reading code, calling APIs, applying fixes, and opening PRs autonomously.

The repository ships a deliberately vulnerable Flask application and a suite of agentic workflows that scan, report, fix, and document it — fully automated.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [The Application](#the-application)
- [Workflow Inventory](#workflow-inventory)
  - [1. Docker Build \& Scan](#1-docker-build--scan)
  - [2. CVE Scanner (Agentic)](#2-cve-scanner-agentic)
  - [3. Daily Repo Status (Agentic)](#3-daily-repo-status-agentic)
  - [4. Update Docs (Agentic)](#4-update-docs-agentic)
  - [5. Copilot Setup Steps](#5-copilot-setup-steps)
- [Two-Stage CVE Pipeline — Deep Dive](#two-stage-cve-pipeline--deep-dive)
- [Security Model](#security-model)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)

---

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions                                │
│                                                                      │
│  ┌─────────────────────────┐       ┌─────────────────────────────┐   │
│  │  Docker Build & Scan    │       │  CVE Scanner (Agent)        │   │
│  │  (regular runner)       │──────▶│  (gh-aw sandbox)            │   │
│  │                         │trigger│                             │   │
│  │  • docker build         │       │  Phase 1: Download artifact │   │
│  │  • trivy image scan     │       │  Phase 2: Parse & categorize│   │
│  │  • upload artifact      │       │  Phase 3: Enrich from APIs  │   │
│  └─────────────────────────┘       │  Phase 4: Fix & verify      │   │
│                                    │  Phase 5: Report (Issue+PR) │   │
│  ┌─────────────────────────┐       └─────────────────────────────┘   │
│  │  Daily Repo Status      │                                         │
│  │  (agent — daily cron)   │──▶ Creates status issue                 │
│  └─────────────────────────┘                                         │
│                                                                      │
│  ┌─────────────────────────┐                                         │
│  │  Update Docs            │                                         │
│  │  (agent — on push)      │──▶ Creates docs PR                      │
│  └─────────────────────────┘                                         │
└───────────────────────────────────────────────────────────────────────┘
```

---

## The Application

A **Flask REST API** wrapping a path-compressed **Trie** data structure, designed for prefix-based autocomplete:

| File | Purpose |
|------|---------|
| `code-example/trie.py` | Compressed Trie implementation (insert, search, prefix lookup, delete) |
| `code-example/app.py` | Flask REST endpoints: `/insert`, `/search`, `/autocomplete`, `/delete`, `/health` |
| `Dockerfile` | Containerises the app with `python:3.12-slim` + `gunicorn` on port 8080 |
| `requirements.txt` | **8 intentionally vulnerable** packages (testing the CVE scanner) |

The vulnerable dependencies are pinned on purpose:

```
requests==2.25.0    urllib3==1.26.5     flask==2.0.1
jinja2==3.0.1       werkzeug==2.0.1     cryptography==3.4.7
certifi==2021.5.30  gunicorn==20.1.0
```

---

## Workflow Inventory

### 1. Docker Build & Scan

| | |
|---|---|
| **File** | `.github/workflows/docker-build.yml` |
| **Type** | Regular GitHub Actions (not agentic) |
| **Triggers** | Daily cron (`0 7 * * *`), push on `Dockerfile`/`requirements.txt`/`code-example/**`, manual |
| **Runner** | `ubuntu-latest` (full Docker daemon) |

**Logic:**

1. **Build** — `docker build -t app:scan .`
2. **Save** — `docker save` produces a tarball for portability
3. **Install Trivy** — pulled from the official install script
4. **Scan the real image** — `trivy image --format json` produces a JSON covering both OS-level Debian packages AND Python dependencies. A second run in table format writes to `GITHUB_STEP_SUMMARY`
5. **Statistics** — Python script parses the JSON for OS vs app counts, appends a summary table to the workflow summary
6. **Upload artifacts** — `trivy-scan-results` (JSON, 7-day retention) + `docker-image-tarball` (1-day retention)
7. **Trigger downstream** — `gh workflow run cve-scanner.lock.yml --ref main`

> **Why a separate workflow?** The agentic sandbox is rootless and has no Docker daemon. Image building and scanning must happen on a regular runner.

---

### 2. CVE Scanner (Agentic)

| | |
|---|---|
| **File** | `.github/workflows/cve-scanner.md` → compiled to `cve-scanner.lock.yml` |
| **Type** | GitHub Agentic Workflow (Copilot agent) |
| **Triggers** | `workflow_dispatch` (called by Docker Build & Scan) |
| **Timeout** | 45 minutes |
| **Tools** | `github` (default + code_security), `bash`, `web-fetch` |
| **Network** | defaults, python, linux-distros, github, containers, `api.osv.dev` |

This is the core security workflow. It operates in **5 phases**:

#### Phase 1 — Download Trivy Image Scan Results

The agent calls the GitHub REST API via `web-fetch` to:
1. Find the latest successful run of `docker-build.yml`
2. List artifacts from that run
3. Download and unzip `trivy-scan-results`

**Fallback:** if no artifact exists, runs `trivy fs` locally (Python-only, no OS coverage).

#### Phase 2 — Parse & Categorize

Parses the Trivy JSON and splits every vulnerability by **layer**:
- `Class: "os-pkgs"` → OS-level (Debian base image)
- `Class: "lang-pkgs"` → Application-level (Python pip)

Prints a structured dashboard: total count, severity breakdown (🔴 CRITICAL → 🔵 LOW), and per-layer tables sorted by severity.

#### Phase 3 — Enrich CVE Details (Live Data Only)

For every CVE, the agent queries **three live sources** — never training data:

| Source | URL | Purpose |
|--------|-----|---------|
| **OSV API** | `api.osv.dev/v1/vulns/{ID}` | CVSS score, summary, references, fix versions |
| **PyPI JSON** | `pypi.org/pypi/{pkg}/json` | Latest available version |
| **GitHub Advisory** | via `code_security` toolset | Cross-reference with Dependabot alerts |

Produces an enriched 9-column table and a **fix plan** (fixable / needs rebuild / unfixable).

#### Phase 4 — Fix & Verify (max 3 iterations)

1. **Python fixes** — bumps versions in `requirements.txt` to the minimum patched version from Trivy/OSV data
2. **OS fixes** — adds `RUN apt-get update && apt-get upgrade -y` to the Dockerfile (verified on next image rebuild)
3. **Verification** — runs `trivy fs` to confirm Python CVEs are resolved
4. **Comparison dashboard** — before/after table; loops back if CVEs remain (up to 3 times)

Rules: never change application logic, never push directly, never change the Python version.

#### Phase 5 — Final Report

Creates two GitHub outputs via **safe-outputs** (the agent never gets a write token):

| Output | Content |
|--------|---------|
| **Issue** | Full GFM report: scan summary box, architecture table, severity-sorted CVE tables, enriched details (collapsible), fix diff, timeline, next steps checklist |
| **Draft PR** | `requirements.txt` + `Dockerfile` changes, diff blocks, version bumps table, verification results |

---

### 3. Daily Repo Status (Agentic)

| | |
|---|---|
| **File** | `.github/workflows/daily-repo-status.md` → `daily-repo-status.lock.yml` |
| **Triggers** | Daily schedule, manual |
| **Tools** | `github` (lockdown: false for public repos) |
| **Network** | defaults |

**Logic:** gathers recent issues, PRs, discussions, releases, and code changes then creates a GitHub issue with productivity insights, community highlights, and recommendations. Light and informational — no code changes.

---

### 4. Update Docs (Agentic)

| | |
|---|---|
| **File** | `.github/workflows/update-docs.md` → `update-docs.lock.yml` |
| **Triggers** | Push to `main` on `code-example/**`, manual |
| **Tools** | `github` (all toolsets), `bash` |
| **Network** | defaults |
| **Timeout** | 15 minutes |

**Logic:**

1. Discovers every file in `code-example/` (`find code-example/ -type f`)
2. Reads and analyses each file (language, purpose, key functions)
3. Generates `docs/code-examples.md` with one section per file
4. Produces **Mermaid diagrams** for each algorithm/data structure (flowcharts, class diagrams, state diagrams, sequence diagrams)
5. Opens a **draft PR** with the documentation

Scope is strictly limited to `code-example/` — ignores everything else.

---

### 5. Copilot Setup Steps

| | |
|---|---|
| **File** | `.github/workflows/copilot-setup-steps.yml` |
| **Type** | Environment setup (regular Actions job named `copilot-setup-steps`) |

Checks out the repo and installs `gh-aw` CLI extension (v0.50.2). This job is automatically recognized by the Copilot Agent runtime and runs before every agentic workflow.

---

## Two-Stage CVE Pipeline — Deep Dive

```
  ┌─────────────────────┐                    ┌──────────────────────────┐
  │ docker-build.yml    │                    │ cve-scanner.lock.yml     │
  │ (ubuntu-latest)     │                    │ (agent sandbox)          │
  ├─────────────────────┤                    ├──────────────────────────┤
  │                     │                    │                          │
  │  docker build ──┐   │                    │  Phase 1                 │
  │                 │   │                    │  ├─ GET workflow runs    │
  │  trivy image ◄──┘   │                    │  ├─ GET artifacts       │
  │       │             │  artifact upload   │  └─ Download JSON       │
  │       ▼             │ ─────────────────▶ │                          │
  │  trivy-results.json │                    │  Phase 2                 │
  │       │             │  gh workflow run   │  └─ Parse OS vs Python   │
  │       ▼             │ ─────────────────▶ │                          │
  │  upload-artifact    │                    │  Phase 3                 │
  │                     │                    │  ├─ OSV API lookup       │
  │                     │                    │  ├─ PyPI latest version  │
  │                     │                    │  └─ GitHub Advisory      │
  │                     │                    │                          │
  │                     │                    │  Phase 4 (max 3×)        │
  │                     │                    │  ├─ Bump requirements    │
  │                     │                    │  ├─ Patch Dockerfile     │
  │                     │                    │  └─ trivy fs ──▶ verify  │
  │                     │                    │                          │
  │                     │                    │  Phase 5                 │
  │                     │                    │  ├─ Create Issue ✉️       │
  │                     │                    │  └─ Create Draft PR 📝   │
  └─────────────────────┘                    └──────────────────────────┘
        "Eyes"                                       "Brain"
   (scan the image)                         (analyse, fix, report)
```

**Why this split?**

| Constraint | Solution |
|-----------|----------|
| Agent sandbox is rootless — no Docker daemon | Build + scan on a regular runner |
| Regular Actions can't reason about CVEs | Agent provides analysis, enrichment, and fixes |
| Image scan catches OS + Python CVEs | `trivy image` on the real built image (not just `pip freeze`) |
| Agent needs internet for API enrichment | Network allowlist in frontmatter (OSV, PyPI, GitHub, etc.) |

---

## Security Model

GitHub Agentic Workflows enforce a strict security boundary:

### Safe Outputs

The LLM **never receives a write-scoped token**. Instead, it declares structured outputs in the frontmatter and the runtime creates them on behalf of the agent:

```yaml
safe-outputs:
  create-pull-request:
    base-branch: main
    draft: true
    labels: [security, automated, cve-fix]
  create-issue:
    title-prefix: "[CVE-scan] "
    close-older-issues: true
    labels: [security, automated]
```

### Network Firewall

Agent sandbox traffic is restricted to an explicit domain allowlist:

```yaml
network:
  allowed:
    - defaults          # GitHub API, npm, etc.
    - python            # pypi.org
    - linux-distros     # Debian security repos
    - github            # GitHub API
    - containers        # Container registries
    - api.osv.dev       # OSV vulnerability database
```

### Read-Only Permissions

All agentic workflows use `permissions: read-all`. Write operations happen exclusively through safe-outputs.

### Guardrails in Prompts

- **Live data only** — the agent is instructed to never use training-data knowledge for CVE details
- **No direct push** — all code changes go through draft PRs
- **No app logic changes** — only dependency versions and Dockerfile
- **Max 3 fix iterations** — prevents infinite loops
- **Timeout** — 45 min with a 5 min buffer

---

## How to Run

### Prerequisites

- GitHub repository with **Copilot Agent** enabled
- `gh-aw` CLI extension installed (handled by `copilot-setup-steps.yml`)

### Triggering Workflows

**From the GitHub UI:**

1. Go to **Actions** tab
2. Select the workflow in the left sidebar
3. Click **Run workflow** → select branch → **Run workflow**

**From the CLI:**

```bash
# Full CVE pipeline (build + scan + agent)
gh workflow run docker-build.yml

# CVE scanner agent only (uses last scan artifact)
gh workflow run cve-scanner.lock.yml

# Daily repo status report
gh workflow run daily-repo-status.lock.yml

# Update docs for code-example/
gh workflow run update-docs.lock.yml
```

### Compiling Agentic Workflows

After editing any `.md` workflow file:

```bash
gh aw compile
```

This produces the corresponding `.lock.yml` files that GitHub Actions actually runs. Always commit both the `.md` source and the `.lock.yml` compiled output.

---

## Project Structure

```
agent-workflow-demo/
├── .github/
│   └── workflows/
│       ├── copilot-setup-steps.yml      # Agent environment setup
│       ├── docker-build.yml             # Stage 1: build + Trivy image scan
│       ├── cve-scanner.md               # Stage 2: agentic CVE analysis (source)
│       ├── cve-scanner.lock.yml         # Stage 2: compiled workflow
│       ├── daily-repo-status.md         # Daily status report (source)
│       ├── daily-repo-status.lock.yml   # Daily status report (compiled)
│       ├── update-docs.md               # Code documentation (source)
│       └── update-docs.lock.yml         # Code documentation (compiled)
├── code-example/
│   ├── app.py                           # Flask REST API (Trie service)
│   └── trie.py                          # Compressed Trie data structure
├── Dockerfile                           # python:3.12-slim container
├── requirements.txt                     # Intentionally vulnerable deps
└── README.md
```
