# Mojo Version 24.6 Changelog Documentation

```
TITLE: Mojo Programming Language - Version 24.6
VERSION: 24.6
RELEASED: 2024-12-17
COMPATIBILITY: Compatible with previous versions with some rename/syntax changes
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/
```

## Conceptual Overview

- Argument conventions `inout` and `borrowed` renamed to `mut` and `read` with new `out` convention for constructors and named results
- `Lifetime` and related types renamed to `Origin` to better describe their purpose in reference handling
- Implicit conversions now require explicit opt-in with the `@implicit` decorator
- New collection types added to standard library including `Deque` (double-ended queue) and `OwnedPointer` (safe smart pointer)
- Improved VS Code debugging experience with data breakpoints, function breakpoints, and symbol breakpoints

## Core Language

### Argument Convention Renaming [`CHANGED`]

**Status:** Stable
**Breaking:** No (Old syntax still supported in this version)

**Context:**
- The `inout` and `borrowed` argument conventions have been renamed to `mut` and `read` respectively
- These verbs reflect what the callee can do to the argument value passed by the caller
- Old syntax still works but will be removed in future versions

**Usage Example:**
```mojo
# Before 24.6
struct TaskManager:
    var tasks: List[Task]

    fn add_task(inout self, task: Task):
        self.tasks.append(task)

    fn show_tasks(self):
        for t in self.tasks:
            print("- ", t[].description)

# After 24.6
struct TaskManager:
    var tasks: List[Task]

    fn add_task(mut self, task: Task):
        self.tasks.append(task)

    fn show_tasks(self):
        for t in self.tasks:
            print("- ", t[].description)
```

**Migration:**
```mojo
// BEFORE:
fn example(borrowed x: String) -> None:
    pass

// AFTER:
fn example(read x: String) -> None:
    pass
```

**Migration Difficulty:** Simple

### Constructor Argument Convention [`CHANGED`]

**Status:** Stable
**Breaking:** No (Old syntax still supported in this version)

**Context:**
- The argument convention for the `self` argument in `__init__()`, `__copyinit__()`, and `__moveinit__()` methods changed from `inout` to `out`
- This reflects that constructors initialize values without reading from them

**Usage Example:**
```mojo
@value
struct Task:
    var description: String

    # Before 24.6
    fn __init__(inout self, desc: String):
        self.description = desc

    # After 24.6
    fn __init__(out self, desc: String):
        self.description = desc
```

**Migration:**
```mojo
// BEFORE:
struct Foo:
    fn __init__(inout self): pass

// AFTER:
struct Foo:
    fn __init__(out self): pass
```

**Migration Difficulty:** Simple

### Named Results Syntax [`CHANGED`]

**Status:** Stable
**Breaking:** No (Old syntax still supported in this version)

**Context:**
- Named results now use `out` syntax instead of `-> T as name`
- Functions may have at most one named result or return type with `->` syntax
- `out` arguments can appear anywhere in the argument list but are typically last

**Usage Example:**
```mojo
struct TaskManager:
    var tasks: List[Task]

    # Before 24.6
    @staticmethod
    fn bootstrap_example() -> TaskManager as manager:
        manager = TaskManager()
        manager.add_task("Default Task #0")
        manager.add_task("Default Task #1")
        return

    # After 24.6
    @staticmethod
    fn bootstrap_example(out manager: TaskManager):
        manager = TaskManager()
        manager.add_task("Default Task #0")
        manager.add_task("Default Task #1")
        return  # 'manager' is implicitly returned
```

**Migration:**
```mojo
// BEFORE:
fn example() -> String as result:
    result = "foo"

// AFTER:
fn example(out result: String):
    result = "foo"
```

**Migration Difficulty:** Simple

### Implicit Conversions [`CHANGED`]

**Status:** Stable
**Breaking:** Yes

**Context:**
- Single argument constructors now require the `@implicit` decorator to allow implicit conversions
- Makes code clearer and avoids surprising behavior
- Without the decorator, explicit construction is required

