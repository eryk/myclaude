---
description: "Perform thorough code review focusing on completeness, quality, architecture, and security"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Conduct comprehensive code review examining feature completeness, test quality, code design/architecture, security, and **Rust-specific performance optimizations** to ensure production-ready code.

## Execution

### 1. Initial Setup

```bash
# Determine review scope
git branch --show-current
git diff main --name-only  # or master
```

**Branch-Specific Strategy:**
- Feature branch: Review only diff against base branch
- Main/master: Review `target-path` or current directory

### 2. Review Dimensions

#### A. Feature Completeness Analysis

- Scan for `TODO`, `FIXME`, `unimplemented!()`, `todo!()`
- Verify all features are fully implemented (no placeholder code)
- Validate error handling covers all edge cases

#### B. Test Quality Assessment

- Analyze test coverage for main flows
- Identify useless/redundant tests
- Verify unit tests cover edge cases
- Check integration tests for critical paths
- Ensure assertions are meaningful

#### C. Code Design & Architecture

- **SRP**: Each module has one responsibility
- **DRY**: Flag code duplication
- **Separation of Concerns**: Clear layer boundaries
- **SOLID principles** adherence
- Module organization and visibility

#### D. Security Review

- Input validation and sanitization
- Authentication & authorization
- Unsafe code justification and documentation
- Dependency vulnerabilities (`cargo audit`)
- No sensitive data in logs/errors

#### E. Rust Simplification Analysis

| Category | Look For | Fix |
|----------|----------|-----|
| **Redundant Code** | Dead code, unused imports | Remove or `#[allow(dead_code)]` with reason |
| **Over-abstraction** | Traits for single impl, excessive generics | Simplify to concrete types |
| **Verbose Patterns** | Manual loops vs iterators | `for i in 0..v.len()` → `v.iter()` |
| **Unnecessary Clones** | `.clone()` where borrow suffices | Use references |
| **Complex Conditionals** | Nested if/else | Early returns, pattern matching |
| **Boilerplate** | Manual `Debug`/`Default` | `#[derive(...)]` |

#### F. Rust Performance Analysis

| Category | Look For | Severity |
|----------|----------|----------|
| **Allocation** | Missing `Vec::with_capacity`, repeated `String` allocs | HIGH |
| **Copying** | Expensive copies in hot paths, missing `Cow` | HIGH |
| **Locking** | Lock contention, `std::sync` vs `parking_lot` | HIGH |
| **Iteration** | `collect()` then iterate, `.iter().filter().collect().len()` | MEDIUM |
| **Boxing** | Unnecessary `Box<dyn Trait>` | MEDIUM |
| **Bounds Checks** | Repeated indexing in hot loops | MEDIUM |
| **String Ops** | `format!` in loops, `+` concatenation | MEDIUM |
| **Async** | Blocking in async, unnecessary `.await` | HIGH |

#### G. Language-Specific Checks

```bash
cargo clippy --all-features -- -D warnings
cargo audit
cargo fmt --check
```

### 3. Severity Assignment

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Security vulnerabilities, data races, blocking bugs |
| **HIGH** | Significant performance impact, missing error handling |
| **MEDIUM** | Code quality, maintainability concerns |
| **LOW** | Style preferences, minor optimizations |

### 4. Review Deliverables

Generate report with:

1. **Executive Summary** - Overall quality assessment
2. **Critical Issues** - Security/blocking issues requiring immediate fix
3. **Feature Completeness** - Missing implementations
4. **Performance Findings** - Optimization opportunities with before/after examples
5. **Simplification Opportunities** - Code reduction suggestions
6. **Actionable Recommendations** - Prioritized by impact/effort

### 5. Exit Criteria

Code review passes when:

- ✅ Zero `TODO`/`FIXME`/`unimplemented!()` in production code
- ✅ All features fully implemented
- ✅ Test coverage >80% for main flows
- ✅ No critical/high security vulnerabilities
- ✅ `cargo clippy` passes without warnings
- ✅ `cargo audit` shows no vulnerabilities
- ✅ No unnecessary allocations in hot paths
- ✅ Error handling comprehensive
- ✅ No code duplication beyond threshold

## Operating Principles

### What to Focus On

- **Pragmatic**: Meaningful improvements over nitpicks
- **Context-aware**: Hot path vs setup code
- **Specific**: Every finding has clear fix
- **Rust-idiomatic**: Leverage zero-cost abstractions

### What NOT to Suggest

- Comments on self-explanatory code
- Renaming for minor style preferences
- Generics for single-type usage
- Premature optimization in cold paths
- Over-engineering simple code

## Context

$ARGUMENTS
