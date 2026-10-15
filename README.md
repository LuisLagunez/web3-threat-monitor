# web3-threat-monitor

> SOC-style threat monitor for Ethereum: ingests on-chain events, detects anomalies, and ships curated alerts to Microsoft Sentinel (KQL detections + response playbooks).

## Why this project

It treats the blockchain as if it were the "corporate network": on-chain logs
are the telemetry source (the firewall / Active Directory equivalent), a Python
worker is the log shipper, PostgreSQL is the intermediate store, and **Microsoft
Sentinel is the SIEM** where the real analyst work happens — triage, KQL
detections, incidents, and response playbooks.

It is a portfolio project that bridges **backend engineering**, **Web3**, and
**SOC / blue-team** skills.

> **Read-only by design.** The monitor never signs transactions and never holds
> private keys. Test events, when needed, are generated on a testnet (Sepolia).

## Architecture (target)

```
RPC node (Alchemy/Infura)
   │  WebSocket (real-time) + HTTP (backfill)
   ▼
Ingestion worker (Python / web3.py) ── decode logs ─▶ detection rules
   │
   ▼
PostgreSQL  ◀── source of truth (all alerts & context)
   │
   ├─▶ FastAPI  (query / management API)
   │
   └─▶ Microsoft Sentinel (curated alerts only → KQL detections → incidents)
```

Design principle: **signal, not noise.** The chain is high-volume; the worker
filters and enriches, PostgreSQL retains the detail, and only curated alerts are
forwarded to the SIEM — the same way ingestion is designed in a real SOC (cost
and noise control).

## Tech stack

- **Ingestion:** Python, `web3.py` (WebSocket subscriptions)
- **API:** FastAPI, Pydantic
- **Storage:** PostgreSQL, SQLAlchemy, Alembic
- **Packaging / infra:** Docker, docker-compose
- **SIEM:** Microsoft Sentinel (Logs Ingestion API + DCR, Entra ID auth), KQL
- **Quality / security:** ruff, mypy, bandit, pytest, pre-commit, CodeQL

## Getting started (development)

Prerequisites: **Python 3.11+** and **Git**.

```bash
python -m venv .venv
```

Activate it (Windows PowerShell): `.\.venv\Scripts\Activate.ps1`
— or Git Bash: `source .venv/Scripts/activate`.

```bash
pip install -e ".[dev]"
pre-commit install
```

Run the same checks CI runs:

```bash
ruff check .
ruff format --check .
mypy
bandit -c pyproject.toml -r src
pytest
```

## Security

- No secrets live in the repo. Copy `.env.example` to `.env` (git-ignored) and
  fill in your own values.
- Secret scanning (local `gitleaks` hook + GitHub push protection) guards against
  accidental leaks. See [SECURITY.md](SECURITY.md) to report an issue.
