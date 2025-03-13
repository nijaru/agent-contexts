# Mojo v24.2 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v24.2
RELEASED: 2024-03-28
COMPATIBILITY: Backwards compatible with standard library changes
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v242-2024-03-28
```

## Conceptual Overview
- **Open Source Standard Library**: Mojo's standard library is now open source
- **Implicit Trait Conformance**: Structs can now implicitly conform to traits if they implement all requirements
- **Python Interoperability**: Added support for passing keyword arguments to Python functions
- **Package Reorganization**: Significant restructuring of standard library packages for better organization

## Core Language

### Implicit Trait Conformance [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- Structs and other nominal types can now implicitly conform to traits
- A struct implicitly conforms if it implements all the requirements for the trait
- Explicit conformance is still recommended for documentation and future features like default methods and extensions

**Usage Example:**
```mojo
@value
struct Foo:
    fn __str__(self) -> String:
        return "foo!"

fn main():
    print(str(Foo()))  # prints 'foo!' because Foo implicitly conforms to Stringable
```

### Python Keyword Arguments [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo's Python interoperability now supports passing keyword arguments to Python functions
- Makes Python API usage more natural and flexible from Mojo

**Usage Example:**
```mojo
from python import Python

def main():
    plt = Python.import_module("matplotlib.pyplot")
    plt.plot((5, 10), (10, 15), color="red")
    plt.show()
```

### Let Declaration Errors [`BREAKING`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** Yes

**Context:**
- `let` declarations now produce a compile-time error instead of a warning
- The compiler still recognizes the `let` keyword to produce good error messages
- This is another step in removing `let` declarations from the language

**Migration:**
```mojo
# Before
let x = 42  # warning

# After
var x = 42  # Use var instead of let
```

### Dynamic Type Value Removal [`BREAKING`]

**Available Since:** `v24.2`
**Status:** Removed
**Breaking:** Yes

**Context:**
- Dynamic type values have been disabled in the language
- Type-valued parameters still work as before
- Will be redesigned in the future when ownership comes in

**Migration:**
```mojo
# No longer allowed
var t = Int
takes_type(SomeType)

# Still works
alias t = Int  # type-valued parameter
takes_type[SomeType]()
```

### Unbound Parameter Restriction [`BREAKING`]

**Available Since:** `v24.2`
**Status:** Changed
**Breaking:** Yes

**Context:**
- The `*_` expression in parameter expressions is now required to occur at the end of a positional parameter list
- No longer allowed in the middle of parameter lists
- Encourages type designers to get the order of parameters right

**Migration:**
```mojo
# No longer supported
alias FirstUnbound = SomeStruct[*_, 42]
alias MidUnbound   = SomeStruct[7, *_, 6]

# Still supported
alias LastUnbound  = SomeStruct[42, *_]
```

## Standard Library

### Open Source Standard Library [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- The Mojo standard library is now open source
- Available on GitHub in the [modular/max](https://github.com/modular/max) repository
- Developers can contribute to the library and understand implementation details
- Check out the [README](https://github.com/modular/max/blob/main/mojo/stdlib/README.md) for contributing

### List Type [`STABLE`]

**Package:** `collections.list`
**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** Yes (renamed)

**Context:**
- `DynamicVector` has been renamed to `List` and moved to `collections.list` module
- Constructor now accepts variadic number of values
- Supports negative indexing like Python (-1 refers to last element)
- `push_back()` has been removed in favor of `append()`

**Usage Example:**
```mojo
var numbers = List[Int](1, 2, 3)
print(numbers[-1])  # prints '3'
numbers.append(4)  # Add element to the end
```

**Migration:**
```mojo
# Before
from collections.vector import DynamicVector
var v = DynamicVector[Int]()
v.push_back(1)

