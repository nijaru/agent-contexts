# Mojo v24.1 Release Notes 

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v24.1
RELEASED: 2024-02-29
COMPATIBILITY: First release under the MAX platform version scheme
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v241-2024-02-29
```

## Conceptual Overview
- **MAX Platform Integration**: Mojo is now bundled with the MAX platform with versioning scheme YY.MAJOR.MINOR
- **Debugging Support**: Added comprehensive debugger support in VS Code
- **Collection Types**: New `Set` type and improved `DynamicVector` with iteration
- **Keyword Arguments**: Enhanced support for keyword-only arguments and parameters
- **Parameter Binding**: New `*_` syntax for explicitly unbinding positional parameters

## Core Language

### Set Type [`STABLE`]

**Package:** `collections.set`
**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
struct Set[T: KeyElement]:
    fn __init__(inout self, *elements: T)
    fn add(inout self, element: T)
    fn remove(inout self, element: T) raises
    # Plus standard operators: |, &, -, ^, etc.
```

**Context:**
- New `Set` type in the collections package, backed by `Dict`
- Fast add, remove, and membership checking operations
- Requires member elements to conform to the `KeyElement` trait
- Supports standard set operations like union, intersection, and difference

**Usage Example:**
```mojo
from collections import Set

var set = Set[Int](1, 2, 3)
print(len(set))  # 3
set.add(4)

for element in set:
    print(element[])

set -= Set[Int](3, 4, 5)
print(set == Set[Int](1, 2))  # True
print(set | Set[Int](0, 1) == Set[Int](0, 1, 2))  # True
let element = set.pop()
print(len(set))  # 1
```

### `in` Operator Support [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo now supports the `x in y` and `x not in y` expressions
- Syntax sugar for `y.__contains__(x)`
- Works with any type that implements the `__contains__` method

**Usage Example:**
```mojo
if 5 in my_list:
    print("Found 5 in the list")

if "key" not in my_dict:
    print("Key not found in dictionary")
```

### Keyword-only Arguments [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
fn my_product(a: Int, b: Int = 1, *, c: Int, d: Int = 2):
    # function body
```

**Context:**
- Mojo now supports keyword-only arguments and parameters
- Parameters after `*` can only be passed by name
- Works with both variadic and keyword-only arguments/parameters
- Variadic keyword arguments (`**kwargs`) are not supported yet

**Usage Example:**
```mojo
fn my_product(a: Int, b: Int = 1, *, c: Int, d: Int = 2):
    print(a * b * c * d)

my_product(3, c=5)     # prints '30'
my_product(3, 5, c=1, d=7)  # prints '105'

fn prod_with_offset(*args: Int, offset: Int = 0) -> Int:
    var res = 1
    for i in range(len(args)):
        res *= args[i]
    return res + offset

print(prod_with_offset(2, 3, 4, offset=10))  # prints 34
```

### Partial Parameter Binding [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `*_` syntax to explicitly unbind any number of positional parameters
- Useful for partially binding parametric types and functions
- Allows more flexible parameterization patterns

**Usage Example:**
```mojo
struct StructWithDefault[a: Int, b: Int, c: Int = 8, d: Int = 9]: pass

alias all_unbound = StructWithDefault[*_]
# equivalent to
alias all_unbound = StructWithDefault[_, _, _, _]

alias first_bound = StructWithDefault[5, *_]
# equivalent to
alias first_bound = StructWithDefault[5, _, _, _]

alias last_bound = StructWithDefault[*_, 6]
# equivalent to
alias last_bound = StructWithDefault[_, _, _, 6]
```

**Edge Cases and Anti-patterns:**
- Since these unbound parameters must be explicitly specified at some point, default values are not applied
- When using `last_bound` from the example, you must still specify values for all the unbound parameters

### DynamicVector Iteration [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- `DynamicVector` now supports iteration
- Iteration values are instances of `Reference` and require dereferencing
- Added `reverse()` and `extend()` methods

**Usage Example:**
```mojo
var v: DynamicVector[String]()
v.append("Alice")
v.append("Bob")
v.append("Charlie")
for x in v:
    x[] = str("Hello, ") + x[]
for x in v:
    print(x[])
```

**Edge Cases and Anti-patterns:**
- Iterating directly over a variadic list produces a `Reference` requiring an extra subscript to dereference
- This will be fixed in a future update

### Debugger Support [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo VS Code extension now includes debugger support
- Breakpoints can be inserted programmatically with the `breakpoint()` function
- See [Debugging](/mojo/tools/debugging) in the Mojo Manual for details

**Usage Example:**
```mojo
fn main():
    var x = 1
    breakpoint()  # Execution will pause here when debugging
    x += 1
    print(x)