**Usage Example:**
```mojo
# Without @implicit - Explicit conversion required
struct Task:
    var description: String

    fn __init__(out self, desc: String):
        self.description = desc

# User code must explicitly create Task objects
manager.add_task(Task("Walk the dog"))

# With @implicit - Allows implicit conversion
struct Task:
    var description: String

    @implicit  # Explicitly opt-in to implicit conversion
    fn __init__(out self, desc: String):
        self.description = desc

    @implicit  # Also allow conversion from string literals
    fn __init__(out self, desc: StringLiteral):
        self.description = desc

# User code can now use strings directly
manager.add_task(String("Walk the dog"))
manager.add_task("Write Mojo 24.6 blog post")  # StringLiteral works too
```

**Migration:**
```mojo
// BEFORE (implicit conversion allowed):
struct Foo:
    var value: Int
    fn __init__(out self, value: Int):
        self.value = value

// AFTER (explicit conversion required):
struct Foo:
    var value: Int
    fn __init__(out self, value: Int):
        self.value = value

// To re-enable implicit conversion:
struct Foo:
    var value: Int
    @implicit
    fn __init__(out self, value: Int):
        self.value = value
```

**Migration Difficulty:** Medium

### Origin (Formerly Lifetime) System [`CHANGED`]

**Status:** Stable
**Breaking:** No (Old syntax still supported in this version)

**Context:**
- `Lifetime` and related types renamed to `Origin` to better clarify their purpose
- `__lifetime_of()` operator renamed to `__origin_of()`
- Can now specify a union of origins with multiple values in `__origin_of()` or inside `ref [a, b]`
- `Origin` is now a complete wrapper around the MLIR origin type
- `ref` arguments without an origin clause are treated as `ref [_]` for convenience

**Usage Example:**
```mojo
struct TaskManager:
    var tasks: List[Task]

    # Return a reference to a task with origin tracking
    fn get_task(ref self, index: Int) -> ref [self.tasks] Task:
        # The [self.tasks] annotation shows this reference originates from the tasks list
        return self.tasks[index]

# Function that handles multiple origins
fn pick_longer(ref t1: Task, ref t2: Task) -> ref [t1, t2] Task:
    # The [t1, t2] annotation shows this reference could come from either t1 or t2
    return t1 if len(t1.description) >= len(t2.description) else t2

# Usage example
def main():
    manager = TaskManager()
    manager.add_task("Short task")
    manager.add_task("This is a longer task")

    # Get a reference to tasks
    first_task = manager.get_task(0)
    first_task.description = "Walk the dog ASAP!"  # Safe modification

    # Compare tasks by length
    longer = pick_longer(first_task, manager.get_task(1))
    print("Longer task: ", longer.description)
```

**Migration:**
```mojo
// BEFORE:
fn return_ref(a: String) -> ref[__lifetime_of(a)] String:
    return a

// AFTER:
fn return_ref(a: String) -> ref[a] String:
    return a
```

**Migration Difficulty:** Simple

## Standard Library

### Deque Collection [`NEW`]

**Package:** `collections.deque`
**Status:** Stable

**Context:**
- Double-ended queue based on a dynamic circular buffer
- Efficient O(1) additions and removals at both ends
- O(1) direct access to all elements
- Supports full Python `collections.deque` API
- Includes enhancements like `peek()` and `peekleft()` methods

**Usage Example:**
```mojo
from collections import Deque

struct TaskManager:
    # Using Deque instead of List
    var tasks: Deque[Task]

    fn __init__(out self):
        self.tasks = Deque[Task]()

    fn add_task(mut self, task: Task):
        # Add to back (normal priority)
        self.tasks.append(task)

    fn add_urgent_task(mut self, task: Task):
        # Add to front (high priority)
        self.tasks.appendleft(task)
```

### OwnedPointer [`NEW`]

**Package:** `memory.owned_pointer`
**Status:** Stable

**Context:**
- Provides safe, single-owner, non-nullable smart pointer functionality
- Ensures automatic cleanup when going out of scope
- Features move semantics with the `^` operator
- Always points to valid data (non-nullable)
- Ideal for managing resources that need deterministic cleanup

