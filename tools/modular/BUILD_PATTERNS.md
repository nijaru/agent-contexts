# Modular Build Patterns

## DECISION: Build System Selection
```
IF working_in_modular_repo:
    → ./bazelw build //...
ELIF has_pixi_toml:
    → pixi install && pixi run [task]
ELSE:
    → mojo [file]
```

## PATTERN: Bazel Commands
```bash
# ❌ WRONG: Using raw bazel
bazel build //...

# ✅ CORRECT: Using wrapper
./bazelw build //...

# Common patterns
./bazelw build //max/kernels/...   # Build GPU kernels
./bazelw build //mojo/stdlib/...   # Build stdlib
./bazelw test //... --config=asan  # Test with sanitizers
./bazelw test --runs_per_test=10   # Multiple test runs
```

## PATTERN: Pixi Task Discovery
```bash
# Check available tasks
pixi task list

# Common task patterns
pixi run main      # Run main entry point
pixi run test      # Run tests
pixi run format    # Format code
pixi run benchmark # Run benchmarks

# Task locations
# /mojo/: build, tests, examples, benchmarks
# /max/: llama3, mistral, generate, serve
# /examples/*/: main, test, hello, dev-server
```

## DECISION: Environment Setup
```
IF need_MAX_server:
    IF want_docker:
        → docker run --gpus=1 -p 8000:8000 docker.modular.com/modular/max-nvidia-full:latest
    ELIF want_pip:
        → pip install modular --index-url https://dl.modular.com/public/nightly/python/simple/
    ELSE:
        → pixi global install -c conda-forge -c https://conda.modular.com/max-nightly

IF need_mojo_dev:
    → Install nightly VS Code extension
    → Use nightly Mojo builds
```

## ERROR → SOLUTION MAPPINGS

| Build Error | Fix | Context |
|-------------|-----|---------|
| `bazel: command not found` | Use `./bazelw` wrapper | Always use wrapper |
| `pixi: command not found` | `curl -fsSL https://pixi.sh/install.sh \| bash` | Install Pixi |
| `No pixi.toml found` | Check parent directories or use bazel | Wrong directory |
| `Target not found` | Use `//...` or check BUILD.bazel files | Invalid target |

## PATTERN: Performance Development
```bash
# Run benchmarks with env vars
./bazelw run //max/kernels/benchmarks/gpu:bench_matmul -- \
    env_get_int[M]=1024 env_get_int[N]=1024 env_get_int[K]=1024

# Use autotune
python max/kernels/benchmarks/autotune/kbench.py benchmarks/gpu/bench_matmul.yaml

# Common env variables
env_get_int[param_name]=value
env_get_bool[flag_name]=true/false  
env_get_dtype[type]=float16/float32
```

## PATTERN: Git Commit Format
```bash
# ❌ WRONG: Generic commit
git commit -m "fix bug"

# ✅ CORRECT: Modular format
git commit -s -m "[Stdlib] Fix memory leak in String.copy

BEGIN_PUBLIC
[Stdlib] Fix memory leak in String.copy

This fixes a memory leak where String.copy() didn't properly
deallocate the internal buffer when copying empty strings.
END_PUBLIC"

# Tags to use
[Stdlib]   # Standard library changes
[Kernels]  # Kernel modifications
[GPU]      # GPU-specific changes
[Docs]     # Documentation updates
```

## COMMAND SEQUENCES

### SEQUENCE: New Feature Development
```bash
# 1. Setup environment
pixi install

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Build and test iteratively
./bazelw build //path/to:target
./bazelw test //path/to:test

# 4. Format code
pixi run mojo format ./

# 5. Run full test suite
./bazelw test //...

# 6. Commit with proper format
git commit -s -m "[Tag] Description..."
```

### SEQUENCE: Debug Build Failure
```bash
# 1. Clean build cache
./bazelw clean

# 2. Verbose build
./bazelw build //target --verbose_failures

# 3. Check with sanitizers
./bazelw build --config=asan //target

# 4. Examine build graph
./bazelw query "deps(//target)"
```

## STATE RECOGNITION
```
NO_BUILD_FILE: Missing BUILD.bazel → Create or move to correct dir
PIXI_NOT_INSTALLED: No pixi.toml → Use bazel or install pixi
TEST_FAILURE: Check with --test_output=all
BENCHMARK_SLOW: Add env vars to reduce problem size
```

---
*Optimized for Modular repository development*