---
description: "Sync documentation from source-of-truth config files for Rust, C++, Python, or mixed projects"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Automatically generate and synchronize project documentation from authoritative source files. Supports Rust, C++, Python, and multi-language projects.

## Execution

### 1. Language Detection

Scan project root to identify language(s):

```bash
# Check for language indicators
ls -la Cargo.toml CMakeLists.txt Makefile pyproject.toml setup.py requirements.txt package.json 2>/dev/null
```

| Indicator | Language | Source of Truth |
|-----------|----------|-----------------|
| `Cargo.toml` | Rust | Cargo.toml, lib.rs doc comments |
| `CMakeLists.txt`, `Makefile` | C++ | CMakeLists.txt, README sections |
| `pyproject.toml`, `setup.py` | Python | pyproject.toml, setup.py |
| `package.json` | Node.js | package.json, .env.example |
| Multiple | Mixed | All applicable files |

### 2. Read Source of Truth

#### Rust Projects

```bash
# Read Cargo.toml metadata
cat Cargo.toml

# Read workspace members (if workspace)
grep -A 20 '\[workspace\]' Cargo.toml 2>/dev/null

# Extract crate documentation
head -50 src/lib.rs 2>/dev/null || head -50 src/main.rs 2>/dev/null

# List available features
grep -A 20 '\[features\]' Cargo.toml 2>/dev/null

# List binaries and examples
ls src/bin/ examples/ 2>/dev/null
```

**Extract:**
- Package name, version, description, license
- Dependencies (runtime vs dev)
- Available features and their purposes
- Binary targets and examples
- Workspace structure (if applicable)

#### C++ Projects

```bash
# Read CMakeLists.txt
cat CMakeLists.txt 2>/dev/null

# Find project definition
grep -E "project\(|add_executable|add_library" CMakeLists.txt 2>/dev/null

# Check for vcpkg/conan dependencies
cat vcpkg.json conanfile.txt conanfile.py 2>/dev/null

# Find Doxygen config
cat Doxyfile 2>/dev/null | head -50
```

**Extract:**
- Project name, version
- Build targets (executables, libraries)
- Dependencies (vcpkg, conan, system)
- Compiler requirements
- Build options/flags

#### Python Projects

```bash
# Read pyproject.toml (preferred)
cat pyproject.toml 2>/dev/null

# Fallback to setup.py
cat setup.py 2>/dev/null

# Read requirements
cat requirements.txt requirements-dev.txt 2>/dev/null

# Check for entry points
grep -A 10 '\[project.scripts\]' pyproject.toml 2>/dev/null
grep -A 10 'entry_points' setup.py 2>/dev/null
```

**Extract:**
- Package name, version, description
- Dependencies (runtime vs dev)
- Entry points (CLI commands)
- Python version requirements
- Optional dependencies groups

### 3. Read Environment Configuration

```bash
# Check for environment templates
cat .env.example .env.template .env.sample 2>/dev/null

# Check for config templates
cat config.example.toml config.template.yaml settings.example.json 2>/dev/null
```

**Extract:**
- All environment variables
- Required vs optional settings
- Format and validation rules
- Default values (if any)

### 4. Generate Documentation

Create/update the following files:

#### `docs/CONTRIBUTING.md`

```markdown
# Contributing to [PROJECT_NAME]

## Prerequisites

[Language-specific requirements]

## Development Setup

[Step-by-step setup instructions]

## Available Commands

| Command | Description |
|---------|-------------|
| [extracted from config] | [description] |

## Code Style

[Language-specific style guide]

## Testing

[How to run tests]

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
```

#### `docs/RUNBOOK.md`

```markdown
# Runbook

## Build & Deploy

### Building

[Language-specific build instructions]

### Deployment

[Deployment procedures]

## Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| [from .env.example] | | | |

### Feature Flags

[From Cargo.toml features / CMake options / pyproject.toml extras]

## Troubleshooting

### Common Issues

[Placeholder for known issues]

### Logs & Debugging

[Where to find logs, how to enable debug mode]
```

