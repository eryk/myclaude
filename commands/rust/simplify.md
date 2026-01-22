---
allowed-tools: all
description: "精简和优化 Rust 代码，清理未使用的依赖、简化冗余代码、优化 imports"
---

# /rust:simplify - 精简和优化 Rust 代码

## Purpose

精简和优化 Rust 代码，确保修改后代码能通过 clippy 检查和测试。

## Usage

```
/rust:simplify [target-path]
```

## Arguments

- `target-path` (optional) - 目标 crate 路径或包名（如 `crates/my-crate` 或 `-p my-crate`）。如未指定，处理整个工作区。

## Execution

### 1. 确定目标范围

根据参数确定精简范围：
- 如果指定了 crate 路径/包名，只处理该 crate
- 否则处理整个工作区

### 2. 分析阶段

```bash
# 如果指定了包名 (如 -p my-crate)
cargo clippy -p <package> --all-targets -- -W clippy::all 2>&1

# 如果指定了路径，cd 到该目录后运行
cargo clippy --all-targets -- -W clippy::all 2>&1

# 整个工作区
cargo clippy --all-targets --all-features -- -W clippy::all 2>&1
```

分析 clippy 输出，找出：
- 未使用的 imports
- 可简化的代码模式
- 冗余的 clone/unwrap
- 其他 lint 警告

同时检查 Cargo.toml 中未使用的依赖。

### 3. 精简操作 (按优先级)

#### 3.1 清理未使用的依赖
- 移除 `[dependencies]` 中未使用的 crate
- 移除未使用的 feature flags

#### 3.2 优化 imports
```rust
// Before: 分散的 imports
use std::collections::HashMap;
use std::collections::HashSet;

// After: 合并 imports
use std::collections::{HashMap, HashSet};
```

排序顺序：`std` → 外部 crate → 本地模块

#### 3.3 简化代码模式

| Before | After |
|--------|-------|
| `match result { Ok(v) => v, Err(e) => return Err(e) }` | `result?` |
| `if x.is_some() { x.unwrap() }` | `if let Some(v) = x { v }` |
| `vec.iter().map(\|x\| x).collect()` | `vec.clone()` 或移除 |
| 手动循环求和 | `.iter().sum()` |
| 不必要的 `.clone()` | 直接使用引用 |
| `Option::None` | `None` |
| `Result::Ok(x)` | `Ok(x)` |

### 4. 验证 (每次修改后必须执行)

```bash
# 编译检查
cargo build -p <package> 2>&1

# Clippy 检查 (严格模式)
cargo clippy -p <package> --all-targets -- -D warnings 2>&1

# 运行测试
cargo test -p <package> 2>&1
```

**关键规则：**
- 如果 clippy 或测试失败，立即回滚修改
- 每次只修改一处，验证通过后再继续
- 对目标 crate 的 clippy 检查必须零警告

### 5. 输出报告

```markdown
## 精简报告

### 已完成的优化
- [x] 移除了 N 个未使用的依赖
- [x] 合并/清理了 N 处 imports
- [x] 简化了 N 处冗余代码

### 验证结果
- cargo build: ✓
- cargo clippy: ✓ (零警告)
- cargo test: ✓ (N passed)

### 未能优化的项目 (如有)
- 原因说明...
```

## Constraints

- 不修改公共 API 签名
- 不修改 `unsafe` 块内的代码
- 不删除 `#[allow(...)]` 属性
- 不优化被 feature flag 控制的代码
- 不添加新功能，只做精简

## Examples

```bash
# 精简整个工作区
/rust:simplify

# 精简指定 crate
/rust:simplify crates/my-crate

# 精简指定包
/rust:simplify -p my-package
```
