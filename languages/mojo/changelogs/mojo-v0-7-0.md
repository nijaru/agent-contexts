# Mojo v0.7.0 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v0.7.0
RELEASED: 2023-10-05
COMPATIBILITY: Some breaking changes from v0.6.x
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v070-2023-10-05
```

## Conceptual Overview
- **Parameter Values in Functions**: Call functions in parameter context to evaluate them at compile time
- **Variable Scope Improvements**: Introduced `let` declarations for local runtime constants in functions
- **Dictionary Type**: Added a new Mojo-native dictionary type for key-value pairs
- **File I/O**: Introduced basic file I/O support with Python-like interface
- **Parameterization Improvements**: Expanded parameter deduction and struct deduction capabilities

## Core Language

### Parameter Function Calls [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Functions can now be called in a parameter context to be evaluated at compile time
- The result can be used as parameter values for other declarations
- Enables more powerful compile-time programming

**Usage Example:**
```mojo
fn fma(x: Int, y: Int, z: Int) -> Int:
    return x + y * z

fn parameter_call():
    alias nelts = fma(32, 2, 16)  # Evaluated at compile time
    var x: SIMD[f32, nelts]  # x is a SIMD vector with 80 elements
```

### Let Declarations [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `let` declarations for local run-time constant values that are always rvalues
- Complement `var` declarations (which are mutable lvalues)
- Generate less IR and are always in SSA form when initialized
- Cannot be mutated after initialization

**Usage Example:**
```mojo
fn example():
    let x = 42  # Immutable
    var y = 10  # Mutable
    y += 5
    print(x + y)  # Prints 57
```

### String Indexing and Slicing [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `String` now supports indexing with integers or slices
- Makes string manipulation more Python-like
- Added utilities for base64 encoding

**Usage Example:**
```mojo
var s = "Hello, Mojo!"
print(s[0])       # Prints 'H'
print(s[7:11])    # Prints 'Mojo'
```

### File I/O Support [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Added basic file I/O with the `file` module
- Python-like open/read/write/close operations
- Context manager support with `with` statements

**Usage Example:**
```mojo
var f = open("my_file.txt", "r")
print(f.read())
f.close()

# Or using context manager
with open("my_file.txt", "r") as f:
    print(f.read())
```

### Path Module [`PREVIEW`]

**Available Since:** `v0.7.0`
**Status:** Preview
**Breaking:** No

**Context:**
- Basic implementation of `pathlib` functionality
- Provides path manipulation and filesystem operations
- Will be expanded in future releases

**Usage Example:**
```mojo
from pathlib import Path

var p = Path("/tmp/example.txt")
print(p.suffix())  # Prints '.txt'
```

### Automatic Struct Parameter Deduction [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Struct parameter deduction for partially bound types
- Works with static methods
- Simplifies working with parameterized types

**Usage Example:**
```mojo
@value
struct Thing[v: Int]: pass

struct CtadStructWithDefault[a: Int, b: Int, c: Int = 8]:
    fn __init__(inout self, x: Thing[a]):
        print("hello", a, b, c)

    @staticmethod
    fn foo(x: Thing[a]):
        print("🔥", a, b, c)

fn main():
    _ = CtadStructWithDefault[b=7](Thing[6]())  # prints 'hello 6 7 8'
    CtadStructWithDefault[b=7].foo(Thing[6]())  # prints '🔥 6 7 8'
```

## Standard Library

### Dict Type [`STABLE`]

**Package:** `collections.dict`
**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- New Mojo-native dictionary type for storing key-value pairs
- Stores values conforming to `CollectionElement` trait
- Keys need to conform to the `KeyElement` trait
- Fast lookups, insertions, and deletions

**Usage Example:**
```mojo
from collections.dict import Dict, KeyElement

@value
struct StringKey(KeyElement):
    var s: String

    fn __init__(inout self, owned s: String):
        self.s = s^

    fn __init__(inout self, s: StringLiteral):
        self.s = String(s)

    fn __hash__(self) -> Int:
        return hash(self.s)

    fn __eq__(self, other: Self) -> Bool:
        return self.s == other.s

fn main() raises:
    var d = Dict[StringKey, Int]()
    d["cats"] = 1
    d["dogs"] = 2
    print(len(d))         # prints 2
    print(d["cats"])      # prints 1
    print(d.pop("dogs"))  # prints 2
    print(len(d))         # prints 1
```

### Memory Features [`STABLE`]

**Package:** `memory.unsafe`
**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `bitcast` function for low-level operations
- Enables type conversions between pointers and scalars

**Usage Example:**
```mojo
from memory.unsafe import bitcast

var i: Int = 42
var ptr = bitcast[UnsafePointer[Int]](i)
```

### Parameter Access in Types [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Input parameters of parametric types can be directly accessed as attributes
- Works on both the type and instances of the type
- Parameters can be accessed in parameter contexts

**Usage Example:**
```mojo
@value
struct Thing[param: Int]:
    pass

fn main():
    print(Thing[2].param)  # prints '2'
    let x = Thing[9]()
    print(x.param)  # prints '9'
    
    alias constant = x.param + 4
    fn foo[value: Int]():
        print(value)
    foo[constant]()  # prints '13'
```

### Tensor Improvements [`STABLE`]

**Package:** `tensor`
**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `Tensor` now has `save()` and `load()` methods for serialization
- Preserves shape and datatype information
- Added `fromfile()` and `tofile()` methods for binary data

**Usage Example:**
```mojo
let tensor = Tensor[DType.float32]()
# ... populate tensor
tensor.save("tensor.dat")

let tensor_from_file = Tensor[DType.float32].load("tensor.dat")
```

## Tooling

### REPL Enhancements [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- REPL now supports code completion (press Tab while typing)
- Error messages from Python are now exposed in Mojo

**Usage Example:**
```mojo
fn main():
    try:
        let my_module = Python.import_module("my_uninstalled_module")
    except e:
        print(e)  # Prints "No module named 'my_uninstalled_module'"
```

### Error Messages [`STABLE`]

**Available Since:** `v0.7.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Error messages can now store dynamic messages
- Improved error handling and reporting

**Usage Example:**
```mojo
fn foo(x: String) raises:
    raise Error("Failed on: " + x)

fn main():
    try:
        foo("Hello")
    except e:
        print(e)  # Prints "Failed on: Hello"
```

## Breaking Changes

### __moveinit__ Renamed to __takeinit__ [`BREAKING`]

**Available Since:** `v0.7.0`
**Status:** Changed
**Breaking:** Yes

**Context:**
- The second form of move constructor has been renamed from `__moveinit__` to `__takeinit__`
- Makes it clear that these are two separate operations
- The name connotes taking a value conceptually without destroying it

**Migration:**
```mojo
# Before
fn __moveinit__(inout self, inout existing: Self): ...

# After
fn __takeinit__(inout self, inout existing: Self): ...
```

### Error Type Changes [`BREAKING`]

**Available Since:** `v0.7.0`
**Status:** Changed
**Breaking:** Yes

**Context:**
- Error type in Mojo has changed
- Use `error.message()` instead of `error.value` to extract error messages

**Migration:**
```mojo
# Before
try:
    raise Error("oops")
except err:
    print(err.value)

# After
try:
    raise Error("oops")
except err:
    print(err.message())
```

## Fixed Issues

- Improved error message for failure lowering `kgen.param.constant`
- Fixed aliases of static tuples failing to expand
- Fixed call expansion failures
- Fixed incorrect comment detection in multiline strings
- Fixed initialization errors of VS Code extension
- Fixed building LLDB/REPL with libedit for better editing experience
