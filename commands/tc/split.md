---
allowed-tools: all
description: "Split PRD into epics"
---

# /tc:split - Split PRD into epics

## Purpose

Split PRD into epics.

## Usage

```
/tc:split [target]
```

## Arguments

- `target` - PRD name under ./specs

## Execution

use @agent-product-spec-architect.

1. read ./specs/[target].md carefully
2. Based on its content, think hard and divide it into multiple epics, generate each of epic files with detailed thought on UI/UX for each features/user stories in the epic.
3. Put each epic file under ./specs/epics/<number starts from 0001>-<epic-name>.md.
4. Review the epic files and make sure they fully cover the PRD.
