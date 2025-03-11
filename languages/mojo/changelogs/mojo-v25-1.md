# Mojo Version 25.1 Changelog Documentation

```
TITLE: Mojo Programming Language - Version 25.1
VERSION: 25.1
RELEASED: 2025-02-13
COMPATIBILITY: Compatible with previous versions, with some deprecated features
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/
```

## Conceptual Overview

- Mojo now supports GPU programming through the new `gpu` and `layout` packages, enabling developers to manage interactions between CPU host and GPU device
- Legacy argument conventions (`borrowed`/`inout`) and type conversion functions (`bool()`, `float()`, `int()`, `str()`) are deprecated in favor of new syntax
- Major string handling improvements including a new `Char` struct for Unicode characters and replacement of `StringRef` with `StringSlice`
- Enhanced SIMD capabilities with improved constructors for casting between different types

## Core Language

### Argument Convention System [`CHANGED`]

**Status:** Stable
**Breaking:** No (Deprecation warnings only in this version)

**Context:**
- The legacy `borrowed`/`inout` keywords and `-> T as foo` syntax now generate compiler warnings
- Developers should migrate to `read`/`mut`/`out` argument syntax instead

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

### Constructor Behavior [`CHANGED`]

**Status:** Stable
**Breaking:** Yes

**Context:**
- Initializers are now treated as static methods that return an instance of `Self`
- The `out` argument of an initializer is treated the same as any other function result or `out` argument

**Migration:**
```mojo
// BEFORE:
instance.__init__()
x.__copyinit__(y)

// AFTER:
instance = T()
x = y
```

**Migration Difficulty:** Simple

### Overloaded Keyword Arguments [`NEW`]

**Status:** Stable

**Signature:**
```mojo
struct Example:
    var val: Int

    fn __init__(out self, single: Int):
        self.val = single

    fn __init__(out self, *, double: Int):
        self.val = double * 2
```

**Usage Example:**
```mojo
Example(1)        # val=1
Example(double=1) # val=2
```

**Context:**
- You can now overload positional arguments with keyword-only arguments
- This also works with indexing operations

## Standard Library

### Type Conversion Functions [`DEPRECATED`]

**Status:** Deprecated
**Breaking:** No (Deprecation warnings only in this version)

**Context:**
- The following functions are deprecated in favor of constructors:

| **Before** | **After** |
| --- | --- |
| `bool()` | `Bool()` |
| `float()` | `Float64()` |
| `int()` | `Int()` |
| `str()` | `String()` |

**Migration Difficulty:** Simple - search and replace can update most occurrences

### Char Type [`NEW`]

**Package:** `builtin.char`
**Status:** Stable

**Signature:**
```mojo
struct Char:
    # Numerous methods for character type checking
    fn is_ascii(self) -> Bool: ...
    fn is_ascii_digit(self) -> Bool: ...
    fn is_ascii_upper(self) -> Bool: ...
    fn is_ascii_lower(self) -> Bool: ...
    fn is_ascii_printable(self) -> Bool: ...
    fn is_posix_space(self) -> Bool: ...
    fn is_python_space(self) -> Bool: ...
    fn to_u32(self) -> UInt32: ...
```

**Dependencies/Imports:**
```mojo
from builtin.char import Char
```

**Context:**
- New struct representing a single Unicode character
- Implements `CollectionElement`, `EqualityComparable`, `Intable`, and `Stringable`
- Includes methods for categorizing character types
- Can be converted to/from strings and numeric code points

### String Iteration and Character Handling [`CHANGED`]

**Status:** Stable
**Breaking:** Yes

**Context:**
- When iterating over characters in a `String`, use the new `.chars()` or `.char_slices()` methods instead of the now-deprecated `__iter__()`
- `StringRef` has been removed in favor of `StringSlice`
- `StringSlice` now has more functionality previously found in `String` and `StringLiteral`

**Migration:**
```mojo
// BEFORE:
var s: String = ...
for c in s:
    # ...

// AFTER:
var s: String = ...
for c in s.char_slices():
    # ...
```

**Migration Difficulty:** Medium

### SIMD Type Casting [`IMPROVED`]

**Status:** Stable

**Usage Example:**
```mojo
var val = Int8(42)
var cast = Int32(val)  # Cast to different scalar type

var vector = SIMD[DType.int64, 4](cast)  # [42, 42, 42, 42]
var float_vector = SIMD[DType.float64, 4](vector)  # Cast vector to different type
```

**Context:**
- You can now use SIMD constructors to cast existing SIMD values to different types
- For values other than scalars, the size of the SIMD vector needs to be equal
- `SIMD.cast()` still exists to infer the size of the new vector

## GPU Programming

### GPU Package [`NEW`]

**Package:** `gpu`
**Status:** Stable

**Usage Example:**
```mojo
from max.tensor import ManagedTensorSlice
from gpu import thread_idx, block_dim, block_idx

fn gpu_add_kernel(out: ManagedTensorSlice, x: ManagedTensorSlice[out.type, out.rank]):
    tid_x = thread_idx.x + block_dim.x * block_idx.x
    tid_y = thread_idx.y + block_dim.y * block_dim.y
    if tid_x < x.dim_size(0) and tid_y < x.dim_size(1):
        out[tid_x, tid_y] = x[tid_x, tid_y] + 1
```

**Context:**
- New package for low-level GPU programming
- Allows developers to manually manage interaction between CPU host and GPU device
- Supports memory management between devices and thread synchronization
- Currently best used with MAX custom operations

### Layout Package [`NEW`]

**Package:** `layout`
**Status:** Stable

**Context:**
- Provides APIs for working with layouts that describe tensor organization
- Includes the `LayoutTensor` type for representing tensors with specific layouts
- Can be used to build efficient tensor operations for GPU execution

## Bug Fixes

- Fixed Jupyter Notebook Mojo Kernel for nightly releases
- Fixed VSCode debugging working directory with `mojo debug --vscode`
- Fixed compiler crash handling `for`-`else` statement (Issue #3796)
- Fixed bug where named output slots broke trait conformance (Issue #3540)
- Fixed type constructors for wrapped literal references (Issue #3617)
- Fixed Mojo Language Server crash on empty `__init__.mojo` files (Issue #3826)
- Fixed confusing OOM error when using `Tuple.get()` incorrectly (Issue #3935)
- Fixed unexpected copy behavior with `def` arguments in loops (Issue #3955)
- Fixed infinite `for` loop issue (Issue #3960)

## Removed/Deprecated Features

- `StringRef` has been removed - use `StringSlice` instead
- `Tuple.get[i, T]()` method has been removed - use `tup[i]` or `rebind[T](tup[i])` instead
- `StringableCollectionElement` is deprecated - use `WritableCollectionElement` instead
- `IntLike` trait has been removed - functionality incorporated into `Indexer` trait
- The `Type{field1: 42, field2: 17}` syntax for direct initializing register passable types has been removed
