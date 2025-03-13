# Mojo Programming Language Testing and Debugging Tools

## TITLE: Mojo Testing and Debugging Tools
## VERSION: 2025-03
## RELEASED: 2025-03-12
## COMPATIBILITY: Mojo 0.5.0+, MAX SDK
## DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/tools/
## MODEL: Claude-3.7-Sonnet-Thinking

## Conceptual Overview

- Mojo provides comprehensive debugging tools including a VS Code integration and LLDB-based debugging system
- GPU debugging is supported through CUDA-GDB for debugging Mojo code running on NVIDIA GPUs
- A flexible unit testing framework is included in the standard library with the `testing` module
- Tests are defined as functions that start with `test_` and use assertion utilities to verify code behavior
- The Mojo command line includes the `mojo test` and `mojo debug` commands for test execution and debugging

## Technical Reference

### Mojo Debugging Framework [`STABLE`]

**Package:** Mojo SDK core tools
**Available Since:** Early SDK versions
**Status:** Stable

**Dependencies/Imports:**
```mojo
# No specific imports needed to use the debugger
# For programmatic breakpoints:
from builtin import breakpoint
```

**Context:**
- Purpose: Provides integration with VS Code debugger and LLDB for debugging Mojo applications
- Patterns: Support for standard debugging operations - breakpoints, stepping, variable inspection
- Alternatives: Command-line LLDB for terminal-based debugging
- Limitations: No support for hot code reloading or dynamic code evaluation within the debugger
- Related: GPU debugging with CUDA-GDB

#### VS Code Debugging Integration [`STABLE`]

**Usage Example:**
```mojo
# No specific code needed - just launch VS Code with the Mojo extension
# and use debugging features like breakpoints and the Debug toolbar
```

The VS Code Mojo extension enables several ways to start a debug session:
- Quick run or debug from the editor toolbar
- Launch configurations in launch.json
- Command palette
- F5 keyboard shortcut
- Debug view

Debug button actions include:
- Continue/Pause
- Step Over
- Step Into
- Step Out
- Restart
- Stop

**Edge Cases and Anti-patterns:**
- Breakpoints in GPU code behave differently, appearing in CPU functions before the GPU kernel launches
- VS Code RPC connection issues may occur when multiple VS Code windows are open

**Migration:** Moving from a command-line LLDB workflow to VS Code debugging requires minimal changes.

### Command-line Debugging [`STABLE`]

**Signature:**
```
mojo debug [options] <file>
mojo debug --vscode <file>  # Start VS Code debugging session
mojo debug --cuda-gdb <file>  # Debug with CUDA-GDB for GPU code
```

**Usage Example:**
```shell
# Debug a Mojo file with VS Code
mojo debug --vscode myproject.mojo

# Debug a compiled binary
mojo debug --vscode myproject

# Attach to a running process
mojo debug --vscode --pid <PROCESS_ID>
```

**Context:**
- Purpose: Provides command-line interface to the Mojo debugger
- Patterns: Connects to VS Code or launches LLDB directly
- Behavior: Non-blocking when launched with VS Code

### Programmatic Breakpoints [`STABLE`]

**Signature:**
```mojo
fn breakpoint()
```

**Usage Example:**
```mojo
if some_value.is_valid():
   do_the_right_thing()
else:
   # We should never get here!
   breakpoint()
```

**Context:**
- Purpose: Programmatically insert breakpoints in code
- Patterns: Used for conditional debugging or to catch error conditions
- Related: Can combine with `param_env` for conditional debugging

### Launch Configurations [`STABLE`]

Launch configurations in VS Code define how the debugger starts your application.

**Usage Example:**
```json
{
  "type": "mojo-lldb",
  "request": "launch",
  "name": "Debug current Mojo file",
  "mojoFile": "${file}",
  "args": [],
  "env": {},
  "cwd": "${workspaceFolder}"
}
```

Common template configurations include:
- Debug current Mojo file
- Debug Mojo file (specific file)
- Debug binary
- Attach to process

**Edge Cases and Anti-patterns:**
- Launch configurations must include either `mojoFile` or `program` for launch requests
- For attach requests, must include either `pid` or `program`

### GPU Debugging [`STABLE`]

**Package:** Mojo SDK with CUDA-GDB integration
**Available Since:** Mojo 0.4.0+
**Status:** Stable for NVIDIA GPUs

**Dependencies/Imports:**
```
# External dependencies
- NVIDIA CUDA Toolkit 12.4+
- NVIDIA GPU with CUDA support
- Nsight Visual Studio Code Extension (for VS Code debugging)
```

**Signature:**
```
mojo debug --cuda-gdb [options] <file>
mojo debug --cuda-gdb --break-on-launch --vscode <file>
```

**Usage Example:**
```shell
# Start GPU debugging with VS Code, breaking at kernel launch
mojo debug --cuda-gdb --break-on-launch --vscode my_gpu_code.mojo
```

**Launch Configuration Example:**
```json
{
  "type": "mojo-cuda-gdb",
  "request": "launch",
  "name": "Mojo: Debug current Mojo file with CUDA-GDB",
  "mojoFile": "${file}",
  "args": [],
  "env": [],
  "cwd": "${workspaceFolder}",
  "breakOnLaunch": true,
  "legacyDebugger": true,
  "initCommands": [
      "set environment CUDBG_USE_LEGACY_DEBUGGER=1"
  ]
}
```

