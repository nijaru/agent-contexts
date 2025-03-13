# Mojo v24.4 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v24.4
RELEASED: 2024-06-07
COMPATIBILITY: Backwards compatible with some deprecated features
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v244-2024-06-07
```

## Conceptual Overview
- **Function Argument Improvements**: Changed how `def` function arguments are processed for better performance and consistency
- **Standard Library Unification**: Continued unification of standard library APIs around the `UnsafePointer` type
- **Collection Enhancements**: Many quality-of-life improvements for standard library collection types
- **Dictionary Performance**: Significant performance improvements for `Dict` insertions
- **Compile-time Loops**: New `@parameter for` mechanism for expressing compile-time loops, replacing `@unroll`

## Core Language

### `def` Function Argument Processing [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Changed how `def` function arguments are processed for better performance and consistency
- Previously, arguments to `def` were treated with the `owned` convention by default, making a copy and allowing mutation
- Now `def` functions take arguments as `borrowed` by default (consistent with `fn` functions)
- The compiler will make a local copy ONLY if the argument is mutated in the function body
- This improves consistency, performance, and ease of use by eliminating unnecessary copies

**Usage Example:**
```mojo
# Before, this would make a copy of x even if not mutated
def process(x):
    return x + 1

# Now, no copy is made unless x is mutated
def process(x):
    return x + 1  # No copy made

def mutate(x):
    x += 1  # Copy automatically made since x is mutated
    return x
```

### Implicit Variable Definition in a `def` [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Implicit variable definitions in `def` functions are more flexible
- Now supports implicit declaration of variables as the result of a tuple return: `a, b = foo()`
- Implicit variable declarations can now shadow global immutable symbols without generating errors

**Usage Example:**
```mojo
def return_two(i: Int) -> (Int, Int):
    return i, i+1

def main():
    a, b = return_two(5)  # a=5, b=6
    
    # This now works (shadowing a global name)
    slice = some_function()
```

### Auto-dereferenced References [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
fn get_first_ref(inout self) -> ref [self] Int:
    return self.first
```

**Context:**
- New `ref` keyword in result type specifiers provides a way to return an "automatically dereferenced" reference
- Enables returning a reference to storage that can be directly assigned to
- Eliminates the need for `__refitem__()` which has been removed in favor of `__getitem__()` that returns a reference

**Usage Example:**
```mojo
@value
struct Pair:
    var first: Int
    var second: Int

    fn get_first_ref(inout self) -> ref [self] Int:
        return self.first

fn show_mutation():
    var somePair = Pair(5, 6)
    somePair.get_first_ref() = 1  # Directly assign to the reference
    print(somePair.first)  # Prints 1
```

