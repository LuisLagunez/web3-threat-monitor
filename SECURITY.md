# Security Policy

## Scope & design

This project is **read-only** with respect to the blockchain: it subscribes to
and reads on-chain data only. It never signs transactions and never stores
wallet private keys. The only secrets it uses are read-only RPC keys, a database
connection string, and Microsoft Sentinel / Entra ID credentials — all provided
through environment variables and never committed.

## Reporting a vulnerability

If you find a security issue, please **do not open a public issue**. Instead,
open a private report via GitHub Security Advisories
("Security" tab → "Report a vulnerability"), or contact the maintainer directly.

## Secret hygiene

- `.env` is git-ignored; use `.env.example` as the template.
- A local `gitleaks` pre-commit hook and GitHub push protection guard against
  accidental secret commits.
- If a secret is ever exposed, **rotate/revoke it at the provider first**, then
  clean the git history.
