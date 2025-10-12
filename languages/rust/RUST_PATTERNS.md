# Rust Development Patterns for AI Agents

## BUILD PATTERNS

### Development Builds
```
IF: Iterating on code changes
THEN: cargo build
WHY: Fast, unoptimized builds for development
```

### Release Builds
```
IF: Benchmarking or profiling
THEN: cargo build --release
WHY: Optimized builds (10-100x faster runtime, slower compile)

IF: Final testing before release
THEN: cargo build --release && cargo test --release
WHY: Test with optimizations enabled
```

## TESTING PATTERNS

### Run All Tests
```bash
cargo test                        # All tests, parallel (built-in)
cargo test --release              # With optimizations
cargo test --lib                  # Library tests only
cargo test --test integration     # Specific integration test

# Modern alternatives (2025):
cargo nextest run                 # Faster parallel test runner (cargo install cargo-nextest)
cargo nextest run --retries 3     # With retries for flaky tests
```

### Debug Test Output
```
PROBLEM: Test fails, need to see output
SOLUTION: cargo test [name] -- --nocapture
WHY: By default cargo captures stdout/stderr
```

### Debug Single Test
```
PROBLEM: One test fails in test suite
SOLUTION:
1. cargo test [test_name] -- --nocapture
2. Check git log -- [test_file]
3. Run with breakpoint/println! debugging
```

### Serial Test Execution
```
WHEN: Tests interfere with each other
THEN: cargo test -- --test-threads=1
WHY: Forces serial execution, prevents race conditions
```

## PROFILING PATTERNS

### CPU Profiling
```bash
# Option 1: cargo flamegraph (easiest)
cargo install flamegraph
cargo flamegraph --bin [binary_name]
# Opens flamegraph.svg in browser

# Option 2: perf (Linux)
cargo build --release
perf record --call-graph dwarf ./target/release/[binary]
perf report

# Option 3: Instruments (macOS)
instruments -t "Time Profiler" ./target/release/[binary]
```

### Memory Profiling
```bash
# Option 1: valgrind
cargo build
valgrind --leak-check=full --show-leak-kinds=all ./target/debug/[binary]

# Option 2: heaptrack (Linux)
heaptrack ./target/release/[binary]
heaptrack_gui heaptrack.[binary].gz

# Option 3: DHAT (Dynamic Heap Analysis Tool, 2025)
# Add to Cargo.toml: dhat = "0.3"
cargo build --release --features dhat-heap
./target/release/[binary]
# Generates dhat-heap.json, view at https://nnethercote.github.io/dh_view/dh_view.html

# Option 4: Miri (Undefined Behavior detection)
cargo +nightly miri test          # Requires nightly
cargo +nightly miri run
```

### Benchmark Timing
```bash
# Use hyperfine for accurate benchmarking
hyperfine './target/release/[binary]'
hyperfine --warmup 3 './target/release/[binary]'

# Compare two versions
hyperfine './target/release/v1' './target/release/v2'
```

## ERROR HANDLING PATTERNS

### Common Rust Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `cannot borrow as mutable` | Multiple borrows | Scope mutable borrow shorter |
| `use of moved value` | Value consumed | Use reference or clone |
| `cannot move out of borrowed content` | Trying to move from reference | Clone or take ownership |
| `lifetime may not live long enough` | Lifetime mismatch | Add explicit lifetime annotations |

### Performance Regression
```
SYMPTOMS: Benchmark slower than baseline
DIAGNOSIS:
1. git log --grep="perf"
2. git bisect start HEAD [last_good_commit]
3. Profile both versions: cargo flamegraph --bin [bench]

FIX:
1. Identify hot path differences
2. Check for allocations (cargo-flamegraph shows alloc::)
3. Consider using --release for fair comparison
```

## CODE QUALITY PATTERNS

### Linting
```bash
cargo clippy                      # Standard lints
cargo clippy -- -W clippy::all    # All warnings
cargo clippy --fix                # Auto-fix issues
```

### Formatting
```bash
cargo fmt                         # Format code
cargo fmt -- --check              # Check without modifying
```

### Documentation
```bash
cargo doc --open                  # Generate and open docs
cargo doc --no-deps               # Only your crate
```

## DEPENDENCY PATTERNS

