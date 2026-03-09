# AI Coding Tools ROI Report: Evidence Across the SDLC

**Research compiled:** March 2026
**Coverage window:** Q3 2025 – Q1 2026 (July 2025 onwards only)
**Distinct sources:** 25 studies, surveys, and reports (23 confirmed in-window + 2 borderline Q1–Q2 2025)

> **Scope note:** All sources are from late 2025 or early 2026. Pre-2025 and early-2025 studies have been deliberately excluded. Two borderline sources (GitClear January 2025, Qodo June 2025) are included and flagged.

---

## Search Progress Summary

| Round | Queries | Key Sources Found |
|-------|---------|-------------------|
| 1 | "AI coding tools ROI study Q3 Q4 2025" | METR July 2025, Faros AI July 2025, arXiv 2511.04427 |
| 2 | "McKinsey AI developer productivity 2025 2026" | McKinsey State of AI Nov 2025 |
| 3 | "Stack Overflow developer survey 2025"; "JetBrains developer ecosystem 2025" | SO 2025 (~65k devs), JetBrains 2025 (24,534 devs) |
| 4 | "DORA 2025 AI report"; "Gartner magic quadrant AI code assistants 2025" | DORA 2025 (Sep), Gartner MQ AI Code Assistants (Sep) |
| 5 | "GitHub Octoverse 2025"; "GitLab DevSecOps survey 2025" | GitHub Octoverse Oct 2025, GitLab AI Paradox Nov 2025 |
| 6 | "Cursor AI coding ROI 2025"; "LinearB benchmarks 2026" | Cursor/U.Chicago Nov 2025, LinearB 2026 Benchmarks |
| 7 | "Anthropic Claude Code productivity 2025 2026"; "DX AI impact Q4 2025" | Anthropic (3 studies), DX Q4 2025 Impact Report |
| 8 | "Stanford AI employment 2025"; "METR 2026 update"; "Sonar code quality 2026" | Stanford payroll study Aug 2025, METR Feb 2026, Sonar 2026 |

---

## 1. Master Table

