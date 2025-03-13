# Mojo v0.6.0 Release Notes

## Metadata
```
TITLE: Mojo Programming Language
VERSION: v0.6.0
RELEASED: 2023-09-21
COMPATIBILITY: Some breaking changes from v0.5.x
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/changelog/#v060-2023-09-21
```

## Conceptual Overview
- **Traits System**: First-class traits support with inheritance, conformance, and generic programming
- **Memory Model Improvements**: `Destructable` trait and type-safe destruction
- **Dynamic Collections**: Generic `DynamicVector` for memory-primary types
- **Standard Library Traits**: Added `Copyable`, `Movable`, `Stringable`, and other foundational traits
- **New Mojo Manual**: Completely rewritten documentation with enhanced examples

## Core Language

### Traits [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Signature:**
```mojo
trait SomeTrait:
    fn required_method(self, x: Int): ...
```

**Context:**
- Traits define a required set of method prototypes
- Structs can conform to traits by implementing required methods
- Enables writing generic functions that work on any conforming type
- Traits can inherit from other traits

**Usage Example:**
```mojo
trait SomeTrait:
    fn required_method(self, x: Int): ...

struct SomeStruct(SomeTrait):
    fn required_method(self, x: Int):
        print("hello traits", x)

fn fun_with_traits[T: SomeTrait](x: T):
    x.required_method(42)

fn main():
    var thing = SomeStruct()
    fun_with_traits(thing)  # Prints "hello traits 42"
```

**Edge Cases and Anti-patterns:**
- Default method implementations are not supported yet
- Traits cannot have stored properties

### Destructable Trait [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Core trait that every trait automatically conforms to
- Enables destruction of generic types and generic collections
- Will eventually be merged with `AnyType` in the future

**Usage Example:**
```mojo
fn destroy_any[T: Destructable](owned value: T):
    # value is automatically destroyed when function ends
    pass
```

### DynamicVector Type [`STABLE`]

**Package:** `utils.vector`
**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Proper generic collection that works with any type implementing `Movable` and `Copyable` traits
- Can be used with memory-primary types like `String`
- Invokes element destructors upon destruction

**Usage Example:**
```mojo
from utils.vector import DynamicVector

fn main():
    var vec = DynamicVector[String]()
    vec.push_back("Hello")
    vec.push_back("Traits")
    vec.push_back("!")
    
    for i in range(len(vec)):
        print(vec[i])
```

### Value Decorator [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `@value` decorator reduces boilerplate for structs
- Synthesizes missing memberwise initializer, `__copyinit__`, and `__moveinit__` methods
- Encourages best practices in value semantics and ownership management

**Usage Example:**
```mojo
@value
struct MyPet:
    var name: String
    var age: Int
    
    # The following are automatically synthesized:
    # fn __init__(inout self, owned name: String, age: Int)
    # fn __copyinit__(inout self, existing: Self)
    # fn __moveinit__(inout self, owned existing: Self)

fn main():
    var pet = MyPet("Rover", 5)
    print(pet.name)  # Prints "Rover"
```

### Package System [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo now supports packages with `__init__.mojo` or `__init__.🔥` files
- Files in the same directory form modules within the package
- Direct module and package imports with attribute references
- Similar to Python's package system

**Usage Example:**
```mojo
# main.mojo
from my_package.module import some_function
from my_package.other_package.stuff import SomeType

fn main():
    var x: SomeType = some_function()
```

**Directory structure:**
```
main.🔥
my_package/
  __init__.🔥
  module.🔥
  other_package/
    __init__.🔥
    stuff.🔥
```

### Adaptive Decorator [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `@adaptive` decorator for creating overloaded functions
- Represents functions that can resolve to multiple valid candidates
- Emits a fork at call site, creating multiple function candidates
- Useful for search-based optimization

**Usage Example:**
```mojo
@adaptive
fn sort(arr: ArraySlice[Int]):
    bubble_sort(arr)

@adaptive
fn sort(arr: ArraySlice[Int]):
    merge_sort(arr)

fn concat_and_sort(lhs: ArraySlice[Int], rhs: ArraySlice[Int]):
    let arr = lhs + rhs
    sort(arr)  # This forks compilation, creating two instances
```

### Parameter If [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `@parameter if` for compile-time conditional code
- Only emits the 'True' side of the condition to the binary
- Provides "static if" functionality with cleaner syntax than interfaces
- Requires condition to be a parameter expression

**Usage Example:**
```mojo
fn vector_add[width: Int](a: SIMD[DType.float32, width], 
                          b: SIMD[DType.float32, width]) -> SIMD[DType.float32, width]:
    @parameter
    if width == 1:
        return SIMD[DType.float32, 1](a[0] + b[0])
    else:
        return a + b
```

## Standard Library

### Core Traits [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Added foundational traits to the standard library:
  - `Destructable`: For types that can be destroyed
  - `Copyable`: For types that can be copied
  - `Movable`: For types that can be moved
  - `Stringable`: For types that can be converted to strings
  - `Intable`: For types that can be converted to integers
  - `Sized`: For types that have a size/length
  - `CollectionElement`: For types that can be stored in collections

**Usage Example:**
```mojo
@value
struct Point(Stringable, Sized):
    var x: Int
    var y: Int
    
    fn __str__(self) -> String:
        return "(" + str(self.x) + ", " + str(self.y) + ")"
        
    fn __len__(self) -> Int:
        return 2  # x and y components

print(str(Point(3, 4)))  # Prints "(3, 4)"
```

### Built-in Functions [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Added built-in functions that work with traits:
  - `len()`: For types implementing `Sized`
  - `str()`: For types implementing `Stringable`
  - `int()`: For types implementing `Intable`

**Usage Example:**
```mojo
var my_list = DynamicVector[Int]()
my_list.push_back(1)
my_list.push_back(2)
print(len(my_list))  # Prints 2

var value = 3.14
print(str(value))  # Prints "3.14"
print(int("42"))   # Prints 42
```

### Coroutine Module [`STABLE`]

**Package:** `builtin.coroutine`
**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- `Coroutine` type for async function results
- Provides the foundation for asynchronous execution
- Supports awaiting, resuming, and retrieving results

**Usage Example:**
```mojo
async fn add_three(a: Int, b: Int, c: Int) -> Int:
    return a + b + c

async fn call_it():
    let task: Coroutine[Int] = add_three(1, 2, 3)
    print(await task)  # Prints 6
```

## Tooling

### Mojo Manual [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- New comprehensive Mojo user guide
- [Available online](https://docs.modular.com/mojo/manual/)
- Open-sourced on GitHub for community contributions
- Replaces the original programming manual

### Language Server Protocol Support [`STABLE`]

**Available Since:** `v0.6.0`
**Status:** Stable
**Breaking:** No

**Context:**
- Mojo Language Server implements Document Symbols request
- Enables Outline View and Go to Symbol features in IDEs
- Shows documentation when code-completing modules or packages
- Processes code examples in doc strings for better IDE features
- Provides semantic token information for improved highlighting

**Edge Cases and Anti-patterns:**
- Some advanced IDE features may not work with very complex parameterized types

## Fixed Issues

- Fixed issue when throwing an exception from `__init__` before all fields are initialized
- Fixed struct definition with recursive reference crash
- Fixed parameter name shadowing in nested scopes
- Fixed issue when redefining a function and struct in the same cell
- Fixed tuple type syntax and return handling