### Infer-only Parameters [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
fn parameter_simd[dt: DType, //, value: Scalar[dt]]():
    print(value)
```

**Context:**
- Added support for infer-only parameters that must appear at the beginning of the parameter list
- Infer-only parameters cannot be explicitly specified by the user and are declared to the left of a `//` marker
- Allows functions with dependent parameters to be called without specifying all necessary parameters
- Parameters are inferred from the dependent parameters that follow

**Usage Example:**
```mojo
fn parameter_simd[dt: DType, //, value: Scalar[dt]]():
    print(value)

fn call_it():
    parameter_simd[Int32(42)]()  # dt is inferred as DType.int32

struct ScalarContainer[dt: DType, //, value: Scalar[dt]]:
    pass

fn foo(x: ScalarContainer[Int32(0)]):  # dt is inferred as DType.int32
    pass
```

### Parameter For Statement [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
@parameter
for i in range(max)
    # compile-time loop body
```

**Context:**
- New `@parameter for` mechanism for expressing compile-time loops, replacing the earlier `@unroll` decorator
- Defines a for loop where the sequence and induction values must be parameter values
- More reliable than the previous `@unroll` approach
- Currently requires the sequence's `__iter__()` method to return a `_StridedRangeIterator`

**Usage Example:**
```mojo
fn parameter_for[max: Int]():
    @parameter
    for i in range(max)
        @parameter
        if i == 10:
            print("found 10!")
```

### Function Overloading on Parameters [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Functions overloaded on parameters can now be resolved when forming references to those functions
- This enables taking references to overloaded functions based on their parameter types

**Usage Example:**
```mojo
fn overloaded_parameters[value: Int32]():
    pass

fn overloaded_parameters[value: Float32]():
    pass

fn form_reference():
    alias ref = overloaded_parameters[Int32()]  # Now works!
```

### Deprecation Decorator [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added support for `@deprecated` decorator on structs, functions, traits, aliases, and global variables
- Marks declarations as deprecated and causes a warning when referenced in user code
- Requires a deprecation message specified as a string literal

**Usage Example:**
```mojo
@deprecated("Foo is deprecated, use Bar instead")
struct Foo:
    pass

fn outdated_api(x: Foo):  # warning: Foo is deprecated, use Bar instead
    pass

@deprecated("use another function!")
fn bar():
    pass

fn techdebt():
    bar()  # warning: use another function!
```

### Reference Type Updates [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- The `is_mutable` parameter of `Reference` and `AnyLifetime` is now a `Bool`, not a low-level `__mlir_type.i1`
- Improves ergonomics of spelling out a `Reference` type explicitly

## Standard Library

### New Traits [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added built-in `repr()` function and `Representable` trait
- Added the `Indexer` trait to denote types implementing `__index__()` 
- Types conforming to `Indexer` are implicitly convertible to `Int`
- Added traits for user-defined types to be supported by various built-in and math functions:
  - `Absable` for `abs()`
  - `Powable` for `pow()` and `**` operator
  - `Roundable` for `round()`
  - `Ceilable` for `math.ceil`
  - `CeilDivable`/`CeilDivableRaising` for `math.ceildiv`
  - `Floorable` for `math.floor`
  - `Truncable` for `math.trunc`

**Usage Example:**
```mojo
@value
struct AlwaysZero(Indexer):
    fn __index__(self) -> Int:
        return 0

struct MyList:
    var data: List[Int](1, 2, 3, 4)

    fn __getitem__[T: Indexer](self, idx: T) -> Int:
        return self.data[index(idx)]

print(MyList()[AlwaysZero()])  # prints 1
```

### Benchmarking Module [`STABLE`]

**Package:** `benchmark.bencher`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- The `bencher` module is now public and documented
- Provides types like `Bencher` for executing benchmarks
- Allows configuring benchmarks via the `BenchmarkConfig` struct

### String and Collection Improvements [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** Yes (for String conversion)

**Context:**
- **Breaking**: Implicit conversion to `String` removed for builtin classes/types - use `str()` explicitly
- Added `String.isspace()` method conformant with Python's universal separators
- `String.split()` now defaults to whitespace with Python-like behavior
- Added `String.strip()`, `lstrip()`, and `rstrip()` that can remove custom characters
- Added `String.splitlines()` method for splitting strings at line boundaries
- Renamed `InlinedString` to `InlineString` for consistency
- `StringRef` now implements `strip()`, `startswith()` and `endswith()`
- Added a new `StringSlice` type to replace unsafe `StringRef` in standard library code
- Added `as_bytes_slice()` method to `String` and `StringLiteral`
- Continued transition to `UnsafePointer` and unsigned byte type for strings

**Usage Example:**
```mojo
var s = "  hello  "
print(s.strip())  # "hello"

var multiline = "line1\nline2\r\nline3"
var lines = multiline.splitlines()
# lines contains ["line1", "line2", "line3"]
```

### List Enhancements [`STABLE`]

**Package:** `collections.list`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `index()` method to find the location of an element in a `List`
- Improved string conversion for `List` with a simplified syntax
- Added simplified syntax for the `count()` method
- Added support for `__contains__()` allowing use with the `in` operator
- Added `unsafe_get()` to get a reference to an element without bounds checking

**Usage Example:**
```mojo
var my_list = List[Int](2, 3, 5, 7, 3)
print(my_list.index(3))  # prints 1
print(my_list.__str__())  # prints [2, 3, 5, 7, 3]
print(my_list.count(3))  # prints 2

if 5 in my_list:
    print("Found 5")
```

### Dictionary Improvements [`STABLE`]

**Package:** `collections.dict`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added a `fromkeys()` method to return a `Dict` with specified keys and values
- Added a `clear()` method to remove all items
- Added support for `reversed()` on `items()` and `values()` iterators
- Simplified conversion to `String` with `my_dict.__str__()`
- Implemented `get(key)` and `get(key, default)` functions
- Added a temporary `__get_ref(key)` method to get a `Reference` to a value
- Significant performance improvements for `Dict` insertions

**Usage Example:**
```mojo
var d = Dict.fromkeys(List[String]("a", "b", "c"), 1)
print(d.get("a"))  # prints 1
print(d.get("z", 0))  # prints 0

for key in reversed(d.keys()):
    print(key)
```

### InlineList Type [`STABLE`]

**Package:** `collections.inline_list`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added a new `InlineList` type, a stack-allocated list with a static maximum size

### Span Type [`STABLE`]

**Package:** `memory.span`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added a new `Span` type for taking slices of contiguous collections

### OS Module Enhancements [`STABLE`]

**Package:** `os`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `mkdir()` and `rmdir()` for creating and removing directories
- Added `os.path.getsize()` to get file size in bytes
- Added `os.path.join()` function
- Added new `tempfile` module with `gettempdir()` and `mkdtemp()` functions

### SIMD Enhancements [`STABLE`]

**Package:** `builtin.simd`
**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** Yes (for `__bool__`)

**Context:**
- Added `SIMD.shuffle()` with `IndexList` mask
- `SIMD.__bool__()` is now constrained to only work when `size` is `1`
- For SIMD vectors with more than one element, use `any()` or `all()`
- The `reduce_or()` and `reduce_and()` methods are now bitwise operations
- Added `__repr__()` to get the verbose string representation of `SIMD` types

**Usage Example:**
```mojo
fn truthy_simd():
    var vec = SIMD[DType.int32, 4](0, 1, 2, 3)
    if any(vec):
        print("any elements are truthy")
    if all(vec):
        print("all elements are truthy")
```

### Math Package Reorganization [`BREAKING`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** Yes

**Context:**
- `math.bit` module moved to top-level `bit` module
- Several function names changed for clarity:
  - `ctlz` → `countl_zero`
  - `cttz` → `countr_zero`
  - `bit_length` → `bit_width`
  - `ctpop` → `pop_count`
  - `bswap` → `byte_swap`
  - `bitreverse` → `bit_reverse`
- `rotate_bits_left()` and `rotate_bits_right()` moved to `bit` module
- `is_power_of_2()` is now `is_power_of_two()` in the `bit` module
- `abs()`, `round()`, `min()`, `max()`, `pow()`, and `divmod()` moved from `math` to `builtin`
- `math.tgamma()` renamed to `math.gamma()` to conform with Python
- Various utility functions moved to `utils.numerics` module
- `math.gcd()` now works on negative inputs and accepts a variadic list of integers

**Migration:**
```mojo
# Before
from math import abs, round, min, max, pow
from math.bit import ctlz, rotate_bits_left

# After
# These are now builtins and don't need imports
# abs, round, min, max, pow
from bit import countl_zero, rotate_bits_left
```

### Coroutine and Async Updates [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** Yes

**Context:**
- `Coroutine` now requires a lifetime parameter to ensure arguments live as long as the coroutine
- Async function calls no longer allowed to borrow non-trivial register-passable types

## Tooling Changes

### Mojo Package Command [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Invoking `mojo package my-package -o my-dir` now outputs to `my-dir/my-package.mojopkg`
- Previously required specifying the full path including filename

### Diagnostic Improvements [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Language Server now reports warnings for unused local variables
- Several `mojo` subcommands now support a `--diagnostic-format` option
- Specifying `--diagnostic-format json` outputs errors in structured JSON Lines format
- New `--validate-doc-strings` option to emit errors on invalid doc strings
- `--warn-missing-doc-strings` renamed to `--diagnose-missing-doc-strings`
- New `@doc_private` decorator to hide declarations from documentation

### Debugger Improvements [`STABLE`]

**Available Since:** `v24.4`
**Status:** Stable
**Breaking:** No

**Context:**
- Debugger users can now set breakpoints on function calls in O0 builds
- Language Server now supports renaming local variables

## Removed Features

### `@unroll` Decorator [`REMOVED`]

**Available Since:** `v24.4`
**Status:** Removed
**Breaking:** Yes

**Context:**
- The `@unroll` decorator has been deprecated and removed
- Replaced by the `@parameter for` feature which is more robust
- `@unroll` was not as reliable as a compiler-based approach

**Migration:**
```mojo
# Before
@unroll
for i in range(5):
    print(i)

# After
@parameter
for i in range(5)
    print(i)
```

### Other Removals [`REMOVED`]

**Available Since:** `v24.4`
**Status:** Removed
**Breaking:** Yes

**Context:**
- `object.print()` removed - use `print(my_object)` instead
- Many math functions removed in favor of operators or simplified alternatives
- `EvaluationMethod` removed from `math.polynomial`
- The `math.bit.select()` and `math.bit.bit_and()` functions removed
- The `math.limit` module removed
- The `tensor.random` module removed - functionality now in Tensor static methods
- The SIMD struct no longer conforms to `Indexer`

## Fixed Issues

- Fixed self-referential variant crashing the compiler
- Fixed LSP crashing on simple trait definitions
- Fixed error when using `//` on `FloatLiteral` in alias expression
- Improved dictionary performance, especially for integer keys
- Fixed `assert_raises` to include calling location