# After
from collections.list import List
var v = List[Int]()
v.append(1)
```

### String and Print Enhancements [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- `print()` function now takes `sep` and `end` keyword arguments
- `print_no_newline()` function removed - use `print(end="")` instead
- `String` types now conform to `IntableRaising` trait allowing `int("123")` conversion
- `String.tolower()` and `toupper()` renamed to `str.lower()` and `str.upper()`

**Usage Example:**
```mojo
print("Hello", "Mojo", sep=", ", end="!!!\n")  # prints Hello, Mojo!!!
print(int("123"))  # Converts string to integer

var s = "Hello"
print(s.upper())  # prints "HELLO"
```

### Infinite-precision FloatLiteral [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- `FloatLiteral` is now an infinite-precision non-materializable type
- Allows compile-time calculations without rounding errors
- When materialized at runtime, converts to `Float64`

**Usage Example:**
```mojo
# third is an infinite-precision FloatLiteral value
alias third = 1.0 / 3.0
# t is a Float64
var t = third
```

### Tuple Improvements [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- Tuple now works with memory-only element types like `String`
- Allows direct indexing with parameter expressions (`tup[1]` instead of `tup.get[1, Int]()`)
- Support for assigning to tuple elements with `tup[1] = x`

**Usage Example:**
```mojo
var tuple = ("Green", 9.3)
var name = tuple[0]
var value = tuple[1]
tuple[0] = "Blue"
```

### Reference Type Updates [`STABLE`]

**Package:** `memory.reference`
**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** Yes (moved)

**Context:**
- Moved to the `memory.reference` module instead of `memory.unsafe`
- Added `unsafe_bitcast()` method
- Removed unsafe methods that don't belong on a safe type - use `UnsafePointer` instead

### CollectionElement Trait [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** Yes (moved)

**Context:**
- `CollectionElement` is now a built-in trait
- Removed from `collections.vector`
- Many standard library types now conform to this trait

## Package Reorganization [`BREAKING`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** Yes

**Context:**
- Major package reorganization for clarity and future growth:
  - `utils.vector` moved to `collections` package
  - Renamed `InlinedFixedVector` parameters to `[type, size]` instead of `[size, type]`
  - `write_file()` in `Buffer` renamed to `tofile()` for Python compatibility
  - Various other modules renamed or moved

**Migration:**
```mojo
# Before
from utils.vector import DynamicVector, InlinedFixedVector

# After
from collections.list import List  # DynamicVector is now List
from collections.vector import InlinedFixedVector

# Before
buffer.write_file("data.bin")

# After
buffer.tofile("data.bin")
```

### Other Standard Library Changes [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `argmax()` and `argmin()` functions to `Tensor`
- New `OptionalReg` type as a register-passable alternative to `Optional`
- Added `ulp()` function to the `math` module
- More standard library types conform to `CollectionElement` trait

**Usage Example:**
```mojo
# Find position of max value in a tensor
var tensor = Tensor[DType.float32](2, 3)
# ... fill tensor with values
var max_pos = tensor.argmax()
```

## Tooling Changes

### VS Code Extension [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- VS Code extension now includes a Mojo language server
- Provides completion, quick fixes, tooltips, and more

### REPL Magic Commands [`STABLE`]

**Available Since:** `v24.2`
**Status:** Stable
**Breaking:** No

**Context:**
- REPL now provides limited support for the `%cd` magic command
- Maintains an internal stack of directories you visit during the session

**Usage Example:**
```mojo
%cd 'dir'  # Change to directory 'dir' and push it on the stack
%cd -      # Pop the directory stack and change to the last visited directory
```

## Fixed Issues

- Fixed missing overloads for `Testing.assertEqual` so they work on `Integer` and `String` values
- Fixed playground evaluation stopping on generic definitions
- Fixed memory leak in Python interoperability
- Fixed rounding issue with floor division with negative numerator
- Fixed sort function returning invalid results in corner cases
- Fixed initialization of tensors in alias declarations
- Fixed `time.now()` function to return nanoseconds across all operating systems
