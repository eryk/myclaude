---
allowed-tools: all
description: "Clean up Rust dependencies"
---

# /clean-deps - Clean up Rust dependencies

## Purpose

Clean up Rust dependencies.

## Usage

```
/clean-deps
```

## Execution

use @agent-rust-developer, read code base carefully, think hard and make sure you understand the code base. Then remove all dependencies and all features in the dependencies that are not used. Then update Cargo.toml. Make sure `cargo udeps`,  `cargo clippy` and `cargo test` pass without any warnings or errors. Finally, commit the changes.
