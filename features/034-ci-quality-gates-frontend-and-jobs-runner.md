---
id: 034
name: CI Quality Gates (Frontend + Jobs Runner)
status: Completed
---

# 034 - CI Quality Gates (Frontend + Jobs Runner)

Add CI checks to prevent regressions and ensure the system remains buildable and runnable.

## Description

- Frontend:
  - build check
  - lint/typecheck (as applicable)
- Jobs runner:
  - unit tests for core computations
  - lint/format checks
- Ensure CI runs on pull requests.
- Ensure CI uses Linux runners to match the target deployment environment.

## Impact

- Keeps the project stable as scope grows.

## Success Criteria

- CI fails on broken builds/tests.
- CI passes on mainline.
- Checks run automatically for PRs.
- Linux runner parity is maintained (Ubuntu-based runners).
