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

- VS Code extension now supports setting data breakpoints and function breakpoints
- Mojo LLDB debugger supports symbol breakpoints (e.g., `b main` or `b my_module::main`)
- Various improvements to information display in error messages, LSP, and API documentation
- New documentation including Mojo tutorial, pages on operators and expressions, error handling, and pointers

## Breaking Changes

- Implicit conversions now require explicit opt-in with `@implicit` decorator
- `Lifetime` and related types renamed to `Origin`
- `__lifetime_of()` operator renamed to `__origin_of()`
- `Formatter` struct replaced with `Writer` trait
- `Formattable` trait renamed to `Writable`
