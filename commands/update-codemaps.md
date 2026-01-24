---
description: "Analyze codebase structure and generate/update architecture documentation for Rust, C++, Python, or mixed projects"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Generate and maintain token-lean architecture documentation ("codemaps") that provide high-level structural understanding of the codebase. Supports Rust, C++, Python, and multi-language projects.

## Execution

### 1. Language Detection

Scan the project root to determine primary language(s):

```bash
# Count source files by type
find . -type f \( -name "*.rs" -o -name "*.cpp" -o -name "*.hpp" -o -name "*.c" -o -name "*.h" -o -name "*.py" \) 2>/dev/null | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn
```

**Identify project type:**

| Indicator | Language |
|-----------|----------|
| `Cargo.toml` | Rust |
| `CMakeLists.txt`, `Makefile`, `*.vcxproj` | C++ |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| Multiple indicators | Multi-language |

### 2. Directory Structure Analysis

```bash
# Get high-level structure (max 3 levels)
find . -type d -not -path '*/\.*' -not -path '*/target/*' -not -path '*/build/*' -not -path '*/__pycache__/*' -not -path '*/node_modules/*' -not -path '*/venv/*' | head -50
```

### 3. Language-Specific Analysis

#### For Rust Projects

```bash
# Module structure from Cargo.toml
cat Cargo.toml 2>/dev/null | grep -E '^\[|^name|^path'

# Public API surface
grep -r "^pub " --include="*.rs" | head -100

# Module hierarchy
find . -name "mod.rs" -o -name "lib.rs" -o -name "main.rs" 2>/dev/null
```

**Extract:**
- Crate/workspace structure
- Public modules and their responsibilities
- Key traits and their implementations
- Error types hierarchy
- Feature flags

#### For C++ Projects

```bash
# Header structure (public API)
find . -name "*.hpp" -o -name "*.h" | grep -v "build\|third_party\|vendor"

# Namespace structure
grep -rh "^namespace" --include="*.hpp" --include="*.cpp" | sort -u

# Class definitions
grep -rh "^class\|^struct" --include="*.hpp" | head -50
```

**Extract:**
- Namespace hierarchy
- Header dependency graph (key headers only)
- Class hierarchies and relationships
- Build targets (from CMakeLists.txt)
- Library boundaries

#### For Python Projects

```bash
# Package structure
find . -name "__init__.py" -not -path '*/venv/*' -not -path '*/.venv/*'

# Public modules
find . -name "*.py" -not -name "_*" -not -path '*/test*' | head -50

# Class definitions
grep -rh "^class " --include="*.py" | sort -u
```

**Extract:**
- Package/module hierarchy
- Public classes and functions
- Entry points (from pyproject.toml/setup.py)
- Key base classes and protocols
- Dependency structure (imports)

### 4. Generate Codemaps

Create documentation in `codemaps/` directory:

| File | Content |
|------|---------|
| `architecture.md` | Overall system design, component relationships |
| `modules.md` | Module/package breakdown by responsibility |
| `data-flow.md` | Key data structures and their flow |
| `entry-points.md` | CLI, API, library entry points |

**Format Requirements:**

- **Token-lean**: Concise descriptions, no verbose prose
- **Hierarchical**: Use nested lists for structure
- **Cross-referenced**: Link related components
- **Mermaid diagrams**: For complex relationships (optional)

**Template for each codemap:**

```markdown
# [Section Name]

> Last updated: YYYY-MM-DD
> Language(s): [Rust|C++|Python|Mixed]
> Scope: [what this covers]

## Overview

[2-3 sentence summary]

## Structure

- `component/` - Brief description
  - `subcomponent.rs` - Specific purpose
  - Key types: `TypeA`, `TypeB`

## Key Abstractions

| Name | Type | Purpose |
|------|------|---------|
| `Foo` | trait/class/protocol | What it represents |

## Dependencies

[Mermaid diagram or list of inter-component deps]
```

### 5. Diff Analysis

If previous codemaps exist:

```bash
# Check for existing codemaps
ls -la codemaps/ 2>/dev/null

# Calculate diff if exists
git diff --stat codemaps/ 2>/dev/null || diff -rq codemaps/ codemaps.bak/ 2>/dev/null
```

**Threshold check:**
- If changes > 30% of content, **pause and request user approval**
- Show summary of major changes before updating

### 6. Freshness Tracking

Add to each codemap header:

```markdown
<!-- codemap-meta
generated: YYYY-MM-DD HH:MM
source_hash: [short git SHA or file hash]
tool_version: claude-code
-->
```

### 7. Validation

After generation, verify:

- [ ] All major source directories represented
- [ ] Entry points documented
- [ ] Key abstractions captured
- [ ] No implementation details (focus on structure)
- [ ] Cross-references valid

## Output Structure

```
codemaps/
├── architecture.md      # System overview
├── modules.md           # Module/package breakdown
├── data-flow.md         # Data structures & flow
└── entry-points.md      # CLI/API/library entries

.reports/
└── codemap-diff.txt     # Change summary (if updating)
```

## Language-Specific Considerations

### Rust
- Focus on: crate boundaries, trait hierarchies, error types
- Use `cargo doc --document-private-items` structure as reference
- Note feature-gated code

### C++
- Focus on: namespace organization, header interfaces, PIMPL patterns
- Document build system structure (CMake targets)
- Note ABI boundaries

### Python
- Focus on: package structure, protocol/ABC hierarchies, entry points
- Document typing information where available
- Note async boundaries

## Operating Principles

### DO
- Capture architectural decisions evident in code structure
- Document "why" of unusual patterns
- Keep entries scannable (5-10 words per line)
- Update incrementally, not wholesale

### DON'T
- Include implementation details
- Document every file (focus on structure)
- Add comments that duplicate code
- Over-document stable/mature code

## Context

$ARGUMENTS
