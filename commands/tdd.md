---
description: "Enforce test-driven development workflow for Rust, C++, Python projects. Write failing tests FIRST, then implement minimal code to pass. Ensure 80%+ coverage."
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Enforce strict TDD (Test-Driven Development) methodology across Rust, C++, and Python projects. The cycle is non-negotiable: **RED → GREEN → REFACTOR**.

## TDD Cycle

```
RED → GREEN → REFACTOR → REPEAT

RED:      Write a failing test (test MUST fail)
GREEN:    Write MINIMAL code to pass (no more, no less)
REFACTOR: Improve code while keeping tests green
REPEAT:   Next feature/scenario
```

**MANDATORY**: Tests must be written BEFORE implementation. Never skip the RED phase.

## Execution

### 1. Language Detection

```bash
# Detect project type
ls Cargo.toml CMakeLists.txt pyproject.toml setup.py pytest.ini 2>/dev/null
```

| Indicator | Language | Test Framework |
|-----------|----------|----------------|
| `Cargo.toml` | Rust | `cargo test`, proptest |
| `CMakeLists.txt` | C++ | Google Test, Catch2, CTest |
| `pyproject.toml`, `pytest.ini` | Python | pytest, unittest |

### 2. Scaffold Interface (SCAFFOLD)

Define types and signatures FIRST, without implementation.

#### Rust

```rust
// src/liquidity.rs

/// Market data for liquidity calculation
#[derive(Debug, Clone)]
pub struct MarketData {
    pub total_volume: f64,
    pub bid_ask_spread: f64,
    pub active_traders: u32,
    pub last_trade_time: chrono::DateTime<chrono::Utc>,
}

/// Calculate liquidity score (0-100)
pub fn calculate_liquidity_score(market: &MarketData) -> f64 {
    todo!("Implementation pending - TDD RED phase")
}
```

#### C++

```cpp
// include/liquidity.hpp
#pragma once

#include <chrono>

namespace trading {

struct MarketData {
    double total_volume;
    double bid_ask_spread;
    uint32_t active_traders;
    std::chrono::system_clock::time_point last_trade_time;
};

/// Calculate liquidity score (0-100)
[[nodiscard]] double calculate_liquidity_score(const MarketData& market);

}  // namespace trading
```

```cpp
// src/liquidity.cpp
#include "liquidity.hpp"
#include <stdexcept>

namespace trading {

double calculate_liquidity_score(const MarketData& market) {
    throw std::runtime_error("Not implemented - TDD RED phase");
}

}  // namespace trading
```

#### Python

```python
# src/liquidity.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MarketData:
    total_volume: float
    bid_ask_spread: float
    active_traders: int
    last_trade_time: datetime

def calculate_liquidity_score(market: MarketData) -> float:
    """Calculate liquidity score (0-100)."""
    raise NotImplementedError("Implementation pending - TDD RED phase")
```

### 3. Write Failing Tests (RED)

Write comprehensive tests BEFORE implementation.

#### Rust Tests

```rust
// src/liquidity.rs (or tests/liquidity_test.rs)

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::Utc;

    #[test]
    fn test_high_liquidity_market() {
        let market = MarketData {
            total_volume: 100_000.0,
            bid_ask_spread: 0.01,
            active_traders: 500,
            last_trade_time: Utc::now(),
        };

        let score = calculate_liquidity_score(&market);

        assert!(score > 80.0, "Expected high score, got {}", score);
        assert!(score <= 100.0, "Score should not exceed 100");
    }

    #[test]
    fn test_low_liquidity_market() {
        let market = MarketData {
            total_volume: 100.0,
            bid_ask_spread: 0.5,
            active_traders: 2,
            last_trade_time: Utc::now() - chrono::Duration::days(1),
        };

        let score = calculate_liquidity_score(&market);

        assert!(score < 30.0, "Expected low score, got {}", score);
        assert!(score >= 0.0, "Score should not be negative");
    }

    #[test]
    fn test_zero_volume_returns_zero() {
        let market = MarketData {
            total_volume: 0.0,
            bid_ask_spread: 0.0,
            active_traders: 0,
            last_trade_time: Utc::now(),
        };

        let score = calculate_liquidity_score(&market);

        assert_eq!(score, 0.0, "Zero volume should return zero score");
    }
}
```

**Property-based tests (proptest):**

```rust
#[cfg(test)]
mod proptests {
    use super::*;
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn score_always_in_valid_range(
            volume in 0.0..1_000_000.0f64,
            spread in 0.0..1.0f64,
            traders in 0u32..10_000,
        ) {
            let market = MarketData {
                total_volume: volume,
                bid_ask_spread: spread,
                active_traders: traders,
                last_trade_time: Utc::now(),
            };

            let score = calculate_liquidity_score(&market);

            prop_assert!(score >= 0.0 && score <= 100.0,
                "Score {} out of range for {:?}", score, market);
        }
    }
}
```

#### C++ Tests (Google Test)

