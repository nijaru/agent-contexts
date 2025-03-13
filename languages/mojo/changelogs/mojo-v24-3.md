# Mojo v24.3 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v24.3
RELEASED: 2024-05-02
COMPATIBILITY: Backwards compatible with API changes
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v243-2024-05-02
```

## Conceptual Overview
- **Unsafe Pointer Unification**: `AnyPointer` renamed to `UnsafePointer` with enhanced capabilities and consistent API
- **Variadic Arguments**: Improved support for heterogeneous variadic arguments and optional parameters
- **Standard Library Cleanup**: Many APIs made more consistent with Pythonic naming conventions
- **Debugging Support**: Added `-g` option as a shorter alias for `--debug-level full`
- **Package Compilation**: Improved `mojo package` command produces more portable packages

## Core Language

### Variadic and Optional Arguments [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo now supports functions with both optional and variadic arguments
- Works with both positional and keyword-only arguments
- Supports optional parameters alongside variadic parameters

**Usage Example:**
```mojo
fn variadic_arg_after_default(
  a: Int, b: Int = 3, *args: Int, c: Int, d: Int = 1, **kwargs: Int
): ...

fn variadic_param_after_default[e: Int, f: Int = 2, *params: Int]():
  pass
```

**Edge Cases and Anti-patterns:**
- Variadic keyword parameters (`**kwargs`) are not fully supported yet
- Parameter names in variadic pack arguments must match exactly

### UnsafePointer Type [`STABLE`]

**Package:** `memory.unsafe_pointer`
**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes (renamed from AnyPointer)

**Context:**
- `AnyPointer` renamed to `UnsafePointer` and is now Mojo's preferred unsafe pointer type
- The element type can now be any type (doesn't require `Movable`)
- Pointer operations moved to top-level functions and renamed for clarity:
  - `take_value()` → `move_from_pointee()`
  - `emplace_value()` → `initialize_pointee_move()` and `initialize_pointee_copy()`
  - `move_into()` → `move_pointee()`
- New `destroy_pointee()` function for running destructor on the pointee
- Direct initialization from `Reference` with `UnsafePointer(someRef)`
- Conversion to a reference with `yourPointer[]`

**Usage Example:**
```mojo
var ptr = UnsafePointer[Int].alloc(1)
initialize_pointee_copy(ptr, 42)  # Initialize memory with a value
print(ptr[])  # Access value through reference
var value = move_from_pointee(ptr)  # Take value out of memory
destroy_pointee(ptr)  # Run destructor (not needed for Int but shown for completeness)
ptr.free()  # Free allocated memory
```

**Migration:**
```mojo
# Before
var ptr = AnyPointer[Int].alloc(1)
ptr.emplace_value(42)
val = ptr.take_value()
ptr.free()

# After
var ptr = UnsafePointer[Int].alloc(1)
initialize_pointee_copy(ptr, 42)
val = move_from_pointee(ptr)
ptr.free()
```

### Variadic Pack Improvements [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- Heterogeneous variadic pack arguments now work reliably with memory types
- Defined by the `VariadicPack` type with a more convenient API
- Simplifies implementing functions with variable arguments

**Usage Example:**
```mojo
fn print[T: Stringable, *Ts: Stringable](first: T, *rest: *Ts):
    print_string(str(first))

    @parameter
    fn print_elt[T: Stringable](a: T):
        print_string(" ")
        print_string(str(a))
    rest.each[print_elt]()
```

**Edge Cases and Anti-patterns:**
- Heterogeneous variadic arguments require slightly different syntax than homogeneous ones
- Extra care needed when moving values from variadic packs

### Register-passable Initializer Updates [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- Initializers for `@register_passable` values can (and should) now use `inout self` arguments 
- Makes language more consistent, more similar to Python
- No performance impact as compiler arranges to return in a register automatically
- Required for initializers that may raise errors

**Usage Example:**
```mojo
@register_passable
struct YourPair:
    var a: Int
    var b: Int
    
    fn __init__(inout self):
        self.a = 42
        self.b = 17
        
    fn __copyinit__(inout self, existing: Self):
        self.a = existing.a
        self.b = existing.b
