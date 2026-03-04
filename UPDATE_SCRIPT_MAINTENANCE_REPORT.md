## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: legacy publish action setup and missing explicit content-write permission.
- Fixes made: replaced publish action with native commit-if-changed step, added manual trigger, upgraded checkout/setup actions, and set `permissions: contents: write`.
- Validation: checked workflow command chain (`make data`) and guarded push step.
- Known blockers: none identified in this remediation pass.
