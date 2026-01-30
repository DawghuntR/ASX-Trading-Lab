---
id: 033
name: Local Developer Workflow & Environment
status: Completed
---

# 033 - Local Developer Workflow & Environment

Document and standardize how to run the frontend and jobs runner locally for development and debugging.

## Description

Primary documented platform: **Ubuntu 24.04.3 LTS**.

- Provide local setup instructions:
  - prerequisites (node, python, docker optional)
  - environment variable setup
  - how to run frontend locally
  - how to run daily jobs manually
- Provide sample `.env.example` files (no secrets).

## Impact

- Reduces friction and prevents setup divergence.

## Success Criteria

- A new developer can follow the docs to run the UI locally against Supabase Cloud.
- A new developer can run the jobs runner in a dry-run or limited-symbol mode.
- All commands and paths in docs are validated against Ubuntu (Linux-first).

## Implementation Notes

- Frontend setup and scripts: `frontend/README.md`
- Jobs runner setup and CLI usage: `jobs/README.md`
- Deployment on Ubuntu (systemd timer): `deploy/README.md`