### Add Dependencies
```bash
cargo add [crate]                 # Add to dependencies
cargo add --dev [crate]           # Add to dev-dependencies
cargo add --build [crate]         # Add to build-dependencies
```

### Update Dependencies
```bash
cargo update                      # Update within semver
cargo upgrade                     # Update to latest (requires cargo-edit)
cargo outdated                    # Check for outdated deps
```

### Audit Dependencies
```bash
cargo audit                       # Security vulnerabilities (RustSec database)
cargo deny check                  # Dependency auditing (advisories, licenses, bans)
cargo tree                        # Dependency tree
cargo tree --duplicates           # Find duplicate deps
cargo outdated                    # Check for outdated dependencies
```

## PERFORMANCE OPTIMIZATION PATTERNS

### Identify Bottlenecks
```
STEP 1: Profile first (cargo flamegraph)
STEP 2: Look for:
  - Allocations in hot paths (Vec::new, String::from)
  - Unnecessary clones
  - Inefficient algorithms (O(n²) loops)
  - Lock contention (if concurrent)

STEP 3: Optimize high-impact areas only
```

### Common Optimizations
```rust
// ❌ SLOW: Repeated allocations
for item in items {
    let mut vec = Vec::new();  // Allocates each iteration
    vec.push(item);
}

// ✅ FAST: Reuse allocation
let mut vec = Vec::with_capacity(items.len());
for item in items {
    vec.push(item);
}

// ❌ SLOW: Unnecessary clones
let data = expensive_data.clone();  // If data not needed later

// ✅ FAST: Move instead of clone
let data = expensive_data;  // Take ownership

// ❌ SLOW: String concatenation in loop
let mut result = String::new();
for s in strings {
    result = result + s;  // Allocates each time
}

// ✅ FAST: Use push_str
let mut result = String::with_capacity(estimated_size);
for s in strings {
    result.push_str(s);
}
```

## TESTING BEST PRACTICES

### Test Organization
```rust
// Unit tests: Same file as implementation
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_functionality() {
        // Arrange
        let input = setup();

        // Act
        let result = function(input);

        // Assert
        assert_eq!(result, expected);
    }
}

// Integration tests: tests/ directory
// File: tests/integration_test.rs
#[test]
fn test_full_workflow() {
    // Test public API only
}
```

### Test Fixtures
```rust
// ❌ WRONG: Duplication
#[test]
fn test1() {
    let data = vec![1, 2, 3];
    // test
}

#[test]
fn test2() {
    let data = vec![1, 2, 3];  // Duplicate setup
    // test
}

// ✅ CORRECT: Shared helper
fn setup_test_data() -> Vec<i32> {
    vec![1, 2, 3]
}

#[test]
fn test1() {
    let data = setup_test_data();
    // test
}
```

## DEBUGGING PATTERNS

### Print Debugging
```rust
// Quick debug print
println!("{:?}", value);      // Debug format
println!("{:#?}", value);     // Pretty debug format

// In tests (won't show unless --nocapture)
eprintln!("Debug: {:?}", value);  // To stderr
```

### GDB/LLDB Debugging
```bash
# Build with debug symbols
cargo build

# Run with debugger
rust-gdb ./target/debug/[binary]
rust-lldb ./target/debug/[binary]

# Commands
(gdb) break main.rs:42
(gdb) run
(gdb) backtrace
(gdb) print variable
```

## DECISION TREES

### When to Use --release
```
IF: Benchmarking performance
    → MUST use --release

IF: Testing correctness
    → Use debug (faster iteration)

IF: Profiling
    → Use --release (unless debugging issue specific to debug)

IF: CI/Production
    → MUST use --release
```

### When to Clone vs Move
```
IF: Value needed in multiple places
    → Clone

IF: Value no longer needed
    → Move (take ownership)

IF: Large value, expensive to clone
    → Use reference (&) or Arc<T>

IF: Performance critical
    → Profile first, then decide
```

### When to Use Arc vs Rc
```
IF: Multi-threaded
    → Arc<T> (atomic reference counting)

IF: Single-threaded
    → Rc<T> (cheaper, no atomics)

IF: Need interior mutability
    → Arc<Mutex<T>> or Arc<RwLock<T>>
```