```

**Migration:**
```mojo
# Before: returning Self
fn __init__(a: Int, b: Int) -> Self:
    return Self {a: a, b: b}

# After: modifying self directly
fn __init__(inout self, a: Int, b: Int):
    self.a = a
    self.b = b
```

## Standard Library

### Vector Additions [`STABLE`]

**Package:** `collections.list`
**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- New constructor `List(ptr, size, capacity)` to avoid deep copying when constructing from existing memory
- Added `resize(new_size)` for resizing lists without specifying a value
- Added `insert(index, value)` for inserting at a specified position
- Added `pop(index)` for removing an element at a specific index

**Usage Example:**
```mojo
var list = List[Int](1, 2, 3)
list.insert(1, 42)  # list now contains [1, 42, 2, 3]
list.resize(3)  # list now contains [1, 42, 2]
print(list.pop(0))  # Prints 1, list now contains [42, 2]
```

### Dictionary and Set Enhancements [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- `Dict` now has an `update()` method to update from another `Dict`
- `Set` now has named methods for set operations:
  - `difference()` mapping to `-`
  - `difference_update()` mapping to `-=`
  - `intersection_update()` mapping to `&=`
  - `update()` mapping to `|=`
- Collections now conform to the `Boolable` trait (evaluate to `True` if they contain elements)

**Usage Example:**
```mojo
var set1 = Set[Int](1, 2, 3)
var set2 = Set[Int](3, 4, 5)
set1.difference_update(set2)  # set1 now contains {1, 2}

var dict1 = Dict[String, Int]()
dict1["a"] = 1
var dict2 = Dict[String, Int]()
dict2["b"] = 2
dict1.update(dict2)  # dict1 now contains {"a": 1, "b": 2}

def list_names(names: List[String]):
    if names:  # Evaluates to True if names contains any elements
        for name in names:
            print(name[])
    else:
        print("No names to list.")
```

### Optional Enhancements [`STABLE`]

**Package:** `collections.optional`
**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes (for value())

**Context:**
- `Optional` now implements `__is__` and `__isnot__` for comparison with `None`
- `Optional.value()` now returns a reference instead of a copy of the contained value
- To perform a copy manually, dereference the result: `var value = result.value()[]`

**Usage Example:**
```mojo
var opt = Optional(1)
if opt is not None:
    print(opt.value()[])  # Dereference to get the value
```

**Migration:**
```mojo
# Before
var val = opt.value()  # Returns a copy

# After
var val = opt.value()[]  # Dereference to get a copy
```

### Reversed Iterator Function [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- Added the `reversed()` function for creating reversed iterators
- Works with range types, `List`, and `Dict` iterators

**Usage Example:**
```mojo
var numbers = List(1, 2, 3, 4, 5)
for number in reversed(numbers):
    print(number)  # Prints 5, 4, 3, 2, 1
```

### File Handling Improvements [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `FileHandle.seek()` with `whence` argument defaulting to `os.SEEK_SET`
- `FileHandle.read()` can now read into a `DTypePointer`
- Added new `sys.exit()` function to exit a program with a specified error code

**Usage Example:**
```mojo
var file = open("/tmp/example.txt", "r")
# Skip 32 bytes
file.seek(os.SEEK_CUR, 32)
# Start from 32 bytes before the end of the file
file.seek(os.SEEK_END, -32)

# Read into a pointer
var ptr = DTypePointer[DType.float32].alloc(8)
var bytes = file.read(ptr, 8)
print("bytes read", bytes)
```

### Tensor and Buffer Changes [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes (for parameter order)

**Context:**
- `NDBuffer` and `Buffer` constructors changed for consistency
- The parameters are now `[type, size]` instead of `[size, type]`
- Default sizes for certain types make code more concise
- `Tensor` constructor parameters changed and now broadcasts scalar values

**Usage Example:**
```mojo
# Before
var buffer = NDBuffer[3, DType.float32]()