```cpp
// tests/liquidity_test.cpp
#include <gtest/gtest.h>
#include "liquidity.hpp"

using namespace trading;
using namespace std::chrono;

class LiquidityTest : public ::testing::Test {
protected:
    system_clock::time_point now = system_clock::now();
};

TEST_F(LiquidityTest, HighLiquidityMarket) {
    MarketData market{
        .total_volume = 100000.0,
        .bid_ask_spread = 0.01,
        .active_traders = 500,
        .last_trade_time = now
    };

    double score = calculate_liquidity_score(market);

    EXPECT_GT(score, 80.0) << "Expected high score";
    EXPECT_LE(score, 100.0) << "Score should not exceed 100";
}

TEST_F(LiquidityTest, LowLiquidityMarket) {
    MarketData market{
        .total_volume = 100.0,
        .bid_ask_spread = 0.5,
        .active_traders = 2,
        .last_trade_time = now - hours(24)
    };

    double score = calculate_liquidity_score(market);

    EXPECT_LT(score, 30.0) << "Expected low score";
    EXPECT_GE(score, 0.0) << "Score should not be negative";
}

TEST_F(LiquidityTest, ZeroVolumeReturnsZero) {
    MarketData market{
        .total_volume = 0.0,
        .bid_ask_spread = 0.0,
        .active_traders = 0,
        .last_trade_time = now
    };

    double score = calculate_liquidity_score(market);

    EXPECT_DOUBLE_EQ(score, 0.0) << "Zero volume should return zero";
}
```

#### Python Tests (pytest)

```python
# tests/test_liquidity.py
import pytest
from datetime import datetime, timedelta
from src.liquidity import MarketData, calculate_liquidity_score

class TestLiquidityScore:
    def test_high_liquidity_market(self):
        market = MarketData(
            total_volume=100_000,
            bid_ask_spread=0.01,
            active_traders=500,
            last_trade_time=datetime.now()
        )

        score = calculate_liquidity_score(market)

        assert score > 80, f"Expected high score, got {score}"
        assert score <= 100, "Score should not exceed 100"

    def test_low_liquidity_market(self):
        market = MarketData(
            total_volume=100,
            bid_ask_spread=0.5,
            active_traders=2,
            last_trade_time=datetime.now() - timedelta(days=1)
        )

        score = calculate_liquidity_score(market)

        assert score < 30, f"Expected low score, got {score}"
        assert score >= 0, "Score should not be negative"

    def test_zero_volume_returns_zero(self):
        market = MarketData(
            total_volume=0,
            bid_ask_spread=0,
            active_traders=0,
            last_trade_time=datetime.now()
        )

        score = calculate_liquidity_score(market)

        assert score == 0, "Zero volume should return zero score"


# Property-based tests with hypothesis
from hypothesis import given, strategies as st

@given(
    volume=st.floats(min_value=0, max_value=1_000_000),
    spread=st.floats(min_value=0, max_value=1),
    traders=st.integers(min_value=0, max_value=10_000)
)
def test_score_always_in_valid_range(volume, spread, traders):
    market = MarketData(
        total_volume=volume,
        bid_ask_spread=spread,
        active_traders=traders,
        last_trade_time=datetime.now()
    )

    score = calculate_liquidity_score(market)

    assert 0 <= score <= 100, f"Score {score} out of range"
```

### 4. Run Tests - Verify FAIL (RED)

```bash
# Rust
cargo test --lib

# C++
cd build && ctest --output-on-failure

# Python
pytest tests/ -v
```

**Expected output:** All tests FAIL with "not implemented" errors.

✅ Verify tests fail for the RIGHT reason (not implemented, not syntax errors).

### 5. Implement Minimal Code (GREEN)

Write the MINIMUM code to make tests pass. No optimization, no extra features.

#### Rust Implementation

```rust
pub fn calculate_liquidity_score(market: &MarketData) -> f64 {
    if market.total_volume == 0.0 {
        return 0.0;
    }

    let volume_score = (market.total_volume / 1000.0).min(100.0);
    let spread_score = (100.0 - market.bid_ask_spread * 1000.0).max(0.0);
    let trader_score = (market.active_traders as f64 / 10.0).min(100.0);

    let hours_since_trade = (Utc::now() - market.last_trade_time)
        .num_hours() as f64;
    let recency_score = (100.0 - hours_since_trade * 10.0).max(0.0);

    let score = volume_score * 0.4
        + spread_score * 0.3
        + trader_score * 0.2
        + recency_score * 0.1;

    score.clamp(0.0, 100.0)
}
```

#### C++ Implementation