#### `docs/API.md` (if library)

```markdown
# API Reference

## Overview

[Brief description]

## Installation

[Language-specific installation]

## Quick Start

[Minimal usage example]

## Modules/Crates/Packages

[Generated from source structure]
```

### 5. Language-Specific Sections

#### For Rust

**CONTRIBUTING.md additions:**
```markdown
## Rust-Specific Guidelines

### Running Tests
\`\`\`bash
cargo test --all-features
\`\`\`

### Linting
\`\`\`bash
cargo clippy --all-features -- -D warnings
\`\`\`

### Formatting
\`\`\`bash
cargo fmt --check
\`\`\`

### Documentation
\`\`\`bash
cargo doc --open
\`\`\`
```

**RUNBOOK.md additions:**
```markdown
### Cargo Features

| Feature | Description | Default |
|---------|-------------|---------|
| [from Cargo.toml] | | |

### Release Build
\`\`\`bash
cargo build --release
\`\`\`
```

#### For C++

**CONTRIBUTING.md additions:**
```markdown
## C++ Build Instructions

### Dependencies
[From vcpkg.json / conanfile]

### Building
\`\`\`bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
\`\`\`

### Running Tests
\`\`\`bash
ctest --output-on-failure
\`\`\`
```

**RUNBOOK.md additions:**
```markdown
### CMake Options

| Option | Description | Default |
|--------|-------------|---------|
| [from CMakeLists.txt] | | |

### Build Types
- Debug: Full debug symbols, no optimization
- Release: Full optimization, no debug
- RelWithDebInfo: Optimization with debug symbols
```

#### For Python

**CONTRIBUTING.md additions:**
```markdown
## Python Development

### Virtual Environment
\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
\`\`\`

### Running Tests
\`\`\`bash
pytest
\`\`\`

### Linting
\`\`\`bash
ruff check .
mypy .
\`\`\`

### Formatting
\`\`\`bash
ruff format .
\`\`\`
```

**RUNBOOK.md additions:**
```markdown
### Entry Points

| Command | Description |
|---------|-------------|
| [from pyproject.toml scripts] | |

### Optional Dependencies
\`\`\`bash
pip install ".[extra1,extra2]"
\`\`\`
```

### 6. Identify Stale Documentation

```bash
# Find docs not modified in 90+ days
find docs/ -name "*.md" -mtime +90 2>/dev/null

# Compare with source files
git log --since="90 days ago" --name-only --pretty=format: -- docs/ | sort -u
```

**Flag for review:**
- Documentation older than 90 days
- Docs referencing deleted files/functions
- Broken internal links

### 7. Show Diff Summary

```bash
# Show what changed
git diff --stat docs/

# Detailed diff
git diff docs/
```

**Present to user:**
- Files created/modified
- Sections added/removed
- Ask for confirmation before finalizing

## Output Structure

```
docs/
├── CONTRIBUTING.md    # Development guide
├── RUNBOOK.md         # Operations guide
├── API.md             # API reference (if library)
└── CHANGELOG.md       # Version history (if not exists)

.reports/
└── docs-sync.txt      # Sync report with timestamps
```

## Validation Checklist

After generation, verify:

- [ ] All commands/scripts documented
- [ ] Environment variables complete
- [ ] Build instructions tested
- [ ] Links valid (no 404s)
- [ ] Version numbers consistent
- [ ] No placeholder text remaining

## Operating Principles

### DO
- Extract from source of truth (config files)
- Keep commands copy-pasteable
- Update incrementally (preserve manual additions)
- Include troubleshooting for common issues

### DON'T
- Duplicate information from README
- Include auto-generated API docs inline
- Hardcode version numbers (reference source)
- Remove manually-added sections

## Source of Truth Priority

1. **Config files** (Cargo.toml, pyproject.toml, CMakeLists.txt)
2. **Environment templates** (.env.example)
3. **Existing documentation** (preserve manual additions)
4. **Code comments** (only for API docs)

## Context

$ARGUMENTS
