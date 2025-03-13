# Mojo v0.6.1 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v0.6.1
RELEASED: 2023-12-18
COMPATIBILITY: Backwards compatible with v0.6.0
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v061-2023-12-18
```

## Conceptual Overview
- **Value Decorator Enhancements**: Structs decorated with `@value` now automatically conform to `Movable` and `Copyable` traits
- **String Utilities**: New case conversion methods for `String` type
- **Collection Trait Conformance**: Standard library types now conform to `CollectionElement` trait
- **Hashing Support**: Added builtin `hash()` function and `Hashable` trait

## Core Language

### @value Decorator Improvements [`STABLE`]

**Available Since:** `v0.6.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Structs decorated with `@value` now automatically conform to the `Movable` and `Copyable` built-in traits
- Reduces boilerplate by eliminating the need to explicitly declare these trait conformances
- Encourages use of the value semantics pattern

**Usage Example:**
```mojo
@value
struct Point:
    var x: Int
    var y: Int
    
    # No need to explicitly declare Movable and Copyable conformance
    # These initializers are still synthesized automatically:
    # fn __init__(inout self, x: Int, y: Int)
    # fn __copyinit__(inout self, existing: Self)
    # fn __moveinit__(inout self, owned existing: Self)

# Point can be used in containers requiring Movable and Copyable
var points = DynamicVector[Point]()
points.push_back(Point(1, 2))
```

### REPL CD Magic Command [`STABLE`]

**Available Since:** `v0.6.1`
**Status:** Stable
**Breaking:** No

**Context:**
- The Mojo REPL now provides limited support for the `%cd` magic command
- Automatically maintains an internal stack of directories visited during the REPL session
- Makes navigation between directories more convenient during development

**Usage Example:**
```mojo
# Change to a directory and push it on the stack
%cd '/path/to/project'

# Work with files in that directory
import module_from_current_dir

# Return to the previous directory
%cd -
```

## Standard Library

### String Case Methods [`STABLE`]

**Package:** `collections.string`
**Available Since:** `v0.6.1`
**Status:** Stable
**Breaking:** No

**Context:**
- `String` now has new `toupper()` and `tolower()` methods for case conversion
- Analogous to Python's `str.upper()` and `str.lower()` methods
- Makes string manipulation more convenient

**Usage Example:**
```mojo
var s = "Hello Mojo"
print(s.toupper())  # Prints "HELLO MOJO"
print(s.tolower())  # Prints "hello mojo"
```

### Hashable Trait [`STABLE`]

**Package:** `builtin.hash`
**Available Since:** `v0.6.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Added a `hash()` built-in function and `Hashable` trait for types implementing the `__hash__()` method
- Future releases will add `Hashable` support to more standard library types
- Currently includes a version that works on arbitrary byte strings

**Usage Example:**
```mojo
from builtin.hash import _hash_simd

@value
struct MyHashable(Hashable):
    var id: Int
    
    fn __hash__(self) -> Int:
        return self.id
        
fn gen_simd_hash():
    let vector = SIMD[DType.int64, 4](1, 2, 3, 4)
    let hash_value = _hash_simd(vector)
    print(hash_value)
```

### Collection Element Conformance [`STABLE`]

**Available Since:** `v0.6.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Several standard library types now conform to the `CollectionElement` trait
- These types include `Bool`, `StringLiteral`, `DynamicVector`, `Tensor`, `TensorShape`, and `TensorSpec`
- Enables these types to be stored in collections like `DynamicVector`

**Usage Example:**
```mojo
var vectors = DynamicVector[DynamicVector[Int]]()
var v1 = DynamicVector[Int]()
v1.push_back(1)
v1.push_back(2)
vectors.push_back(v1)  # Now works because DynamicVector conforms to CollectionElement

var shapes = DynamicVector[TensorShape]()
shapes.push_back(TensorShape(2, 3))
```

## Fixed Issues

- Fixed a crash when using Tuples in the REPL
- Fixed error generation for obviously self-recursive functions
- Fixed type inference issues in 'ternary assignment' operations
- Fixed logical operators (`and`/`or`) with memory-only types
- Fixed `setitem` support for `PythonObject`
- Fixed compatibility of function signatures that only differ in default argument values
- Fixed printing of empty `String`