| # | Study / Report | Publisher | Date | Tools Covered | SDLC Phase | Key Finding (1 sentence) | Sample Size | Neutrality | Source Link |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity | METR (non-profit) | **Jul 10, 2025** | Cursor Pro + Claude 3.5/3.7 Sonnet | Coding (real OSS issue resolution) | Experienced developers took 19% **longer** with AI enabled despite predicting a 24% speedup — stark perception-reality gap on complex real-world tasks. | 16 developers, 246 tasks, repos with 22k+ stars | NEUTRAL | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ |
| 2 | The AI Productivity Paradox Research Report | Faros AI | **Jul 23, 2025** | GitHub Copilot, Cursor (general AI) | Coding, code review, CI/CD | Individual output rises (21% more tasks, 98% more PRs) while PR review time rises 91%, PR size grows 154%, bugs/developer rise 9%, and no company-level DORA metric improves. | 10,000+ developers, 1,255 teams | VENDOR (engineering analytics tool maker) | https://www.faros.ai/blog/ai-software-engineering |
| 3 | Pragmatic Engineer 2025 Tech Stack Survey | Pragmatic Engineer / Gergely Orosz | **Jul 15, 2025** | Copilot, Cursor, ChatGPT, Claude, Gemini, Windsurf, Claude Code | General (adoption) | 85% use at least one AI tool; Copilot leads (#1, 50%) but declining YoY; Cursor (#2, 28%) and Claude surging; Claude Code at 6% in just months since launch. | 2,997 tech professionals | NEUTRAL (independent newsletter survey) | https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey |
| 4 | GitLab C-Suite AI Survey | GitLab / The Harris Poll | **Jul 29, 2025** | General AI dev tools | Full SDLC (C-suite perception) | C-suites report $28,249 saved per developer per year from AI tools, projecting $750B+ global potential; 48% report increased developer productivity; 89% expect agentic AI to be standard within 3 years. | 2,786 C-level executives, 8 global markets | VENDOR | https://about.gitlab.com/press/releases/2025-07-29-gitlab-c-suite-survey/ |
| 5 | Techreviewer AI in Software Development 2025 | Techreviewer.co | **Jul 17, 2025** | General AI coding tools | Coding, documentation, testing, code review | 97.5% of companies have adopted AI in software engineering (up from 90.9% in 2024); 82.3% report 20%+ productivity gains; 24.1% report 50%+ gains. | 50+ countries surveyed; n undisclosed | VENDOR-ADJACENT (market research firm) | https://techreviewer.co/blog/ai-in-software-development-2025-from-exploration-to-accountability-a-global-survey-analysis |
| 6 | 2025 Stack Overflow Developer Survey | Stack Overflow | **Jul 29, 2025** | ChatGPT, GitHub Copilot, and others | General (adoption, trust, satisfaction) | 84% use AI tools; trust fell to 29% accuracy confidence (from ~40% in 2024); positive sentiment down to 60%; 66% spend more time fixing "almost right" AI code; 51% use AI daily. | ~65,000 developers surveyed | NEUTRAL | https://survey.stackoverflow.co/2025/ai |
| 7 | "Canaries in the Coal Mine?" — AI and Entry-Level Developer Employment | Stanford Digital Economy Lab (Brynjolfsson, Chandar, Chen) | **Aug 26, 2025** | General AI coding tools | Full SDLC (employment/workforce) | Entry-level software developers aged 22–25 saw ~20% employment decline since late 2022; 13% relative employment decline for most AI-exposed early-career roles; developers 26+ grew 6–9% over same period. | Millions of workers via ADP payroll microdata; tens of thousands of companies | NEUTRAL (academic; ADP data partnership) | https://digitaleconomy.stanford.edu/wp-content/uploads/2025/08/Canaries_BrynjolfssonChandarChen.pdf |
| 8 | Gartner Magic Quadrant for AI Code Assistants 2025 | Gartner | **Sep 15, 2025** | GitHub Copilot, Cursor, Windsurf (Codeium), GitLab Duo, Amazon Q, Google Gemini Code Assist, and others | General market assessment | 14 vendors evaluated; by 2028, 90% of enterprise engineers will use AI code assistants (up from <14% in early 2024); market consolidating around agentic capabilities. | Analyst survey of engineering leaders (n not disclosed; report paywalled) | NEUTRAL (independent analyst) | https://www.gartner.com/en/documents/6948266 |
| 9 | DORA 2025: Accelerate State of DevOps Report | Google Cloud / DORA | **Sep 23, 2025** | General AI coding tools | Full SDLC | 90% of developers now use AI (+14% YoY); AI adoption now **positively** correlates with delivery throughput (reversal of DORA 2024 finding), but also correlates with higher change failure rates and instability; AI amplifies existing org strengths and dysfunctions equally. | ~5,000 technology professionals | NEUTRAL (Google-funded; open methodology, published questionnaire) | https://dora.dev/research/2025/dora-report/ |
| 10 | State of Developer Ecosystem 2025 | JetBrains | **Oct 2025** | ChatGPT, GitHub Copilot, Cursor, Codeium, Claude, JetBrains AI | General (adoption, productivity, time savings) | 85% of developers regularly use AI tools; 91% of JetBrains AI Assistant users save time; 37% save 1–3 hrs/week; most common concern is accuracy, not privacy. | 24,534 developers, 194 countries | VENDOR (JetBrains is an IDE maker; survey methodology independent) | https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/ |
| 11 | GitHub Octoverse 2025 | GitHub | **Oct 28, 2025** | GitHub Copilot | Coding, code review | 80% of new GitHub developers use Copilot within their first week; 43.2M PRs/month (+23% YoY); 1.1M public repos import LLM SDKs (+178% YoY); 73% of Copilot code review users report improved effectiveness. | 180M+ developers, 630M repos on GitHub | VENDOR | https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ |
| 12 | McKinsey State of AI 2025 | McKinsey & Company | **Nov 5, 2025** | General AI tools (coding + other functions) | Full SDLC (enterprise value) | 88% of organizations use AI regularly, but only 6% capture meaningful enterprise value; software engineering is among the top value-creation functions; orgs with 80–100% developer adoption report 110%+ productivity gains. | 1,993 participants, 105 countries | NEUTRAL/CONSULTING (McKinsey independent research; methodology partially disclosed) | https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai |
| 13 | GitLab Global DevSecOps Survey 2025: "The AI Paradox" | GitLab | **Nov 10, 2025** | General AI coding tools | Coding, security, compliance, code review | 97% using or planning AI in software development; 7 hrs/week lost to AI-related inefficiencies; 73% experienced issues with "vibe coding"; 70% say AI makes compliance harder; only 37% would trust AI output without human review. | 3,266 DevSecOps professionals | VENDOR | https://about.gitlab.com/press/releases/2025-11-10-gitlab-survey-reveals-the-ai-paradox/ |
| 14 | Cursor Agent Productivity Analysis | Cursor / Suproteem Sarkar, Univ. of Chicago | **Nov 11, 2025** | Cursor Agent | Coding, pull requests | Companies using Cursor agents merged 39% more PRs; revert rate did not change significantly; senior developers accept more agent output than juniors; 61% of requests are implementation tasks. | Tens of thousands of Cursor users | VENDOR-FUNDED (Cursor commissioned analysis) | https://cursor.com/blog/productivity |
| 15 | "Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity" (arXiv 2511.04427) | Independent academic (MSR 2026 peer-reviewed) | **Nov 2025** | Cursor | Coding, code complexity, maintenance | Cursor adoption produces a large but transient velocity increase alongside a persistent +30% static analysis warnings and +42% code complexity across 807 adopting repos. | 807 Cursor-adopting repos, 1,380 matched controls | NEUTRAL (peer-reviewed; no disclosed vendor conflicts) | https://arxiv.org/abs/2511.04427 |
| 16 | Estimating AI Productivity Gains from Claude Conversations | Anthropic | **Nov 25, 2025** | Claude (all tiers) | Various knowledge work tasks | Median 80% reduction in task completion time across 100,000 real conversations; average task value ~$55 in professional labor; college-level coding tasks achieve ~12x speedup; coding tasks = 19% of total productivity gain. | 100,000 Claude.ai conversations | VENDOR | https://www.anthropic.com/research/estimating-productivity-gains |
| 17 | How AI Is Transforming Work at Anthropic | Anthropic | **Dec 2, 2025** | Claude Code | Coding, planning, full SDLC | 67% increase in merged PRs/engineer/day after Claude Code adoption; self-reported productivity rose from +20% to +50% over 12 months; AI task complexity rising (3.2→3.8); human input per task down 33%. | 132 engineers surveyed, 53 interviews, 200,000 transcripts | VENDOR (Anthropic is Claude Code's maker; internal research) | https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic |
| 18 | DX AI-Assisted Engineering: Q4 2025 Impact Report | DX (developer intelligence platform) | **Q4 2025** | Copilot, Cursor, Amazon Q (general AI assistants) | Coding, onboarding, throughput | 22% of merged code is AI-authored; daily AI users save 4.1 hrs/week and merge 2.3 PRs/week vs. 1.4 for non-users; onboarding time to first 10 PRs cut from 91 to 49 days (−46%). | 135,000+ developers, 435 companies | VENDOR (engineering analytics platform; methodology disclosed) | https://getdx.com/blog/ai-assisted-engineering-q4-impact-report-2025/ |
| 19 | Anthropic Economic Index — January 2026 Report | Anthropic | **Jan 15, 2026** | Claude (all tiers, consumer + API) | Coding (dominant use case) | Coding = ~1/3 of all Claude.ai conversations and ~half of API traffic; "modifying software to correct errors" is the #1 task (10% of API); 66% task success rate for complex coding; API usage increasingly concentrated in software engineering. | 2M conversations (1M consumer, 1M API); Nov 2025 data | VENDOR | https://www.anthropic.com/research/anthropic-economic-index-january-2026-report |
| 20 | LinearB 2026 Software Engineering Benchmarks Report | LinearB | **Early 2026** | General AI coding tools | Coding, code review, pull requests | AI PRs have 10.83 issues per PR vs. 6.45 for human PRs (1.7x more); AI PR acceptance rate is 32.7% vs. 84% for human PRs; AI PRs wait 4.6x longer before review, but once reviewed, complete 2x faster. | 8.1M+ PRs, 4,800 teams, 42 countries | VENDOR (LinearB is an engineering metrics platform) | https://linearb.io/resources/software-engineering-benchmarks-report |
| 21 | "How AI Assistance Impacts the Formation of Coding Skills" (Anthropic RCT) | Anthropic | **Jan 29, 2026** | Claude (AI assistance broadly) | Coding (skill formation) | AI-assisted group scored 17% lower on comprehension tests (50% vs. 67% for hand-coding group; p=0.01, Cohen's d=0.738); speed gain was not statistically significant; debugging skills showed steepest decline; strategic AI use mitigates but doesn't eliminate deskilling. | 52 junior software engineers (RCT) | VENDOR (Anthropic funded; remarkable for self-disclosing negative finding) | https://www.anthropic.com/research/AI-assistance-coding-skills |
| 22 | Sonar "State of Code" Developer Survey 2026 | Sonar (SonarSource) | **2026 (Q1)** | General AI coding tools | Coding, code quality, security | 96% of developers don't fully trust AI output; only 48% always verify before committing; 42% of committed code is AI-authored; teams spend 24% of their work week verifying/fixing AI-generated code; 57% cite data exposure as a key concern. | Enterprise developers (n not disclosed) | VENDOR (Sonar makes code quality tools; survey methodology is independent) | https://www.sonarsource.com/state-of-code-developer-survey-report.pdf |
| 23 | METR Experiment Update: Reliability of AI Productivity Measurements | METR (non-profit) | **Feb 24, 2026** | Cursor Pro + Claude Sonnet | Coding (OSS issue resolution) | 30–50% of developers selectively skipped tasks to avoid AI-restricted conditions, creating selection bias; preliminary estimates show near-zero to small positive effect; METR believes actual 2026 AI speedup is higher than their measured 2025 data suggests. | 57 developers, 800+ tasks | NEUTRAL | https://metr.org/blog/2026-02-24-uplift-update/ |
| 24 | *(Borderline — Q2 2025)* Qodo State of AI Code Quality 2025 | Qodo | **Jun 11, 2025** | General AI coding tools | Coding, code quality | 82% use AI daily or weekly; 78% report productivity gains; 76.4% are in "red zone" (high hallucination rate, low confidence in output); 65% say AI misses critical context; senior devs most cautious. | 609 developers | VENDOR (Qodo makes AI code review tools) | https://www.qodo.ai/reports/state-of-ai-code-quality/ |
| 25 | *(Borderline — Jan 2025)* AI Copilot Code Quality 2025 Research | GitClear | **Jan 31, 2025** | GitHub Copilot and general AI-assisted code | Coding, maintenance | Code clones grew 4x since 2020 (8.3% → 12.3%); refactoring share dropped from 25% to <10%; short-term code churn: 7.9% of new code revised within 2 weeks vs. 5.5% pre-AI. | 211M changed lines of code, 2020–2024 | NEUTRAL (independent code analytics firm) | https://www.gitclear.com/ai_assistant_code_quality_2025_research |

---

## 2. KPI Summary Table by Tool

| Tool | Velocity Gain | Defect / Quality Impact | Cost Savings / ROI | Evidence Strength |
|------|--------------|------------------------|-------------------|-------------------|
| **GitHub Copilot** | 80% of new GitHub devs adopt in first week (Octoverse 2025); 73% of code-review users report improved effectiveness; DX: daily users save 4.1 hrs/week (mixed-tool data) | LinearB 2026: AI PRs have 1.7x more issues (10.83 vs. 6.45); AI PR acceptance rate 32.7% vs. 84% human (LinearB); refactoring dropped from 25% to <10% of changed lines (GitClear) | Gartner 2025: market at $3–4B; no independent enterprise-ROI study from this window | **Strong** — largest evidence base of any tool; multiple independent sources in window; positive adoption metrics coexist with quality warnings |
| **Cursor** | 39% more PRs merged post-agent adoption (vendor-funded, U. Chicago); large but transient velocity gain followed by quality decline (arXiv 2511.04427); −19% on complex real OSS tasks (METR July 2025) | +30% static analysis warnings, +42% code complexity sustained over months (arXiv 2511.04427); 32.7% AI PR acceptance rate vs. 84% human (LinearB, mixed-tool) | $20/month/seat; no independent ROI study in this window | **Moderate** — one peer-reviewed academic study (quality regression), one vendor-commissioned study (throughput gain), one contradictory independent RCT |
| **Claude Code (Anthropic)** | 67% more merged PRs/engineer/day at Anthropic (internal, Dec 2025); self-reported +50% productivity; 12x speedup on college-level coding tasks (Economic Index); 6th most adopted tool overall (Pragmatic Engineer, 6%) | Deskilling RCT: 17% lower comprehension scores for AI users (p=0.01, Jan 2026 — notable self-disclosure by Anthropic); no independent code quality study | $100/month (Max plan) + API; no third-party ROI study in this window | **Weak–Moderate** — three Anthropic internal studies with consistent positive numbers; RCT deskilling finding is a critical counterfactual |
| **Amazon Q Developer** | DX report bundles with "general AI assistants" (4.1 hrs/week savings); no tool-specific Q3/Q4 2025 study found; Gartner MQ 2025 includes as Leader | Not independently measured in this window | $19/month/seat; no independent ROI study in this window | **Weak** — no new independent study in the late-2025 window; subsumed in multi-tool reports |
| **Codeium / Windsurf** | Gartner MQ 2025 positions Cognition/Windsurf as a Leader; Pragmatic Engineer: Windsurf at 7% adoption; no tool-specific controlled study in this window | Not independently measured in this window | $15/month individual; enterprise pricing not disclosed; no independent ROI study | **Weak** — Gartner market positioning only; no outcome data in this window |
| **JetBrains AI Assistant** | 91% of JetBrains AI users report time savings; 37% save 1–3 hrs/week; 22% save 3–5 hrs/week (JetBrains own Oct 2025 survey) | Not independently measured in this window | Bundled with JetBrains IDEs or ~$10/month add-on | **Weak** — vendor survey of own users |
| **Gemini Code Assist** | Pragmatic Engineer 2025: Gemini at 8% but declining; DORA 2025 general AI findings suggest AI adoption now correlates positively with delivery throughput | Not independently measured in this window | $19/month/seat; no tool-specific study | **Weak** — no tool-specific published evidence in this window |
| **Tabnine** | Not specifically covered by any Q3 2025–Q1 2026 study | Not independently measured | $12–$39/user/month | **Weak** — no study in this window |
| **Sourcegraph Cody** | Not specifically covered by any Q3 2025–Q1 2026 study | Not independently measured | No independent ROI study | **Weak** — no study in this window |
| **Aider / Continue.dev / Tabby / Kilo Code / Roo Code** | Community adoption continues; no formal productivity study in this window; Gartner MQ 2025 does not include open-source tools in formal evaluation | Not independently measured | Free (pay API costs for Aider/Continue.dev) or self-hosted GPU costs | **Low** — no formal evidence in this window |

---

## 3. Open-Source vs. Proprietary (Late 2025 / Early 2026 Perspective)

### Total Cost of Ownership (TCO)
As of late 2025, proprietary SaaS tools cost $10–$39/user/month at individual tiers. The Gartner MQ 2025 (Sep 2025) projects the AI code assistant market at $3–4B by year-end 2025. Enterprise deployments involving multiple tools regularly exceed $2M+/year at scale. Self-hosted tools (Tabby, Continue.dev + Ollama, Aider) remain zero-licensing-fee but require GPU infrastructure at $2,000–$8,000/month per server; below ~50 developers with moderate query volume, open-source achieves cost parity.

### Feature Parity (as of Q1 2026)
The Gartner MQ 2025 evaluation confirmed that the agentic capability gap between proprietary and open-source tools narrowed significantly in the second half of 2025. Kilo Code and Roo Code (Cline forks) added competitive agentic modes. Continue.dev retains the widest model choice. However, no open-source tool received a formal Gartner evaluation — enterprise procurement teams remain hesitant without analyst validation.

### Data Privacy
The Sonar State of Code 2026 survey found 57% of developers cite data exposure as a key concern. Self-hosted tools remain the only option that guarantees code never leaves the organization's network — a decisive factor in regulated industries. GitLab's November 2025 AI Paradox survey found 70% of DevSecOps professionals say AI tools make **compliance harder**, adding urgency to on-prem deployment decisions.

### Enterprise Readiness

| Dimension | Proprietary Leaders | Open Source |
|-----------|--------------------|----|
| SLAs / uptime guarantees | Yes (GitHub, Google, AWS, Anthropic) | No |
| SSO / RBAC / audit logs | Yes | Tabby: partial; others: No |
| Compliance certifications (SOC 2, FedRAMP) | GitHub Copilot, Codeium Enterprise, Tabnine: Yes | No |
| Model customization on private code | GitHub Copilot Enterprise, Tabnine, Codeium | Yes (any FOSS model via Ollama) |
| Dedicated enterprise support | Yes | Community-only |
| On-prem / air-gapped deployment | Tabnine, Codeium, Amazon Q | Yes (primary differentiating strength) |
| Formal analyst evaluation (Gartner MQ) | Yes (14 vendors, Sep 2025) | Not included |

---

## 4. Raw Data Sources

| Dataset / Resource | Type | Window | Availability | Link |
|--------------------|------|--------|-------------|------|
| Stack Overflow Developer Survey 2025 microdata | Full anonymized CSV | Jul 2025 | Public download | https://survey.stackoverflow.co/2025/ |
| JetBrains State of Developer Ecosystem 2025 | Interactive explorer + partial CSV | Oct 2025 | Public (interactive results) | https://www.jetbrains.com/lp/devecosystem-2025/ |
| DORA 2025 Report + questionnaire | Survey data + methodology | Sep 2025 | Report public; raw microdata not released | https://dora.dev/research/2025/dora-report/ |
| GitClear AI Code Quality 2025 PDF | 211M LoC analysis (2020–2024 data) | Jan 2025 (borderline) | PDF public download | https://www.gitclear.com/ai_assistant_code_quality_2025_research |
| arXiv 2511.04427 (Cursor speed-vs-quality study) | Full academic paper; analysis reproducible | Nov 2025 | Public | https://arxiv.org/abs/2511.04427 |
| arXiv 2507.09089 (METR experienced-developer RCT) | Full academic paper | Jul 2025 | Public | https://arxiv.org/abs/2507.09089 |
| DX Q4 2025 AI Impact Report PDF | 135k-developer, 435-company telemetry | Q4 2025 | PDF public download | https://getdx.com/uploads/ai-assisted-engineering-q4-impact-report.pdf |
| Sonar State of Code 2026 PDF | Developer survey report | Q1 2026 | PDF public download | https://www.sonarsource.com/state-of-code-developer-survey-report.pdf |
| LinearB 2026 Benchmarks (8.1M PRs) | Engineering telemetry; aggregate reported | Early 2026 | Report public; raw data proprietary | https://linearb.io/resources/software-engineering-benchmarks-report |
| Anthropic deskilling RCT data | RCT (n=52); described in blog; raw not released | Jan 2026 | Research blog post only | https://www.anthropic.com/research/AI-assistance-coding-skills |
| Anthropic Economic Index microdata | 2M conversation classification; described | Jan 2026 | Research blog post only | https://www.anthropic.com/research/anthropic-economic-index-january-2026-report |
| Stanford Brynjolfsson et al. ADP payroll data | Millions of employment records | Aug 2025 | Working paper public; microdata ADP-proprietary | https://digitaleconomy.stanford.edu/wp-content/uploads/2025/08/Canaries_BrynjolfssonChandarChen.pdf |
| Pragmatic Engineer 2025 Tech Stack Survey | 2,997-respondent survey | Jul 2025 | Results in newsletter post | https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey |

---

## 5. Synthesis (300 words)

### What Late-2025 / Early-2026 Evidence Consistently Shows

By late 2025, AI coding tool adoption is essentially ubiquitous: Stack Overflow (65k devs) records 84% usage, JetBrains (24k devs) 85%, and Techreviewer reports 97.5% company adoption. The DX Q4 2025 report — the largest engineering telemetry dataset in this window (135k developers, 435 companies) — confirms that daily AI users save 4.1 hrs/week, merge 64% more PRs per week, and onboard 46% faster (91→49 days to first 10 PRs). These gains are real and replicable across independent and vendor sources alike.

### Where the Evidence Contradicts

Two contradictions sharpen in late 2025. First, **DORA 2025** (Sep 2025, n=5,000) reversed the DORA 2024 finding: AI now correlates *positively* with delivery throughput — but simultaneously correlates with *higher* change failure rates, suggesting teams ship faster but break things more. This aligns with LinearB 2026 (8.1M PRs): AI-generated PRs carry 1.7x more issues per PR than human PRs, and acceptance rates (32.7% vs. 84%) reveal reviewers still reject most AI output. Second, the **METR July 2025 RCT** (experienced developers, real OSS repos) found 19% *slower* performance with AI — then their **February 2026 update** disclosed that 30–50% selection bias contaminated the data, suggesting the actual effect may be small-positive, not negative. The truth for experienced developers on complex tasks remains genuinely unresolved.

### Key Gaps Remaining

No peer-reviewed, independently funded studies exist in this window for Amazon Q, Codeium/Windsurf, Tabnine, JetBrains AI, Gemini Code Assist, or any open-source tool. SDLC phases beyond coding (planning, architecture, deployment, incident response) remain virtually unstudied. The most consequential underexplored finding is **deskilling**: Anthropic's own January 2026 RCT found 17% lower comprehension scores for AI users — the only controlled experiment on skill formation, and it showed harm. No independent replication exists.

### Vendor vs. Independent Evidence Verdict

Vendor studies in this window universally report positive metrics (30–110%+ productivity gains). Independent sources (METR, Stanford, DORA, LinearB, GitClear, Stack Overflow) consistently surface countervailing signals: quality regression, compliance difficulty, declining trust, employment displacement for junior roles, and unresolved deskilling risk. The divergence is not noise — it reflects that vendor studies measure what AI tools do well (greenfield task speed) while independent sources measure what they do to the broader system (code debt, review burden, org-level stability).

---

## All 25 Sources Referenced (Late 2025 / Early 2026 Window)

1. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — METR experienced-dev RCT (Jul 2025)
2. https://www.faros.ai/blog/ai-software-engineering — Faros AI Productivity Paradox (Jul 2025)
3. https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey — Pragmatic Engineer tech stack survey (Jul 2025)
4. https://about.gitlab.com/press/releases/2025-07-29-gitlab-c-suite-survey/ — GitLab C-Suite AI Survey (Jul 2025)
5. https://techreviewer.co/blog/ai-in-software-development-2025-from-exploration-to-accountability-a-global-survey-analysis — Techreviewer AI in Software Dev 2025 (Jul 2025)
6. https://survey.stackoverflow.co/2025/ai — Stack Overflow 2025 Developer Survey (Jul 2025)
7. https://digitaleconomy.stanford.edu/wp-content/uploads/2025/08/Canaries_BrynjolfssonChandarChen.pdf — Stanford AI employment study (Aug 2025)
8. https://www.gartner.com/en/documents/6948266 — Gartner MQ AI Code Assistants 2025 (Sep 2025)
9. https://dora.dev/research/2025/dora-report/ — DORA 2025 Accelerate State of DevOps (Sep 2025)
10. https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/ — JetBrains State of Developer Ecosystem 2025 (Oct 2025)
11. https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ — GitHub Octoverse 2025 (Oct 2025)
12. https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai — McKinsey State of AI 2025 (Nov 2025)
13. https://about.gitlab.com/press/releases/2025-11-10-gitlab-survey-reveals-the-ai-paradox/ — GitLab AI Paradox DevSecOps Survey (Nov 2025)
14. https://cursor.com/blog/productivity — Cursor / U. Chicago Agent Productivity Analysis (Nov 2025)
15. https://arxiv.org/abs/2511.04427 — arXiv 2511.04427 Cursor speed-vs-quality study (Nov 2025)
16. https://www.anthropic.com/research/estimating-productivity-gains — Anthropic Claude productivity conversations (Nov 2025)
17. https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic — Anthropic internal Claude Code transformation study (Dec 2025)
18. https://getdx.com/blog/ai-assisted-engineering-q4-impact-report-2025/ — DX Q4 2025 AI-Assisted Engineering Impact Report (Q4 2025)
19. https://www.anthropic.com/research/anthropic-economic-index-january-2026-report — Anthropic Economic Index Jan 2026 (Jan 2026)
20. https://linearb.io/resources/software-engineering-benchmarks-report — LinearB 2026 Software Engineering Benchmarks (early 2026)
21. https://www.anthropic.com/research/AI-assistance-coding-skills — Anthropic deskilling RCT (Jan 2026)
22. https://www.sonarsource.com/state-of-code-developer-survey-report.pdf — Sonar State of Code 2026 (Q1 2026)
23. https://metr.org/blog/2026-02-24-uplift-update/ — METR experiment methodology update (Feb 2026)
24. *(Borderline Q2 2025)* https://www.qodo.ai/reports/state-of-ai-code-quality/ — Qodo State of AI Code Quality (Jun 2025)
25. *(Borderline Q1 2025)* https://www.gitclear.com/ai_assistant_code_quality_2025_research — GitClear AI Code Quality 2025 (Jan 2025)
