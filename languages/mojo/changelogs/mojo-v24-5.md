# Mojo v24.5 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v24.5
RELEASED: 2024-09-13
COMPATIBILITY: Python 3.12 interoperability
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v245-2024-09-13
```

## Conceptual Overview
- **Python Interoperability**: Mojo now supports Python 3.12, enhancing integration with the Python ecosystem
- **Reduced Implicit Imports**: Dramatically reduced set of automatically imported entities, requiring explicit imports for previously included types and functions
- **Argument Safety**: New diagnostics for "argument exclusivity" violations to detect and prevent aliasing of mutable references
- **Enhanced Type System**: Added support for "conditional conformances" allowing methods to have additional trait requirements beyond the struct itself
- **Streamlined Pointers**: Consolidated pointer types by removing `DTypePointer`, `LegacyPointer`, and `Pointer` in favor of a unified `UnsafePointer` approach

## Core Language

### Implicit Variable Definition in `fn` [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo now allows implicit definitions of variables within a `fn` in the same way that has been allowed in a `def`
- The `var` keyword is still optional but no longer required
- This makes `fn` and `def` more similar, though they still differ in other important ways like memory control and implicit raising

**Usage Example:**
```mojo
fn example():
    count = 5  # Implicit variable definition, no 'var' needed
    var explicit_count = 10  # Still works with explicit 'var'
```

### Argument Exclusivity [`EXPERIMENTAL`]

**Available Since:** `v24.5`
**Status:** Experimental (Warning in v24.5, will be error in future releases)
**Breaking:** Will be breaking in future releases

**Context:**
- Mojo now diagnoses "argument exclusivity" violations due to aliasing references
- Mojo requires references (including implicit references due to `borrowed`/`inout` arguments) to be uniquely referenced (non-aliased) if mutable
- This is important for code safety and allows the compiler to understand when a value is mutated
- Similar to Swift exclusivity checking and Rust's "aliasing xor mutability" concept

**Usage Example:**
```mojo
fn take_two_strings(a: String, inout b: String):
   # Mojo knows 'a' and 'b' cannot be the same string
   b += a

fn invalid_access():
  var my_string = String()

  # warning: passing `my_string` inout is invalid since it is also passed borrowed
  take_two_strings(my_string, my_string)
```

**Edge Cases and Anti-patterns:**
- Argument exclusivity is not enforced for register-passable types since they are passed by copy
- The compiler will warn about exclusivity violations in v24.5, but these will become errors in future releases

### Conditional Conformances [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
struct GenericThing[Type: AnyType]:  # Works with anything
  # Sugar for 'fn normal_method[Type: AnyType](self: GenericThing[Type]):'
  fn normal_method(self): ...

  # Just redeclare the requirements with more specific types:
  fn needs_move[Type: Movable](self: GenericThing[Type], owned val: Type):
    var tmp = val^  # Ok to move 'val' since it is Movable
    ...
```

**Context:**
- Allows methods on a struct to have additional trait requirements that the struct itself doesn't
- Expressed through explicitly declared `self` type
- Works with dunder methods and other special methods
- Allows for more flexible API design with trait-specific behavior

**Usage Example:**
```mojo
# Define a generic type with conditional conformance
trait StringableFormattableCollectionElement(Formattable, StringableCollectionElement):
    ...

struct SafeBuffer[T: CollectionElement]:
    var _data: UnsafePointer[Optional[T]]
    var size: Int

    # Only available when T conforms to StringableFormattableCollectionElement
    fn __str__[U: StringableFormattableCollectionElement](self: SafeBuffer[U]) -> String:
        ret = String()
        writer = ret._unsafe_to_formatter()
        self.format_to(writer)
        _ = writer^
        return ret^

    # Format implementation also requires the same conformance
    fn format_to[U: StringableFormattableCollectionElement](
        self: SafeBuffer[U], inout writer: Formatter
    ):
        # Implementation details...

# Usage
fn usage_example():
  var a = GenericThing[Int]()
  a.normal_method() # Ok, Int conforms to AnyType
  a.needs_move(42)  # Ok, Int is movable

  var b = GenericThing[NonMovable]()
  b.normal_method() # Ok, NonMovable conforms to AnyType

  # error: argument type 'NonMovable' does not conform to trait 'Movable'
  b.needs_move(NonMovable())
```