```

### Slice API Changes [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** Yes (renamed)

**Context:**
- The standard library `slice` type has been renamed to `Slice`
- A `slice` function has been introduced for Python compatibility
- Follows the naming conventions of other types like `Int` and `String`

**Usage Example:**
```mojo
# Creating a slice
var s = Slice(1, 10, 2)
```

### Boolable Trait [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Added a builtin `Boolable` trait for types that can be represented as a boolean
- To conform to the trait, a type must implement the `__bool__()` method
- Collections like `Dict`, `List`, and `Set` conform to the trait

**Usage Example:**
```mojo
def list_names(names: List[String]):
    if names:  # Evaluates to True if names contains any elements
        for name in names:
            print(name[])
    else:
        print("No names to list.")
```

## Standard Library

### String Methods [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Added `find()`, `rfind()`, `count()`, and `__contains__()` methods to string literals
- Enables checking for substrings with the `in` operator

**Usage Example:**
```mojo
if "Mojo" in "Hello Mojo":
    print("Found Mojo!")

var s = "Hello Mojo"
print(s.find("o"))  # Prints 4
print(s.rfind("o"))  # Prints 9
print(s.count("o"))  # Prints 2
```

### File I/O and Path Support [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Enhanced file I/O with basic `file` module and context manager support
- Improved `Path` type for filesystem operations including `read_bytes()` and `read_text()`
- Tensor `save()` and `load()` methods for preserving shape and datatype

**Usage Example:**
```mojo
# Basic file I/O
with open("my_file.txt", "r") as f:
    print(f.read())

# Path operations
let text_path = Path("file.txt")
let text = text_path.read_text()

# Tensor serialization
let tensor = Tensor[DType.float32]()
tensor.save("tensor.dat")
let tensor_from_file = Tensor[DType.float32].load("tensor.dat")
```

### Pointer Subscripting [`STABLE`]

**Available Since:** `v24.1`
**Status:** Stable
**Breaking:** No

**Context:**
- Added subscripting to `DTypePointer` and `Pointer` for easier access
- Simplifies pointer operations with array-like syntax

**Usage Example:**
```mojo
let p = DTypePointer[DType.float16].alloc(4)
for i in range(4):
    p[i] = i
    print(p[i])
```

## Breaking Changes

### Register-passable Initializer Syntax [`BREAKING`]

**Available Since:** `v24.1`
**Status:** Changed
**Breaking:** Yes

**Context:**
- Initializers for `@register_passable` values should now use `inout self` arguments
- Makes language more consistent, more similar to Python
- The older `-> Self` syntax is still supported but will be removed in the future
- Required for initializers that may raise errors

**Migration:**
```mojo
# Before
@register_passable
struct YourPair:
    var a: Int
    var b: Int
    fn __init__(a: Int, b: Int) -> Self:
        return Self{a: a, b: b}

# After
@register_passable
struct YourPair:
    var a: Int
    var b: Int
    fn __init__(inout self, a: Int, b: Int):
        self.a = a
        self.b = b
```

### Async Functions with Errors [`BREAKING`]

**Available Since:** `v24.1`
**Status:** Changed
**Breaking:** Yes

**Context:**
- Async functions that may raise errors temporarily disabled
- Mojo async is undergoing a rework
- Will be re-enabled in a future release

### Buffer and NDBuffer Parameter Order [`BREAKING`]

**Available Since:** `v24.1`
**Status:** Changed
**Breaking:** Yes

**Context:**
- Parameters for `NDBuffer` and `Buffer` types changed for consistency
- Added support for default dimensions

**Migration:**
```mojo
# Before
NDBuffer[3, DType.float32]

# After
NDBuffer[DType.float32, 3]  # Type is now the first parameter
```

### Vectorize Function Changes [`BREAKING`]

**Available Since:** `v24.1`
**Status:** Changed
**Breaking:** Yes

**Context:**
- `vectorize_unroll` removed, using `vectorize` with `unroll_factor` parameter instead
- `vectorize` signatures changed to put closure `func` first
- `unroll` signatures changed to put closure `func` first 

**Migration:**
```mojo
# Before
vectorize[width, func](size)
vectorize_unroll[width, func, unroll_factor](size)

# After
vectorize[func, width, unroll_factor=1](size)
```

## Fixed Issues

- Fixed issue when parametric function is passed as runtime argument
- Fixed crash during diagnostic emission for parameter deduction failure
- Fixed crash when returning type value instead of instance of expected type
- Fixed wrong type name in error for incorrect self argument type
- Fixed crash on implicit conversion in a global variable declaration
- Fixed issue with accessing a struct member alias without parameters
- Fixed tuple limitations for multiple return values without parentheses
