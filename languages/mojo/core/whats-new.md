TITLE: What's New in Mojo Since 2023
VERSION: Mojo SDK v0.6.0 (March 2025)
COMPATIBILITY: Mojo SDK v0.6.0+
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/
MODEL: Claude-3.7-Sonnet-Thinking

# What's New in Mojo (2023-2025)

This document summarizes the major changes and enhancements to Mojo since late 2023, focusing on features that may not be covered in the base knowledge of AI assistants.

## Major New Features

### GPU Programming (v25.1, Feb 2025)

- Low-level GPU programming support through the new `gpu` and `layout` packages
- Thread control with `thread_idx`, `block_dim`, and `block_idx` variables
- Memory management between CPU host and GPU device
- Tensor layout management with the `LayoutTensor` type

```mojo
from max.tensor import ManagedTensorSlice
from gpu import thread_idx, block_dim, block_idx

fn gpu_add_kernel(out: ManagedTensorSlice, x: ManagedTensorSlice[out.type, out.rank]):
    tid_x = thread_idx.x + block_dim.x * block_idx.x
    tid_y = thread_idx.y + block_dim.y * block_idx.y
    if tid_x < x.dim_size(0) and tid_y < x.dim_size(1):
        out[tid_x, tid_y] = x[tid_x, tid_y] + 1
```

### Unicode Character Support (v25.1, Feb 2025)

- New `Char` struct for representing Unicode characters
- Comprehensive character type checking methods (is_ascii, is_digit, etc.)
- Improved string iteration with `.chars()` and `.char_slices()` methods
- `StringSlice` replaces the deprecated `StringRef` type

```mojo
from builtin.char import Char

fn process_chars(s: String):
    for c in s.chars():
        if c.is_ascii_digit():
            print("Digit:", c)
        elif c.is_ascii_upper():
            print("Uppercase:", c)
```

### Argument Convention Modernization (v24.6, Dec 2024)

- New argument convention syntax: `read`, `mut`, `owned`, `out`
- Deprecated older argument conventions: `borrowed`/`inout`
- New syntax for output parameters, no longer using `-> T as foo`

```mojo
# Modern argument conventions
fn process(read input: String, mut counter: Int, owned data: List[Int], out result: Int):
    counter += 1
    result = counter
```

### Parameterized Types Enhancement (v24.5, Oct 2024)

- Improved parameter inference for nested types
- Better compile-time error messages for parameter constraints
- Enhanced support for conditional trait conformance

```mojo
struct Container[T: CollectionElement]:
    var data: T
    
    # Method only available for types that are also Stringable
    fn as_string[U: CollectionElement & Stringable, //](self: Container[U]) -> String:
        return String(self.data)
```

## Language Evolution

### Type System Improvements

- Enhanced trait system with better support for associated aliases
- More powerful compile-time metaprogramming capabilities
- Refined value ownership model with clearer lifetime rules
- New standard traits for common operations

### Standard Library Expansion

- Expanded collections module with more data structures
- Enhanced memory management utilities
- Improved Python interoperability
- Additional mathematical and cryptographic functions

### Tooling and Integration

- Enhanced VSCode extension with better debugging
- Improved REPL experience in Jupyter notebooks
- Enhanced error messages and diagnostics
- Better linting and code formatting tools

## Breaking Changes

### Type Conversion Functions (v25.1)

- Legacy conversion functions are deprecated in favor of constructors

| **Before** | **After** |
| --- | --- |
| `bool()` | `Bool()` |
| `float()` | `Float64()` |
| `int()` | `Int()` |
| `str()` | `String()` |

### Constructor Behavior (v25.1)

- Initializers are now treated as static methods
- The `out` argument of initializers follows the same rules as other functions

```mojo
# Before:
instance.__init__()
x.__copyinit__(y)

# After:
instance = T()
x = y
```

### String Iteration (v25.1)

- Direct string iteration is replaced with explicit methods

```mojo
# Before:
for c in some_string:
    # ...

# After:
for c in some_string.char_slices():
    # ...
```

### Legacy Method Removal

- `StringRef` has been removed - use `StringSlice` instead
- `Tuple.get[i, T]()` has been removed - use `tup[i]` or `rebind[T](tup[i])` instead
- `IntLike` trait has been removed - functionality is in `Indexer` trait

## Resources

- [Official Mojo Documentation](https://docs.modular.com/mojo/)
- [Mojo Github Repository](https://github.com/modular-lang/mojo) 
- [Mojo Community Discord](https://discord.gg/modular)
- [Modular Documentation](https://docs.modular.com/)