---
description: "Analyze and improve test coverage for Rust crates"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

分析代码测试覆盖率，识别未覆盖的代码路径，并生成测试建议以提高覆盖率。

## Scope Determination

1. **If `$ARGUMENTS` specifies crate/module**: Analyze that specific target
2. **If `$ARGUMENTS` is empty**: Analyze the entire workspace or current crate
3. **If `$ARGUMENTS` contains percentage target**: Aim for that coverage level

## Execution Steps

### Step 1: 环境检查

```bash
# 检查 cargo-tarpaulin 是否安装
cargo tarpaulin --version || cargo install cargo-tarpaulin
```

### Step 2: 运行覆盖率分析

```bash
# 基础覆盖率报告
cargo tarpaulin --package <target> --lib --timeout 120 --out Stdout

# 详细报告（包含未覆盖行号）
cargo tarpaulin --package <target> --lib --timeout 120 --out Html --output-dir ./coverage
```

### Step 3: 解析覆盖率数据

从 tarpaulin 输出中提取：
- 总体覆盖率百分比
- 每个文件的覆盖率
- 未覆盖的行号和函数

### Step 4: 代码分析

对于每个未覆盖的代码块，分析：

| 分析维度 | 检查项 |
|----------|--------|
| **可达性** | 代码是否可达？是否是死代码？ |
| **重要性** | 是公共 API？关键路径？错误处理？ |
| **复杂度** | 需要什么样的测试设置？ |
| **依赖** | 需要 mock 外部依赖吗？ |

### Step 5: 优先级排序

| 优先级 | 标准 | 示例 |
|--------|------|------|
| **P0** | 公共 API 未测试 | `pub fn process()` 无测试 |
| **P1** | 错误处理路径未覆盖 | `Err(...)` 分支未测试 |
| **P2** | 边界条件未测试 | 空输入、最大值、溢出 |
| **P3** | 私有辅助函数 | 内部实现细节 |

## Coverage Categories

### 1. 函数覆盖 (Function Coverage)

识别完全未测试的函数：

```rust
// 未覆盖示例
pub fn validate_input(input: &str) -> Result<(), Error> {
    // 整个函数未被任何测试调用
}
```

**建议**: 创建基础测试用例

### 2. 分支覆盖 (Branch Coverage)

识别未覆盖的条件分支：

```rust
fn process(value: Option<i32>) -> i32 {
    match value {
        Some(v) => v * 2,      // ✅ 已覆盖
        None => 0,              // ❌ 未覆盖
    }
}
```

**建议**: 添加 `None` 路径测试

### 3. 错误路径覆盖 (Error Path Coverage)

识别未测试的错误处理：

```rust
fn open_file(path: &Path) -> Result<File, Error> {
    if !path.exists() {
        return Err(Error::NotFound);  // ❌ 未覆盖
    }
    File::open(path).map_err(Error::Io)  // ❌ Io 错误未覆盖
}
```

**建议**: 使用临时文件/目录模拟错误场景

### 4. 边界条件覆盖 (Boundary Coverage)

| 数据类型 | 边界条件 |
|----------|----------|
| 数值 | 0, 1, -1, MAX, MIN |
| 字符串 | 空串, 单字符, 超长, Unicode |
| 集合 | 空, 单元素, 满容量 |
| Option | Some, None |
| Result | Ok, Err (各种错误类型) |

## Test Generation Templates

### 基础单元测试

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_<function>_<scenario>() {
        // Arrange
        let input = ...;

        // Act
        let result = <function>(input);

        // Assert
        assert_eq!(result, expected);
    }
}
```

### 错误路径测试

```rust
#[test]
fn test_<function>_returns_error_when_<condition>() {
    let result = <function>(invalid_input);
    assert!(matches!(result, Err(Error::<Variant>)));
}
```

### 边界条件测试

```rust
#[test]
fn test_<function>_handles_empty_input() {
    let result = <function>(&[]);
    assert_eq!(result, expected_for_empty);
}

#[test]
fn test_<function>_handles_max_value() {
    let result = <function>(i32::MAX);
    assert!(result.is_ok()); // 或验证具体行为
}
```

### 参数化测试 (使用 rstest)

```rust
use rstest::rstest;

#[rstest]
#[case(0, 0)]
#[case(1, 1)]
#[case(10, 55)]
fn test_fibonacci(#[case] input: u32, #[case] expected: u32) {
    assert_eq!(fibonacci(input), expected);
}
```

## Output Format

```markdown
# 测试覆盖率报告

**目标**: [crate/module]
**当前覆盖率**: XX%
**目标覆盖率**: XX%

## 覆盖率摘要

| 文件 | 覆盖率 | 未覆盖行 |
|------|--------|----------|
| src/lib.rs | 85% | 42-45, 78 |
| src/parser.rs | 62% | 100-120, 156-180 |

## 未覆盖代码分析

### [文件名] (当前 XX%)

#### C1: [函数/代码块] (P0/P1/P2/P3)

**位置**: `file.rs:42-50`

**未覆盖代码**:
```rust
// 显示未覆盖的代码
```

**原因分析**: [为什么未覆盖]

**建议测试**:
```rust
#[test]
fn test_xxx() {
    // 测试代码
}
```

---

## 测试实现清单

### 高优先级 (P0-P1)

1. [ ] `test_validate_returns_error_on_invalid_input` (parser.rs:42)
2. [ ] `test_process_handles_empty_slice` (processor.rs:78)

### 中优先级 (P2)

3. [ ] `test_helper_with_boundary_values` (utils.rs:100)

### 低优先级 (P3)

4. [ ] `test_internal_format_function` (internal.rs:50)

## 覆盖率提升预估

| 添加测试 | 预计覆盖率提升 |
|----------|----------------|
| P0 测试 (2个) | +8% |
| P1 测试 (3个) | +5% |
| 总计 | +13% → 达到 XX% |
```

## Analysis Principles

### DO 建议

- ✅ 优先覆盖公共 API
- ✅ 确保错误路径有测试
- ✅ 测试边界条件
- ✅ 使用有意义的断言
- ✅ 测试名称描述场景

### DON'T 建议

- ❌ 追求 100% 覆盖率（80-90% 通常足够）
- ❌ 测试 trivial getters/setters
- ❌ 测试第三方库的功能
- ❌ 为覆盖率而写无意义测试
- ❌ 测试 `#[derive]` 生成的代码

## Coverage Exclusions

以下代码可以合理排除在覆盖率目标之外：

```rust
// 1. 调试/开发代码
#[cfg(debug_assertions)]
fn debug_print() { ... }

// 2. 不可达的防御性代码
unreachable!("This should never happen");

// 3. 平台特定代码（在其他平台测试）
#[cfg(target_os = "windows")]
fn windows_only() { ... }

// 4. FFI 绑定
extern "C" fn ffi_callback() { ... }
```

## Integration with CI

建议在 CI 中添加覆盖率门槛：

```yaml
# .github/workflows/coverage.yml
- name: Run coverage
  run: |
    cargo tarpaulin --lib --out Xml
    # 检查覆盖率不低于阈值
    cargo tarpaulin --lib --fail-under 70
```

## Context

$ARGUMENTS
