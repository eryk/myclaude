---
allowed-tools: all
description: "Review and simplify Rust code following KISS principle"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

审查并简化 Rust 代码，遵循 KISS 原则：**能简单就不要复杂，能删除就不要保留**。

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."
> — Antoine de Saint-Exupéry

## Scope Determination

1. **If `$ARGUMENTS` specifies file(s)/crate**: Target those specific paths
2. **If `$ARGUMENTS` is empty**: Analyze staged/modified files from `git diff`
3. **If `$ARGUMENTS` contains description**: Infer relevant files

## Execution

### Step 1: 分析阶段

```bash
# 确定目标范围
git diff --name-only HEAD | grep '\.rs$'

# 运行 clippy 获取警告
cargo clippy --all-targets -- -W clippy::all 2>&1
```

分析 clippy 输出，找出：
- 未使用的 imports
- 可简化的代码模式
- 冗余的 clone/unwrap
- 其他 lint 警告

同时检查 Cargo.toml 中未使用的依赖。

### Step 2: 简化操作

#### 2.1 删除死代码 (Dead Code Elimination) - P0

| 检测项 | 示例 | 操作 |
|--------|------|------|
| 未使用的 imports | `use std::collections::HashMap;` 但从未使用 | 删除 |
| 未调用的函数 | `fn helper() {}` 无调用点 | 删除或标记 `#[allow(dead_code)]` 并注释原因 |
| 注释掉的代码 | `// old_implementation()` | 删除（Git 有历史记录） |
| 无用的 else 分支 | `if cond { return; } else { ... }` | 移除 else，直接写后续代码 |
| 冗余的 return | `return value;` 在函数末尾 | 改为 `value` |

#### 2.2 清理未使用的依赖 - P0

- 移除 `[dependencies]` 中未使用的 crate
- 移除未使用的 feature flags

#### 2.3 简化控制流 (Control Flow) - P1

**合并条件:**
```rust
// Before
if condition {
    if another_condition {
        do_something();
    }
}

// After
if condition && another_condition {
    do_something();
}
```

**Early Return:**
```rust
// Before
fn process(x: Option<i32>) -> i32 {
    match x {
        Some(v) => {
            // 20 lines of logic
            result
        }
        None => 0,
    }
}

// After
fn process(x: Option<i32>) -> i32 {
    let v = match x {
        Some(v) => v,
        None => return 0,
    };
    // 20 lines of logic
    result
}
```

#### 2.4 消除过度抽象 (Over-Abstraction) - P1

| 模式 | 问题 | 简化方案 |
|------|------|----------|
| 单实现 trait | `trait Foo` 只有一个 `impl Foo for Bar` | 直接在 `Bar` 上定义方法 |
| 单类型泛型 | `fn process<T: AsRef<str>>(s: T)` 只传 `&str` | 改为 `fn process(s: &str)` |
| 过度封装 | `struct Wrapper(Inner)` 只透传方法 | 直接使用 `Inner` |
| Builder 模式滥用 | 3 个字段的 struct 用 Builder | 直接 `new()` 或 struct literal |
| 策略模式滥用 | 只有一种策略 | 删除抽象，直接实现 |

#### 2.5 优化 imports - P2

```rust
// Before: 分散的 imports
use std::collections::HashMap;
use std::collections::HashSet;

// After: 合并 imports
use std::collections::{HashMap, HashSet};
```

排序顺序：`std` → 外部 crate → 本地模块

#### 2.6 Rust 惯用简化 - P2

| 冗长写法 | 惯用写法 |
|----------|----------|
| `match result { Ok(v) => v, Err(e) => return Err(e) }` | `result?` |
| `if x.is_some() { x.unwrap() }` | `if let Some(v) = x { v }` |
| `if let Some(x) = opt { x } else { default }` | `opt.unwrap_or(default)` |
| `match opt { Some(x) => f(x), None => None }` | `opt.map(f)` |
| `vec.iter().map(\|x\| x.clone()).collect()` | `vec.clone()` |
| `for i in 0..vec.len() { vec[i] }` | `for item in &vec` |
| 手动循环求和 | `.iter().sum()` |
| 不必要的 `.clone()` | 直接使用引用 |
| `Option::None` | `None` |
| `Result::Ok(x)` | `Ok(x)` |

### Step 3: 验证 (每次修改后必须执行)

```bash
# 编译检查
cargo build 2>&1

# Clippy 检查 (严格模式)
cargo clippy --all-targets -- -D warnings 2>&1

# 运行测试
cargo test 2>&1
```

**关键规则：**
- 如果 clippy 或测试失败，**立即回滚修改**
- 每次只修改一处，验证通过后再继续
- clippy 检查必须零警告

### Step 4: 输出报告

```markdown
# 代码简化报告

**目标**: [文件列表]
**潜在减少**: [估计行数]

## 简化建议

### [文件名]

#### S1: [简化类别] (P0/P1/P2)

**位置**: `file.rs:42-50`

**当前代码**:
```rust
// 8 lines
```

**简化后**:
```rust
// 3 lines
```

**收益**: -5 行，更易读

---

## 快速执行清单

1. [x] 删除 `unused_helper()` (file.rs:100)
2. [x] 简化 `process()` 控制流 (file.rs:42)
3. [x] 合并重复的错误处理 (file.rs:200, 250)

## 验证结果

- cargo build: ✓
- cargo clippy: ✓ (零警告)
- cargo test: ✓ (N passed)

## 不建议简化的部分

| 位置 | 原因 |
|------|------|
| `complex_algo()` | 算法本身复杂，当前已是最简形式 |
```

## Priority Levels

| 优先级 | 标准 |
|--------|------|
| **P0** | 删除代码（负行数）、死代码、未使用依赖 |
| **P1** | 简化后更易读懂、控制流优化 |
| **P2** | 符合惯用法、imports 优化 |

## Constraints

### DO 简化

- ✅ 删除未使用的代码
- ✅ 用标准库替代手写逻辑
- ✅ 减少嵌套层级
- ✅ 用 early return 简化控制流
- ✅ 移除只有一个实现的 trait

### DON'T 过度简化

- ❌ 为了短而牺牲可读性
- ❌ 删除有意义的错误处理
- ❌ 合并逻辑不同的相似代码
- ❌ 用 unsafe 替代安全但稍长的代码
- ❌ 删除必要的类型标注
- ❌ 修改公共 API 签名
- ❌ 修改 `unsafe` 块内的代码
- ❌ 删除 `#[allow(...)]` 属性
- ❌ 优化被 feature flag 控制的代码
- ❌ 添加新功能，只做精简

## Context

$ARGUMENTS