### Parameter-Specific Initializers [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
@value
struct MyStruct[size: Int]:
    fn __init__(inout self: MyStruct[0]): pass
    fn __init__(inout self: MyStruct[1], a: Int): pass
    fn __init__(inout self: MyStruct[2], a: Int, b: Int): pass
```

**Context:**
- Initializers in a struct may indicate specific parameter bindings to use in the type of their `self` argument
- Allows for constructor overloading based on parameterized type values
- Parameter values can be inferred from constructor arguments

**Usage Example:**
```mojo
def test(x: Int):
    a = MyStruct()      # Infers size=0 from 'self' type
    b = MyStruct(x)     # Infers size=1 from 'self' type
    c = MyStruct(x, x)  # Infers size=2 from 'self' type
```

### Named Result Bindings [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
fn efficiently_return_string(b: Bool) -> String as output:
    if b:
        output = "emplaced!"
        mutate(output)
        return
    return "regular return"
```

**Context:**
- Named result bindings are useful for directly emplacing function results into the output slot of a function
- Provides more flexibility and guarantees around emplacing the result compared to "guaranteed" named return value optimization (NRVO)
- If a `@register_passable` result is bound to a name, the result value is made accessible as a mutable reference
- Enables more efficient return values, especially for non-movable types

**Usage Example:**
```mojo
# Factory method using named result binding
@staticmethod
fn initialize_with_value(size: Int, value: T) -> Self as output:
    output = SafeBuffer(size)
    for i in range(size):
        output.write(i, value)
    return  # No value needed, as 'output' is already initialized
```

**Edge Cases and Anti-patterns:**
- In a function with a named result, `return` may be used with no operand to signal an exit, or it can be used normally to specify the return value
- The compiler will error if the result is not initialized on all normal exit paths

### Variadic Argument `__setitem__` [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
struct YourType:
    fn __setitem__(inout self, *indices: Int, val: Int): ...
```

**Context:**
- `__setitem__()` now works with variadic argument lists
- The Mojo compiler always passes the "new value" being set using the last keyword argument
- Enables multi-dimensional indexing for container types

**Usage Example:**
```mojo
# yourType[1, 2] = 3 turns into:
yourType.__setitem__(1, 2, val=3)
```

### Context Managers without Conditional Exit [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- Context managers used in regions of code that may raise no longer need to define a "conditional" exit function in the form of `fn __exit__(self, e: Error) -> Bool`
- Enables defining `with` regions that unconditionally propagate inner errors
- Simplifies many common context manager use cases

**Usage Example:**
```mojo
def might_raise() -> Int:
    ...

def foo() -> Int:
    with ContextMgr():
        return might_raise()
    # no longer complains about missing return

def bar():
    var x: Int
    with ContextMgr():
        x = might_raise()
    print(x) # no longer complains about 'x' being uninitialized
```

### Async Functions with Memory-Only Results [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
async fn raise_or_string(c: Bool) raises -> String:
    if c:
        raise "whoops!"
    return "hello world!"
```

**Context:**
- `async` functions now support memory-only results (like `String`, `List`, etc.) and `raises`
- Both `Coroutine` and `RaisingCoroutine` have been changed to accept `AnyType` instead of `AnyTrivialRegType`
- Result types of `async` functions do not need to be `Movable`

**Edge Cases and Anti-patterns:**
- `async` functions do not yet support indirect calls, `ref` results, and constructors

## Standard Library

### Reduced Automatic Imports [`BREAKING`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** Yes

**Context:**
- The set of automatically imported entities (types, aliases, functions) has been dramatically reduced
- Previously, all entities in modules like `memory`, `sys`, `os`, `utils`, `python`, `bit`, `random`, `math`, `builtin`, `collections` were automatically included
- Now, only explicitly enumerated entities in `prelude/__init__.mojo` are automatically imported
- Will break existing code that relies on automatic imports

**Migration:**
```mojo
# BEFORE:
var opt = Optional(42)  # Worked without import

# AFTER:
from collections import Optional
var opt = Optional(42)  # Now requires explicit import
```

