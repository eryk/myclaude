---
allowed-tools: all
description: "Run Cargo Clippy and Cargo Test, then commit if successful"
---

# /tc:rust:commit - Run Cargo Clippy and Cargo Test, then commit if successful

## Purpose

Automate Rust code quality checks and testing before committing. This command runs Cargo Clippy for linting, Cargo Test for testing, and creates a commit if both pass successfully.

## Usage

```
/tc:rust:commit [commit-message]
```

## Arguments

- `commit-message` (optional) - Custom commit message. If not provided, a default message will be generated based on the changes.

## Execution

1. **Run Cargo Clippy**: Execute `cargo clippy --all-features -- -D warnings` to check for code quality issues.
   - If clippy fails or finds warnings, find out root cause and fix it in an elegant way.

2. **Run Cargo Test**: Execute `cargo test --all-features` to run all tests.
   - If tests fail, find out root cause and fix it in an elegant way.

3. **Check for changes**: Run `git status` to verify there are uncommitted changes.
   - If no changes, notify user and exit.

4. **Stage changes**: Add all modified Rust files to git staging area.

5. **Create commit**:
   - If commit message provided, use it
   - Otherwise, generate a descriptive commit message based on the changes
   - Include in commit message: "✅ Passed clippy and tests"

6. **Display summary**: Show what was committed and confirm success.

## Examples

```bash
# Run checks and commit with auto-generated message
/tc:rust:commit

# Run checks and commit with custom message
/tc:rust:commit "feat: add new authentication module"
```
