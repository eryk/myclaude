---
allowed-tools: all
description: "Perform thorough code review focusing on completeness, quality, architecture, and security"
---

# /rust:review - Perform thorough code review focusing on completeness, quality, architecture, and security

## Purpose

Conduct comprehensive code review examining feature completeness, test quality, code design/architecture, and security to ensure production-ready code with no gaps or vulnerabilities.

## Usage

```
/rust:review [target-path]
```

## Arguments

- `target-path` - Path to the code to review (directory, file, or git branch). If not specified, reviews current working directory.

## Execution

**Initial Setup:**

1. Determine current git branch using `git branch --show-current`
2. Identify base branch (check for `main` or `master` existence)
3. If on feature branch, get diff scope using `git diff [base-branch] --name-only`

Use @fullstack-code-reviewer as the primary reviewer with domain-specific experts as needed:

- For Rust/backend: @rust-backend-expert
- For web frontend: @ui-engineer
- For macOS apps: @macos-app-developer
- For system architecture: @scalable-system-architect

### Review Process

**Branch-Specific Review Strategy:**

- If current branch is base branch (`main` or `master`): Review entire codebase based on `target-path`.
- If current branch is feature branch: Review only diff against base branch using `git diff main` or `git diff master`

1. **Feature Completeness Analysis**
   - Scan codebase for TODO comments, FIXME markers, and unimplemented functions
   - Verify all features are fully implemented (no placeholder/simulated code)
   - Check that all requirements from specs/epics are addressed
   - Validate error handling covers all edge cases
   - Ensure no critical functionality is missing or incomplete

2. **Test Quality Assessment**
   - Analyze test coverage for main application flows
   - Identify and flag useless/redundant tests that don't add value
   - Verify unit tests cover individual components thoroughly
   - Check integration tests cover critical user journeys
   - Ensure test assertions are meaningful and specific
   - Validate test data setup and teardown practices
   - Review mocking strategies and test isolation

3. **Code Design & Architecture Review**
   - **Single Responsibility Principle (SRP)**: Each class/module has one reason to change
   - **Don't Repeat Yourself (DRY)**: Identify and flag code duplication
   - **Open/Closed Principle**: Code open for extension, closed for modification
   - **Dependency Inversion**: Depend on abstractions, not concretions
   - **Separation of Concerns**: Clear boundaries between layers/modules
   - **SOLID principles** adherence throughout codebase
   - **Clean Code practices**: Naming, function size, complexity
   - **Design patterns** appropriate usage and implementation
   - **Code organization** and module structure
   - **Performance considerations** and optimization opportunities

4. **Security Review**
   - **Input Validation**: All user inputs properly validated and sanitized
   - **Authentication & Authorization**: Proper access controls and session management
   - **Data Protection**: Sensitive data encryption at rest and in transit
   - **SQL Injection**: Parameterized queries and ORM usage
   - **XSS Prevention**: Output encoding and CSP headers
   - **CSRF Protection**: Anti-CSRF tokens and same-origin policies
   - **Dependency Vulnerabilities**: Check for known security issues in dependencies
   - **Error Information Disclosure**: Ensure error messages don't leak sensitive info
   - **Logging Security**: No sensitive data in logs, proper log access controls
   - **Configuration Security**: Secure defaults and environment-specific configs
   - **API Security**: Rate limiting, proper HTTP methods, secure endpoints

5. **Language-Specific Checks**
   - **Rust**: Run `cargo clippy --all-features`, `cargo audit`, check for unsafe code usage
   - **JavaScript/TypeScript**: ESLint rules, TypeScript strict mode, npm audit
   - **Python**: Black formatting, pylint, bandit security linting
   - **General**: Static analysis tools appropriate for the language

6. **Documentation & Maintainability**
   - Code comments explain "why" not "what"
   - Public APIs have clear documentation
   - README and setup instructions are complete
   - Code is self-documenting with clear naming

### Review Deliverables

Generate a comprehensive review report including:

1. **Executive Summary** - High-level findings and overall code quality assessment
2. **Critical Issues** - Security vulnerabilities and blocking issues requiring immediate attention
3. **Feature Completeness Report** - Missing implementations and incomplete features
4. **Test Quality Analysis** - Coverage gaps, test improvements, and testing strategy recommendations
5. **Architecture Assessment** - Design principle violations and architectural improvements
6. **Security Findings** - Detailed security analysis with risk levels and remediation steps
7. **Code Quality Metrics** - Complexity, maintainability, and technical debt assessment
8. **Actionable Recommendations** - Prioritized list of improvements with implementation guidance

### Exit Criteria

Code review passes when:

- ✅ Zero TODO/FIXME comments in production code
- ✅ All features fully implemented with no simulation/placeholder code
- ✅ Test coverage >80% for main flows with meaningful assertions
- ✅ No critical or high-severity security vulnerabilities
- ✅ All SOLID principles followed with minimal violations
- ✅ Static analysis tools pass without warnings
- ✅ No code duplication beyond acceptable thresholds
- ✅ All dependencies up-to-date with no known vulnerabilities
- ✅ Error handling comprehensive for all edge cases
- ✅ Documentation complete and accurate