**Migration Difficulty:** Medium - requires adding explicit imports for previously automatic imports

### `input()` Function [`STABLE`]

**Package:** `builtin.io`
**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
fn input(prompt: String = "") -> String
```

**Context:**
- Behaves the same as Python's input function
- Prints an optional prompt and reads a line from standard input
- Returns the input as a String

**Usage Example:**
```mojo
name = input("Enter your name: ")
print("Hello, " + name + "!")
```

**Edge Cases and Anti-patterns:**
- Known issue when running the `input()` function with JIT compilation (issue #3479)

### `print()` with `Formattable` [`BREAKING`]

**Package:** `builtin.io`
**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** Yes

**Context:**
- `print()` now requires that its arguments conform to the `Formattable` trait
- Enables efficient stream-based writing by default, avoiding unnecessary intermediate String heap allocations
- Previously, `print()` required types to conform to `Stringable`

**Migration:**
```mojo
# BEFORE:
struct Point(Stringable):
    var x: Float64
    var y: Float64

    fn __str__(self) -> String:
        # Performs 3 allocations: 1 each for str(..) of each fields,
        # and then the final returned `String` allocation
        return "(" + str(self.x) + ", " + str(self.y) + ")"

# AFTER:
struct Point(Stringable, Formattable):
    var x: Float64
    var y: Float64

    fn __str__(self) -> String:
        return String.format_sequence(self)

    fn format_to(self, inout writer: Formatter):
        writer.write("(", self.x, ", ", self.y, ")")
```

**Migration Difficulty:** Medium - requires implementing the `Formattable` trait for custom types

### `UnsafePointer` Consolidation [`BREAKING`]

**Package:** `memory.unsafe_pointer`
**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** Yes

**Context:**
- `DTypePointer`, `LegacyPointer`, and `Pointer` have been removed - use `UnsafePointer` instead
- Consolidates pointer types for more consistent memory management
- Functions that previously took a `DTypePointer` now take an equivalent `UnsafePointer`
- Simplifies the pointer system while retaining all necessary capabilities

**Migration:**
```mojo
# BEFORE:
DTypePointer[type]

# AFTER:
UnsafePointer[Scalar[type]]
```

**Migration Difficulty:** Medium - requires updating types and potentially adding infer-only parameters

### Pointer Method Transitions [`BREAKING`]

**Package:** `memory.unsafe_pointer`
**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** Yes

**Context:**
- Global functions for working with pointers have transitioned to being methods on `UnsafePointer`
- Improves code organization and follows object-oriented design principles

**Migration:**
```mojo
# BEFORE:
destroy_pointee(p)
move_from_pointee(p)
initialize_pointee_move(p, value)
initialize_pointee_copy(p, value)
move_pointee(src=p1, dst=p2)

# AFTER:
p.destroy_pointee()
p.take_pointee()
p.init_pointee_move(value)
p.init_pointee_copy(value)
p.move_pointee_into(p2)
```

**Migration Difficulty:** Simple - requires changing function call style

### String and Collections Updates [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- The `String` class now has `rjust()`, `ljust()`, and `center()` methods
- Added the `String.format()` method supporting automatic and manual indexing of `*args`
- `List` values are now equality comparable with `==` and `!=` when their element type is equality comparable
- `Optional` values are now equality comparable with `==` and `!=` when their element type is equality comparable
- Added a new `Counter` dictionary-like type, matching most of the features of the Python one
- `Dict` now implements `setdefault()` and `popitem()`
- Added a `Dict.__init__()` overload to specify initial capacity
- `ListLiteral` now supports `__contains__()`

**Usage Example:**
```mojo
# String formatting
print(String("{1} Welcome to {0} {1}").format("mojo", "🔥"))
# 🔥 Welcome to mojo 🔥

print(String("{} {} {}").format(True, 1.125, 2))
# True 1.125 2