# After 
var buffer = NDBuffer[DType.float32, 3]()
var buffer_default_dims = NDBuffer[DType.float32]()  # Uses default dimensions

# Initialize all elements with a value
var tensor = Tensor[DType.float32](TensorShape(2, 2), 0)  # All zeros
```

### Additional Standard Library Changes [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes (renamed modules)

**Context:**
- Added architecture-specific APIs for querying hardware features
- `SIMD` type now defaults to architectural SIMD width
- New `SIMD.join()` function for concatenating SIMD values

**Usage Example:**
```mojo
# Use default architectural width
var vector = SIMD[DType.float32]()  

# Join two SIMD vectors
var v1 = SIMD[DType.int32, 2](1, 2)
var v2 = SIMD[DType.int32, 2](3, 4)
var joined = v1.join(v2)  # [1, 2, 3, 4]
```

## Module Reorganization [`BREAKING`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes

**Context:**
- Major package reorganization for clarity and future growth:
  - `Buffer` and related types moved from `memory` to `buffer` package
  - `utils.list` (including `Dim` and `DimList`) moved to `buffer`
  - `parallel_memcpy()` moved from `memory` to `buffer`
  - `rand()` and `randn()` functions for Tensors moved to `tensor` package
  - `trap()` renamed to `abort()` and moved from `debug` to `os`
  - `isinf()` and `isfinite()` moved from `math.limits` to `math`

**Migration:**
```mojo
# Before
from memory import Buffer, NDBuffer, parallel_memcpy
from utils.list import Dim, DimList
from debug import trap
from math.limits import isinf, isfinite

# After
from buffer import Buffer, NDBuffer, parallel_memcpy, Dim, DimList
from os import abort  # trap() is now abort()
from math import isinf, isfinite
```

## Tooling Changes

### Mojo Build Command [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes

**Context:**
- The behavior of `mojo build` without an output `-o` argument has changed
- `mojo build ./test-dir/program.mojo` now outputs to `./program` (used to be `./test-dir/program`)
- Added `-g` option as a shorter alias for `--debug-level full`

**Usage Example:**
```bash
# Equivalent commands
mojo build -g my_program.mojo
mojo build --debug-level full my_program.mojo
```

### Package Command [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** Yes

**Context:**
- `mojo package` now produces compilation-agnostic packages
- No longer requires or accepts compilation options like O0 or --debug-level
- Packages are now smaller and more portable
- The `-D` flag is no longer supported for the package command

**Usage Example:**
```bash
# Now produces a more portable package
mojo package my_package -o my_package.mojopkg
```

### REPL Enhancement [`STABLE`]

**Available Since:** `v24.3`
**Status:** Stable
**Breaking:** No

**Context:**
- Limited scope variable handling has been improved
- No longer allows unitialized type level variables
- Provides better lifetime tracking across REPL cells

## Removed Features

### Register-only Variadic Packs [`REMOVED`]

**Available Since:** `v24.3`
**Status:** Removed
**Breaking:** Yes

**Context:**
- Support for "register only" variadic packs has been removed
- Use `AnyType` instead of `AnyRegType` for broader compatibility

**Migration:**
```mojo
# Before
fn your_function[*Types: AnyRegType](*args: *Ts): ...

# After
fn your_function[*Types: AnyType](*args: *Ts): ...
```

### Other Removals [`REMOVED`]

**Available Since:** `v24.3`
**Status:** Removed
**Breaking:** Yes

**Context:**
- `List.pop_back()` removed - use `List.pop()` instead
- `SIMD.to_int(value)` removed - use `int(value)` instead
- `__get_lvalue_as_address(x)` magic function removed - use `Reference(x)` or `UnsafePointer.address_of(x)`

## Fixed Issues

- Fixed issues with functions returning two strings
- Fixed os/kern failure (5)
- Fixed alias with `DynamicVector[Tuple[Int]]`
- Fixed clearer error when defining `main` in a Mojo package
- Fixed LSP hover previews for functions with functional arguments
- Fixed Mojo LSP handling of inout arguments
- Fixed JIT debugging on Mac
- Fixed issues with variadic arguments and non-trivial register-only types