**Context:**
- Purpose: Debug Mojo code running on NVIDIA GPUs
- Patterns: Uses CUDA-GDB as the debugging backend
- Limitations: 
  - Currently only supports NVIDIA GPUs
  - Stepping commands don't work reliably in GPU code
  - Symbol breakpoints not supported

**Edge Cases and Anti-patterns:**
- Breakpoints in GPU code need to be set after kernel launch
- Use `--break-on-launch` to pause at kernel launch for setting breakpoints
- Some systems require the classic debugger backend via `CUDBG_USE_LEGACY_DEBUGGER=1`

**CUDA-GDB Commands:**
```
# Change kernel focus
cuda block 0,0,0 thread 1,0,0

# Inspect registers
info registers $R0 $R1
```

### Mojo Testing Framework [`STABLE`]

**Package:** `testing` module in Mojo standard library
**Available Since:** Mojo 0.4.0+
**Status:** Stable

**Signature:**
```mojo
from testing import assert_true, assert_false, assert_equal, assert_not_equal, assert_almost_equal, assert_raises
```

**Dependencies/Imports:**
```mojo
from testing import assert_true, assert_false, assert_equal, assert_not_equal, assert_almost_equal, assert_raises
```

**Usage Example:**
```mojo
# Write a test function that starts with "test_"
def test_something():
    # Use assertions to verify behavior
    assert_equal(2 + 2, 4)
    assert_true(some_condition())
    
    # Test that exceptions are raised correctly
    with assert_raises():
        # Code that should raise an exception
        raise Error("expected error")
```

**Context:**
- Purpose: Provides a framework for unit testing Mojo code
- Patterns: Define test functions prefixed with `test_` that use assertion utilities
- Related: Works with the `mojo test` command-line tool

#### Assertion Functions [`STABLE`]

**Signatures:**
```mojo
fn assert_true(condition: Bool, msg: String = "") raises
fn assert_false(condition: Bool, msg: String = "") raises
fn assert_equal[T: __eq__[T, Bool], U: __eq__[U, Bool] where __eq__[T, U, Bool]](left: T, right: U, msg: String = "") raises
fn assert_not_equal[T: __eq__[T, Bool], U: __eq__[U, Bool] where __eq__[T, U, Bool]](left: T, right: U, msg: String = "") raises
fn assert_almost_equal[T: __sub__[T, T] & Copyable & Sized, U: __sub__[U, U] & Copyable & Sized](left: T, right: U, atol: F64 = 1e-8, rtol: F64 = 1e-5, msg: String = "") raises where __sub__[T, U, SIMD[DType.float64, 1]]
```

**Context Manager:**
```mojo
fn assert_raises(contains: String = "") raises -> _AssertRaisesContext
```

**Usage Example:**
```mojo
# Boolean assertions
assert_true(value > 0)
assert_false(is_invalid)

# Equality assertions
assert_equal(calculate(), expected_result)
assert_not_equal(pointer1, pointer2)

# Floating point comparison
assert_almost_equal(10/3, 3.33, atol=0.01)

# Exception testing
with assert_raises():
    # Code that should raise an exception
    raise Error("something went wrong")

# Check exception message content
with assert_raises(contains="invalid argument"):
    raise Error("invalid argument provided")
```

**Edge Cases and Anti-patterns:**
- Don't use `assert_equal` for floating point comparisons; use `assert_almost_equal` instead
- The first failed assertion in a test function aborts the test
- When testing for exceptions, the test fails if no exception is raised

### Mojo Test Command [`STABLE`]

**Signature:**
```
mojo test [options] <test-id|file|directory>
```

**Common Options:**
- `-I <path>`: Add directory to import search path
- `--collect-only`, `--co`: Only collect test names without running them
- `--diagnostic-format json`: Output test results in JSON format

**Usage Example:**
```shell
# Run all tests in a directory
mojo test -I src test

# Run a specific test file
mojo test -I src test/my_math/test_dec.mojo

# Run a specific test
mojo test -I src 'test/my_math/test_dec.mojo::test_dec_valid()'

# Collect tests without running them
mojo test --co test

# Output results in JSON format
mojo test --diagnostic-format json test_file.mojo
```

**Context:**
- Purpose: Command-line tool for running Mojo tests
- Patterns: Discovers tests in files with names containing "test", executes them, and reports results
- Related: Works with the `testing` module

## Links to Further Documentation

- [Mojo Debugging Documentation](https://docs.modular.com/mojo/tools/debugging/)
- [GPU Debugging Guide](https://docs.modular.com/mojo/tools/gpu-debugging/)
- [Mojo Testing Documentation](https://docs.modular.com/mojo/tools/testing/)
- [CUDA-GDB Documentation](https://docs.nvidia.com/cuda/cuda-gdb/index.html)
- [VS Code Debugging Documentation](https://code.visualstudio.com/docs/editor/debugging)
- [Example Testing Project](https://github.com/modular/max/tree/main/examples/mojo/testing)