# String conversion flags
String("{} {!r}").format("Mojo", "Mojo")
# "Mojo 'Mojo'"
```

### Filesystem and Environment Utilities [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `Path.home()` to return a path of the user's home directory
- Added `os.path.expanduser()` and `pathlib.Path.expanduser()` to allow expanding a prefixed `~` in paths
- Added `os.path.split()` for splitting a path into `head, tail`
- Added `os.makedirs()` and `os.removedirs()` for creating and removing nested directories
- Added the `pwd` module for accessing user information in `/etc/passwd` on POSIX systems

**Usage Example:**
```mojo
import os
print(os.path.expanduser("~/.modular"))
# /Users/username/.modular

head, tail = os.path.split("/this/is/head/tail")
print("head:", head)
print("tail:", tail)
# head: /this/is/head
# tail: tail

import pwd
current_user = pwd.getpwuid(os.getuid())
print(current_user)
# pwd.struct_passwd(pw_name='jack', pw_passwd='********', pw_uid=501,
# pw_gid=20, pw_gecos='Jack Clayton', pw_dir='/Users/jack',
# pw_shell='/bin/zsh')
```

### Python Interoperability Improvements [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo now supports Python 3.12 interoperability
- Creating a nested `PythonObject` from a list or tuple of Python objects is now possible
- Accessing local Python modules with `Python.add_to_path(".")` is no longer required - behaves the same as Python

**Usage Example:**
```mojo
var np = Python.import_module("numpy")
var a = np.array([1, 2, 3])
var b = np.array([4, 5, 6])
var arrays = PythonObject([a, b])
assert_equal(len(arrays), 2)

var stacked = np.hstack((a, b))
assert_equal(str(stacked), "[1 2 3 4 5 6]")
```

### New Traits and Types [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- Added the `ExplicitlyCopyable` trait to mark types that can be copied explicitly
- Added the `Identifiable` trait for types implementing `__is__()` and `__isnot__()`
- Types conforming to `Boolable` no longer implicitly convert to `Bool`
- Added `ImplicitlyBoolable` trait for types where implicit Bool conversion is desired
- Added a `UInt` type for modeling unsigned integers with a platform-dependent width
- Added `c_char` type alias in `sys.ffi`

### Miscellaneous Standard Library Updates [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- `sort()` now supports a `stable` parameter
- Added the `oct()` builtin function for formatting an integer in octal
- Added `assert_is()` and `assert_is_not()` test functions to the `testing` module
- The `math` package now includes the `pi`, `e`, and `tau` constants
- The `ulp` function from `numerics` has been moved to the `math` module
- `bit` module now supports `bit_reverse()`, `byte_swap()`, and `pop_count()` for the `Int` type
- Renamed bit functions for clarity: `countl_zero()` -> `count_leading_zeros()` and `countr_zero()` -> `count_trailing_zeros()`
- `Slice` now uses `OptionalReg[Int]` for `start` and `end`

**Usage Example:**
```mojo
# Stable sort
sort[cmp_fn, stable=True](list)

# Octal formatting
oct(42)  # "0o52"
```

## Tooling

### Mojo Test Improvements [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- `mojo test` now uses the Mojo compiler for running unit tests
- Resolves compilation issues and improves overall test times
- Now accepts a `--filter` option to narrow the set of tests
- Supports the same compilation options as `mojo build`
- Supports debugging unit tests with the `--debug` flag

**Usage Example:**
```bash
# Run tests matching a pattern
mojo test --filter "test_string.*"

