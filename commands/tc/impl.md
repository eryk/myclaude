---
allowed-tools: all
description: "Implement epic specifications with automated review and testing"
---

# /tc:impl - Implement epic specifications with automated review and testing

## Purpose

Implement epic specifications with automated review and testing.

## Usage

```
/tc:impl [epic-number]
```

## Arguments

- `epic-number` - epic number.

## Execution

Based on the epic file, find out what agents are needed to implement the epic. If backend / rust, use @rust-backend-expert. If web frontend, use @ui-engineer. If macos app, use @macos-app-developer. Otherwise, use @general-purpose agent.

Code reviewer shall use @fullstack-code-reviewer.

1. find the right epic file under ./specs or ./specs/epics. Read it carefully.
2. Think hard to form a plan for the implementation.
3. Implement based on the plan using the right coding agents. Write sufficient unit/integration tests accordingly.
4. Review the code with @fullstack-code-reviewer. If the code is not working as expected, fix the code and repeat the process.
5. Once the code is working as expected (e.g. for rust, `cargo clippy --all-features` and `cargo test --all-features` pass without any warnings/issues), commit the code to the repo.
6. Update the epic file to reflect the changes.