## COMMON ANTI-PATTERNS

### Over-Cloning
```rust
// ❌ WRONG: Unnecessary clone
fn process(data: Vec<i32>) {
    let copy = data.clone();  // Why?
    // ... use copy
}

// ✅ CORRECT: Use reference if not consuming
fn process(data: &[i32]) {
    // ... use data
}

// ✅ CORRECT: Move if consuming
fn process(data: Vec<i32>) {
    // ... consume data
}
```

### Premature Optimization
```
❌ WRONG:
1. Write complex optimized code first
2. Spend hours on micro-optimizations
3. No profiling

✅ CORRECT:
1. Write clear, simple code
2. Profile to find actual bottlenecks
3. Optimize only hot paths (80/20 rule)
```

### Ignoring Errors
```rust
// ❌ WRONG: Unwrap in production
let data = file.read().unwrap();  // Panic if error

// ✅ CORRECT: Handle errors
let data = file.read()?;  // Propagate error
// or
let data = file.read().expect("Failed to read file");  // With context
```

## PERFORMANCE BENCHMARKING

### Fair Comparisons
```
RULES:
1. Same features on both sides (with/without optimizations)
2. Same data distribution (not best-case vs worst-case)
3. Warmup period (first run is often slower)
4. Multiple runs (report median of 3+)
5. Document what IS and ISN'T tested

WRONG: "Our in-memory struct vs SQLite with disk I/O"
RIGHT: "Our implementation vs baseline, both in-memory"
```

### Benchmark Structure
```rust
use std::time::Instant;

fn benchmark_operation() {
    // Warmup
    for _ in 0..100 {
        operation();
    }

    // Timed runs
    let runs = 10;
    let mut times = Vec::new();

    for _ in 0..runs {
        let start = Instant::now();
        operation();
        times.push(start.elapsed());
    }

    // Report median
    times.sort();
    let median = times[runs / 2];
    println!("Median: {:?}", median);
}
```

## VERSION CONTROL INTEGRATION

### Git Bisect with Cargo
```bash
# Find regression commit
git bisect start
git bisect bad HEAD
git bisect good [last_known_good]

# Create bisect script: test.sh
#!/bin/bash
cargo test || exit 1
cargo build --release || exit 1
timeout 60s ./target/release/benchmark || exit 1

# Run bisect
git bisect run ./test.sh
```

## MODERN TOOLING (2025)

### Essential Tools
```bash
# Testing
cargo install cargo-nextest       # Faster test runner
cargo install cargo-tarpaulin     # Code coverage

# Security & Dependencies
cargo install cargo-audit         # Security vulnerabilities
cargo install cargo-deny          # License/advisory checking
cargo install cargo-outdated      # Check outdated deps

# Profiling & Performance
cargo install flamegraph          # CPU profiling visualization
cargo install cargo-instruments   # macOS profiling (Instruments.app)

# Code Quality
cargo install cargo-udeps         # Find unused dependencies
cargo install cargo-machete       # Find unused dependencies (faster)
```

### Advanced Tools
```bash
# Undefined Behavior Detection
rustup component add miri         # Requires nightly
cargo +nightly miri test

# Fuzzing
cargo install cargo-fuzz          # Fuzzing harness
cargo +nightly fuzz run [target]

# Binary Analysis
cargo install cargo-bloat         # Find what takes space in binary
cargo install cargo-expand        # Expand macros
```

## RESOURCES

**Official:**
- [Rust Book](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Cargo Book](https://doc.rust-lang.org/cargo/)

**Performance:**
- [Rust Performance Book](https://nnethercote.github.io/perf-book/)
- [Criterion.rs](https://github.com/bheisler/criterion.rs) - Benchmarking
- [DHAT Viewer](https://nnethercote.github.io/dh_view/dh_view.html) - Memory profiling

**Security:**
- [RustSec Advisory Database](https://rustsec.org/)
- [Rust Security Best Practices](https://ansasecurity.github.io/docs/rust-security/)

**Patterns:**
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
- [API Guidelines](https://rust-lang.github.io/api-guidelines/)

**Community:**
- [This Week in Rust](https://this-week-in-rust.org/) - Weekly newsletter
- [Rust Blog](https://blog.rust-lang.org/) - Official updates
