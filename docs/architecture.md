# Architecture

> Status: target design. Phase 0 only sets up the project skeleton.

## Data flow

1. **RPC node (Alchemy/Infura)** — source of Ethereum mainnet events.
   WebSocket for real-time subscriptions, HTTP for historical backfill.
2. **Ingestion worker (Python / web3.py)** — subscribes to event logs, decodes
   the raw hex data (via ABIs) into readable JSON, applies detection rules, and
   classifies anomalies.
3. **PostgreSQL** — the source of truth: stores every alert, suspicious address,
   and attack signature, including items that are *not* escalated to the SIEM.
4. **FastAPI** — management/query interface (historical alerts, blocklist,
   worker health).
5. **Microsoft Sentinel** — only *curated* alerts are forwarded via the Logs
   Ingestion API (DCR/DCE, authenticated with Entra ID). This is where the
   analyst work happens: KQL detections, incidents, and response playbooks.

## Design principle: signal, not noise

The chain is extremely high-volume. Sending everything to a SIEM would be noisy
and expensive. The worker filters and enriches, PostgreSQL retains the detail,
and only high-value alerts reach Sentinel — mirroring how ingestion is designed
in a real SOC (cost and noise control).

## Detection targets (Phase 3)

Ordered from most deterministic to most heuristic:

1. **Critical role changes** — `OwnershipTransferred`, `RoleGranted`, unexpected
   mint permissions. High-confidence signals; the first detection to build.
2. **Mixer interactions** — transfers to/from a watchlist of known mixer
   addresses (e.g. Tornado Cash). Adds a threat-intel / sanctions angle.
3. **Flash loans** — start by detecting *usage* (calls to `flashLoan` functions),
   then layer heuristics for *possible attacks*. Document false-positive rates.