**Usage Example:**
```mojo
from memory import OwnedPointer

@value
struct HeavyResource:
    var data: String

    fn __init__(out self, data: String):
        self.data = data

    fn do_work(self):
        print("Processing:", self.data)

struct Task:
    var description: String
    var heavy_resource: OwnedPointer[HeavyResource]

    @implicit
    fn __init__(out self, desc: StringLiteral):
        self.description = desc
        self.heavy_resource = OwnedPointer[HeavyResource](
            HeavyResource("Heavy resource with description: " + desc)
        )

    fn __moveinit__(out self, owned other: Task):
        self.description = other.description^
        self.heavy_resource = other.heavy_resource^
```

### Writer Trait [`NEW`]

**Package:** `utils.write`
**Status:** Stable

**Context:**
- Replaces the `Formatter` struct with a more general-purpose `Writer` trait
- Enables buffered IO for performance comparable to C
- Can write any `Span[Byte]`
- The `Formattable` trait is now named `Writable`
- `String.format_sequence()` is now `String.write()`

**Migration:**
```mojo
// BEFORE:
var s = String.format_sequence("Value: ", 42)

// AFTER:
var s = String.write("Value: ", 42)
```

**Migration Difficulty:** Simple

### TypedPythonObject [`NEW`]

**Package:** `python.python_object`
**Status:** Experimental

**Context:**
- Light-weight way to annotate `PythonObject` values with static type information
- Design likely to evolve significantly in future versions
- Added `TypedPythonObject["Tuple].__getitem__()` for accessing elements of a Python tuple

### Associated Types [`NEW`]

**Status:** Stable

**Context:**
- Allows defining type aliases within traits that can be specified in conforming structs
- Example: `alias T: AnyType`, `alias N: Int` in a trait

## Tooling Changes

### VS Code Extension Enhancements [`IMPROVED`]

**Status:** Stable
**Breaking:** No

**Context:**
- VS Code extension now supports setting data breakpoints to watch specific variables or struct fields for changes
- Added support for function breakpoints to break execution when specific functions are called
- Extension now automatically opens the Run and Debug tab when a debug session starts
- Enhanced LSP and documentation display for origins and parametric types

### Mojo LLDB Debugger Improvements [`IMPROVED`]

**Status:** Stable
**Breaking:** No

**Context:**
- Now supports symbol breakpoints (e.g., `b main` or `b my_module::main`)
- The `mojo debug --rpc` command has been renamed to `mojo debug --vscode`
- Command now supports multiple VS Code windows
- Supports a `break-on-raise` command to stop at any `raise` statements
- Hides artificial function arguments `__result__` and `__error__` created by the compiler
- Improved error messages that are clearer and more concise, eliminating unnecessary type expansions

### Documentation Updates [`NEW`]

**Status:** Stable

**Context:**
- New documentation including Mojo tutorial and pages on:
  - Operators and expressions
  - Error handling
  - Pointers
  - Enhanced API documentation display

## Argument Exclusivity

**Status:** Stable

**Context:**
- Mojo 24.6 enforces strict argument exclusivity at compile time
- Prevents passing the same mutable reference to multiple parameters
- Helps prevent potential data races and ensures memory safety

**Usage Example:**
```mojo
# This will fail with error because it tries to pass the same mutable reference twice
pick_longer(manager.get_task(0), manager.get_task(0))

# Error: argument of 'pick_longer' call allows writing a memory location
# previously writable through another aliased argument
```

## Breaking Changes

- Implicit conversions now require explicit opt-in with `@implicit` decorator
- `Lifetime` and related types renamed to `Origin`
- `__lifetime_of()` operator renamed to `__origin_of()`
- `Formatter` struct replaced with `Writer` trait
- `Formattable` trait renamed to `Writable`

## Community Contributions

Mojo v24.6 includes significant contributions from 11 community contributors who provided new features, bug fixes, documentation enhancements, and code refactoring:

@jjvraw, @artemiogr97, @martinvuyk, @jayzhan211, @bgreni, @mzaks, @msaelices, @rd4com, @jiex-liu, @kszucs, @thatstoasty