```cpp
double calculate_liquidity_score(const MarketData& market) {
    if (market.total_volume == 0.0) {
        return 0.0;
    }

    double volume_score = std::min(market.total_volume / 1000.0, 100.0);
    double spread_score = std::max(100.0 - market.bid_ask_spread * 1000.0, 0.0);
    double trader_score = std::min(static_cast<double>(market.active_traders) / 10.0, 100.0);

    auto now = std::chrono::system_clock::now();
    auto hours_since_trade = std::chrono::duration_cast<std::chrono::hours>(
        now - market.last_trade_time).count();
    double recency_score = std::max(100.0 - hours_since_trade * 10.0, 0.0);

    double score = volume_score * 0.4
        + spread_score * 0.3
        + trader_score * 0.2
        + recency_score * 0.1;

    return std::clamp(score, 0.0, 100.0);
}
```

#### Python Implementation

```python
def calculate_liquidity_score(market: MarketData) -> float:
    if market.total_volume == 0:
        return 0.0

    volume_score = min(market.total_volume / 1000, 100)
    spread_score = max(100 - market.bid_ask_spread * 1000, 0)
    trader_score = min(market.active_traders / 10, 100)

    hours_since_trade = (datetime.now() - market.last_trade_time).total_seconds() / 3600
    recency_score = max(100 - hours_since_trade * 10, 0)

    score = (
        volume_score * 0.4
        + spread_score * 0.3
        + trader_score * 0.2
        + recency_score * 0.1
    )

    return max(0, min(score, 100))
```

### 6. Run Tests - Verify PASS (GREEN)

```bash
# Rust
cargo test --lib
# Expected: All tests pass

# C++
cd build && ctest --output-on-failure
# Expected: All tests pass

# Python
pytest tests/ -v
# Expected: All tests pass
```

✅ All tests passing. Ready to refactor.

### 7. Refactor (IMPROVE)

Improve code quality while keeping tests green.

**Refactoring goals:**
- Extract constants and magic numbers
- Improve naming
- Add documentation
- Optimize if needed (after profiling)

```bash
# After each refactor change, run tests:

# Rust
cargo test && cargo clippy

# C++
cmake --build build && ctest

# Python
pytest && ruff check .
```

### 8. Check Coverage

```bash
# Rust (with cargo-tarpaulin)
cargo tarpaulin --out Html

# C++ (with gcov/lcov)
cmake -DCMAKE_BUILD_TYPE=Coverage ..
make && make coverage

# Python
pytest --cov=src --cov-report=html tests/
```

**Coverage targets:**
- **80% minimum** for all code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical code
  - Core business logic

## Test Categories

### Unit Tests (Function-level)
- Happy path scenarios
- Edge cases (empty, null, max values, NaN, infinity)
- Error conditions
- Boundary values

### Integration Tests (Component-level)
- API endpoints
- Database operations
- External service calls
- Module interactions

### Property-Based Tests
- **Rust**: proptest, quickcheck
- **C++**: RapidCheck
- **Python**: hypothesis

## Language-Specific Best Practices

### Rust
```bash
# Run all tests with all features
cargo test --all-features

# Run specific test
cargo test test_name

# Run with output
cargo test -- --nocapture

# Doc tests
cargo test --doc
```

**Test organization:**
- Unit tests: `#[cfg(test)]` module in same file
- Integration tests: `tests/` directory
- Doc tests: `///` comments with examples

### C++
```bash
# CMake with testing
cmake -DBUILD_TESTING=ON ..
cmake --build .
ctest --output-on-failure

# Run specific test
ctest -R test_pattern
```

**Test organization:**
- Unit tests: `tests/` directory with `*_test.cpp`
- Fixtures: `class TestName : public ::testing::Test`
- Mocks: Google Mock / FakeIt

### Python
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-fail-under=80

# Run specific test
pytest tests/test_module.py::TestClass::test_method -v

# Run marked tests
pytest -m "not slow"
```

**Test organization:**
- Tests in `tests/` directory
- Fixtures in `conftest.py`
- Parametrized tests: `@pytest.mark.parametrize`

## TDD Anti-Patterns to Avoid

**DON'T:**
- ❌ Write implementation before tests
- ❌ Skip the RED phase (verify test fails first)
- ❌ Write too much code at once
- ❌ Ignore failing tests
- ❌ Test implementation details (test behavior instead)
- ❌ Mock everything (prefer real dependencies when possible)
- ❌ Write tests after the fact (that's not TDD)

**DO:**
- ✅ Write the test FIRST
- ✅ Run tests and verify they FAIL
- ✅ Write MINIMAL code to pass
- ✅ Refactor only after GREEN
- ✅ Test edge cases and error scenarios
- ✅ Aim for 80%+ coverage

## Workflow Integration

1. **Start**: Define interface/signature (SCAFFOLD)
2. **RED**: Write failing test
3. **Verify**: Run test, confirm it fails
4. **GREEN**: Write minimal implementation
5. **Verify**: Run test, confirm it passes
6. **REFACTOR**: Improve code quality
7. **Verify**: Run test, confirm still passing
8. **REPEAT**: Next test case / feature

## Related Commands

- `/update-docs` - Update documentation after implementation
- `/rust:commit` - Commit after TDD cycle (runs clippy + tests)
- `/rust:review` - Review code quality

## Context

$ARGUMENTS