# Debug tests
mojo test --debug
```

**Migration Tip:**
Add a testing task to your `mojoproject.toml` for easier test running:
```toml
[tasks]
test = "mojo test test_*.mojo"
```

### VS Code Support [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- The VS Code extension now supports a vendored MAX SDK
- Automatically downloaded by the extension
- Used for all Mojo features including Language Server, debugger, and formatter
- Added a proxy to the Language Server that handles crashes more gracefully
- Mojo Language Server no longer sets `.` as a commit character for auto-completion

### Mojo Debugger Updates [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- The `mojo debug --rpc` command has been renamed to `mojo debug --vscode`
- Now able to manage multiple VS Code windows
- Supports a `break-on-raise` command to stop at any `raise` statements
- Hides artificial function arguments `__result__` and `__error__` created by the compiler

### Environment Variable `MOJO_PYTHON` [`STABLE`]

**Available Since:** `v24.5`
**Status:** Stable
**Breaking:** No

**Context:**
- The environment variable `MOJO_PYTHON` can be pointed to an executable to pin Mojo to a specific version
- Or a virtual environment to always have access to those Python modules
- `MOJO_PYTHON_LIBRARY` still exists for environments with a dynamic `libpython` but no Python executable

**Usage Example:**
```bash
export MOJO_PYTHON="/usr/bin/python3.11"
# OR
export MOJO_PYTHON="~/venv/bin/python"
```

## Breaking Changes

### Removed Legacy Initializer Syntax [`BREAKING`]

**Available Since:** `v24.5`
**Status:** Removed
**Breaking:** Yes

**Context:**
- Support for the legacy `fn __init__(...) -> Self:` form has been removed from the compiler

**Migration:**
```mojo
# BEFORE:
fn __init__(...) -> Self:
    ...

# AFTER:
fn __init__(inout self, ...):
    ...
```

**Migration Difficulty:** Simple - requires changing method signature

### Builtin Tensor Module Removed [`BREAKING`]

**Available Since:** `v24.5`
**Status:** Removed
**Breaking:** Yes

**Context:**
- The builtin `tensor` module has been removed
- Identical functionality is available in `max.tensor`
- Generally recommended to use structs from the `buffer` module when possible instead

**Migration:**
```mojo
# BEFORE:
from tensor import Tensor

# AFTER:
from max.tensor import Tensor
# OR (preferred)
from buffer import NDBuffer
```

**Migration Difficulty:** Medium - requires changing imports and potentially adapting to different API

### Pointer Types Removed [`BREAKING`]

**Available Since:** `v24.5`
**Status:** Removed
**Breaking:** Yes

**Context:**
- Removed `DTypePointer`, `LegacyPointer`, and `Pointer`
- Removed various String pointer methods including `String.unsafe_uint8_ptr()`, `StringLiteral.unsafe_uint8_ptr()` and `StringLiteral.as_uint8_ptr()`
- Replaced with `UnsafePointer` for more consistent memory management

**Migration:**
```mojo
# BEFORE:
var ptr = str.unsafe_uint8_ptr()

# AFTER:
var ptr = str.unsafe_ptr()  # Now returns UnsafePointer[UInt8]
```

**Migration Difficulty:** Medium - requires updating code to use new pointer types and methods

### Pointer Aliasing Semantics [`BREAKING`]

**Available Since:** `v24.5`
**Status:** Changed
**Breaking:** Yes

**Context:**
- The pointer aliasing semantics of Mojo have changed
- It is now forbidden to convert a non-pointer-typed value derived from a Mojo-allocated pointer to a pointer-typed value
- The `UnsafePointer` constructor that took an `address` keyword argument has been removed
- Still possible in certain cases for interoperating with other languages like Python

**Migration Difficulty:** Medium to Complex - may require significant restructuring of low-level memory management code

## Fixed Issues

- Fixed a crash in the Mojo Language Server when importing the current file
- Fixed crash when specifying variadic keyword arguments without a type expression in `def` functions
- Mojo now prints `ref` arguments and results in generated documentation correctly
- Fixed issue where calling `__copyinit__` on self causes crash (#1734)
- Fixed confusing `__setitem__` method failure with "must be mutable" error (#3142)
- Fixed incorrect behavior of `SIMD.__int__` on unsigned types (#3065)
- Disabled implicit SIMD conversion routes through `Bool` (#3045)
- Fixed List not working at compile time (#3126)
- Fixed difference between `__getitem__` and `[.]` operator (#3237)
- Fixed outdated references to `let` in REPL documentation (#3336)
- VS Code extension no longer caches the information of the selected MAX SDK
- Mojo debugger now stops showing spurious warnings when parsing closures

## Community Contributions

Mojo v24.5 includes significant contributions from 11 community contributors who provided new features, bug fixes, documentation enhancements, and code refactoring:

@jjvraw, @artemiogr97, @martinvuyk, @jayzhan211, @bgreni, @mzaks, @msaelices, @rd4com, @jiex-liu, @kszucs, @thatstoasty
