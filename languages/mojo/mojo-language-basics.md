TITLE: Mojo Programming Language
VERSION: 0.6.0
RELEASED: 2024-03-01
COMPATIBILITY: macOS, Linux, Python 3.8+
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/manual/
MODEL: Claude-3.7-Sonnet-Thinking

# Mojo Programming Language Technical Reference

## Conceptual Overview

- **Python Compatibility with Systems Performance**: Mojo combines Python's syntax and ease of use with systems programming features like memory safety, value semantics, and performance optimization capabilities.
- **Value Semantics and Ownership Model**: Mojo implements a robust ownership model with argument conventions (`read`, `mut`, `owned`, `out`) and ownership transfer (`^`) that provides memory safety without garbage collection.
- **Compile-time Metaprogramming**: Mojo supports powerful compile-time metaprogramming through parameters, the `@parameter` decorator, and compile-time evaluation.
- **Progressive Type Safety**: Offers both dynamic programming through `def` functions with optional typing and stronger static guarantees through `fn` functions with required type annotations.
- **Zero-cost Abstractions**: Designed for high-performance computing with features like SIMD vectorization, register-passable types, and inlining while maintaining developer ergonomics.

## Core Language

### Variables [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# Explicitly declared variables (block-scoped)
var x: Int = 42
var y = 3.14  # Type inference

# Implicitly declared variables (function-scoped)
z = 10  # Type inference
```

**Usage Example:**
```mojo
# Variable with explicit type annotation
var counter: Int = 0

# Variable with type inference
var name = String("Mojo")

# Implicitly declared variable
message = "Hello, World!"
```

**Context:**
- Purpose: Store and manipulate data during program execution
- Patterns: Type inference, explicit typing for clarity and safety
- Limitations: Variables are strongly typed; once declared, a variable's type cannot change

**Edge Cases and Anti-patterns:**
- Implicitly declared variables (without `var`) use function-scoped semantics similar to Python, while explicitly declared variables use block-scoped semantics
- Attempting to use an uninitialized variable results in a compile-time error

```mojo
# ANTI-PATTERN:
var uninitialized: Int  # Declared but not initialized
print(uninitialized)    # Error: use of uninitialized value

# CORRECT:
var initialized: Int = 0
print(initialized)
```

### Types [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# Numeric types
var integer: Int = 42
var unsigned: UInt = 42
var float_val: Float64 = 3.14

# Other basic types
var text: String = "Hello"
var condition: Bool = True
```

**Usage Example:**
```mojo
# Integer types with specific bit widths
var i8: Int8 = 127
var i16: Int16 = 32767
var i32: Int32 = 2147483647
var i64: Int64 = 9223372036854775807

# Float types with specific bit widths
var f16: Float16 = 1.5
var f32: Float32 = 3.14
var f64: Float64 = 3.141592653589793
```

**Context:**
- Purpose: Represent different kinds of data with appropriate memory usage and operations
- Related: Most types in Mojo are implemented as `struct`s
- Behavior: All types support value semantics and ownership transfer

**Edge Cases and Anti-patterns:**
- Floating-point comparisons can be inexact due to rounding errors
- Be careful with integer overflow, especially with fixed-width integer types

```mojo
# ANTI-PATTERN (inexact floating-point comparison):
var a = 0.1 + 0.2
var b = 0.3
if a == b:  # This may not be true due to floating-point imprecision
    print("Equal")

# CORRECT:
from math import isclose
if isclose(a, b, 1e-10):
    print("Approximately equal")
```

### Control Flow [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# If statements
if condition:
    # code block
elif other_condition:
    # code block
else:
    # code block

# While loops
while condition:
    # code block
    continue  # Skip to next iteration
    break     # Exit loop
else:
    # Executed if loop completes normally (not via break)

# For loops
for item in iterable:
    # code block
```

**Usage Example:**
```mojo
# If statement with conditional expression
var temperature = 22
var description = "warm" if temperature > 20 else "cool"

# While loop with break
var count = 0
while count < 10:
    if count == 5:
        break
    count += 1

# For loop with range
for i in range(5):
    print(i)  # Prints 0, 1, 2, 3, 4
```

**Context:**
- Purpose: Control the flow of execution in a program
- Behavior: Short-circuit evaluation is used for boolean operators (`and`, `or`)

**Edge Cases and Anti-patterns:**
- The `else` clause in loops executes only when the loop terminates normally (not via `break`)
- For collection types, iteration produces references that must be dereferenced with `[]`

```mojo
# When iterating over Mojo collections:
from collections import List
var items = List[Int](1, 2, 3)

# ANTI-PATTERN:
for item in items:
    print(item)  # Error: trying to print a Reference

# CORRECT:
for item in items:
    print(item[])  # Dereference the Reference with []
```

### Functions [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# fn functions (stricter, more explicit)
fn add(a: Int, b: Int) -> Int:
    return a + b

# def functions (more flexible, Python-like)
def compute(a, b):
    return a + b

# Function with error handling
fn process(value: Int) raises -> Int:
    if value < 0:
        raise Error("Negative value")
    return value * 2
```

**Usage Example:**
```mojo
# Function with optional arguments
fn greet(name: String, greeting: String = "Hello") -> String:
    return greeting + ", " + name + "!"

# Function with variadic arguments
fn sum(*values: Int) -> Int:
    var total = 0
    for value in values:
        total += value
    return total

# Using argument conventions
fn update_counter(mut counter: Int):
    counter += 1
```

**Context:**
- Purpose: Encapsulate reusable code blocks and logic
- Patterns:
  - `fn`: Strict type checking, explicit return types, explicit error handling
  - `def`: More flexible, Python-like, implicit types possible
- Alternatives: Use structs with methods for object-oriented designs
- Behavior: Arguments follow ownership rules based on conventions (`read`, `mut`, `owned`, `out`)

**Edge Cases and Anti-patterns:**
- Functions declared with `fn` must explicitly handle any errors from called functions unless they declare `raises`
- Functions declared with `def` can always raise errors without explicit declaration

```mojo
# ANTI-PATTERN (for fn functions):
fn process_data(data: String):
    parse(data)  # Error if parse() can raise an exception

# CORRECT:
fn process_data(data: String):
    try:
        parse(data)
    except e:
        print("Parsing error:", e)

# OR:
fn process_data(data: String) raises:
    parse(data)  # OK, because this function can propagate errors
```

### Error Handling [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# Raising errors
raise Error("Error message")
raise "Error message"  # Shorthand

# Handling errors
try:
    # Code that might raise an error
except e:
    # Handle error
else:
    # Executed if no error occurs
finally:
    # Always executed
```

**Usage Example:**
```mojo
# Function that raises an error
fn validate(value: Int) raises:
    if value < 0:
        raise Error("Negative value not allowed")

# Handling errors
try:
    validate(-5)
except e:
    print("Validation error:", e)

# Using context managers for resource management
with open("file.txt", "r") as file:
    content = file.read()
```

**Context:**
- Purpose: Handle exceptional conditions and ensure proper resource cleanup
- Patterns: Try-except blocks for error handling, context managers for resource management
- Alternatives: Return success/failure codes for non-exceptional conditions

**Edge Cases and Anti-patterns:**
- `fn` functions must use the `raises` keyword if they can raise an error
- Missing error handling in non-raising functions will cause a compilation error

```mojo
# ANTI-PATTERN:
fn process(path: String):
    open(path, "r")  # Error if open() can raise (e.g., file not found)

# CORRECT:
fn process(path: String):
    try:
        open(path, "r")
    except e:
        print("Error opening file:", e)
```

## Data Structures

### Structs [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
struct MyStruct:
    var field1: Int
    var field2: String

    fn __init__(out self, field1: Int, field2: String):
        self.field1 = field1
        self.field2 = field2

    fn my_method(self) -> Int:
        return self.field1
```

**Usage Example:**
```mojo
# Creating a struct with the @value decorator for automatic lifecycle methods
@value
struct Point:
    var x: Float64
    var y: Float64

    fn distance(self, other: Point) -> Float64:
        let dx = self.x - other.x
        let dy = self.y - other.y
        return (dx*dx + dy*dy).sqrt()

    @staticmethod
    fn origin() -> Self:
        return Self(0, 0)

# Using the struct
var p1 = Point(3, 4)
var p2 = Point(0, 0)
var dist = p1.distance(p2)  # 5.0
```

**Context:**
- Purpose: Define custom data types with fields and methods
- Patterns: Use `@value` decorator to automatically generate lifecycle methods
- Alternatives: Plain functions for procedural code
- Limitations: No inheritance (unlike Python classes), but can implement traits for similar functionality

**Edge Cases and Anti-patterns:**
- Struct fields must be explicitly declared with `var`
- Structs are static; you can't add fields or methods at runtime
- Use `@staticmethod` for methods that don't need access to instance data

```mojo
# ANTI-PATTERN (trying to use inheritance):
struct Child(Parent):  # Error: no inheritance in Mojo
    var extra_field: Int

# CORRECT (use traits instead):
trait Behavior:
    fn behave(self): ...

struct Implementation(Behavior):
    fn behave(self):
        print("Implemented behavior")
```

### Traits [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
trait MyTrait:
    fn required_method(self): ...

    fn default_method(self):
        print("Default implementation")
```

**Usage Example:**
```mojo
# Define a trait
trait Printable:
    fn print(self): ...

# Implement the trait
struct Message(Printable):
    var text: String

    fn __init__(out self, text: String):
        self.text = text

    fn print(self):
        print(self.text)

# Function that works with any Printable type
fn display[T: Printable](item: T):
    item.print()
```

**Context:**
- Purpose: Define interfaces that structs can implement for polymorphism
- Patterns: Use traits to enable generic programming
- Alternatives: Type-specific functions when polymorphism is not needed
- Related: Mojo's standard library defines traits like `Stringable`, `Comparable`, etc.

**Edge Cases and Anti-patterns:**
- Traits can have default implementations, but cannot have fields
- Use square brackets to define generic functions that accept trait-conforming types

### Collection Types [`STABLE`]

**Package:** `collections`
**Status:** Stable

**Dependencies/Imports:**
```mojo
from collections import List, Dict, Set, Optional
```

**Signature:**
```mojo
# List - dynamic array
var list = List[Int]()
list.append(42)

# Dict - key-value mappings
var dict = Dict[String, Int]()
dict["key"] = 42

# Set - unique elements
var set = Set[String]()
set.add("value")

# Optional - maybe-present value
var opt: Optional[Int] = 42
var none: Optional[Int] = None
```

**Usage Example:**
```mojo
# Working with List
var numbers = List[Int](1, 2, 3)
numbers.append(4)
var sum = 0
for num in numbers:
    sum += num[]
print(sum)  # 10

# Working with Dict
var scores = Dict[String, Int]()
scores["Alice"] = 95
scores["Bob"] = 87
for item in scores.items():
    print(item[].key, "scored", item[].value)

# Using Optional with or_else for default values
var maybe: Optional[String] = None
print(maybe.or_else("default"))  # "default"
```

**Context:**
- Purpose: Store and manipulate collections of values
- Patterns: Generic collections that work with any type
- Limitations: Elements must conform to certain traits (`CollectionElement` for List, `KeyElement` for Dict keys)
- Behavior: All collections follow value semantics and ownership rules

**Edge Cases and Anti-patterns:**
- Collection iteration currently returns references that must be dereferenced with `[]`
- No direct list literal syntax like Python's `[1, 2, 3]`

```mojo
# ANTI-PATTERN:
var my_list: List[Int] = [1, 2, 3]  # Error: no list literal syntax

# CORRECT:
var my_list = List[Int](1, 2, 3)
```

## Integration Features

### Python Integration [`STABLE`]

**Package:** `python`
**Status:** Stable

**Dependencies/Imports:**
```mojo
from python import Python, PythonObject
```

**Signature:**
```mojo
# Import Python modules
np = Python.import_module("numpy")
pd = Python.import_module("pandas")

# Convert between Python and Mojo types
py_value = np.int64(42)
mojo_value = Int(py_value)
```

**Usage Example:**
```mojo
def use_numpy():
    # Import a Python module
    np = Python.import_module("numpy")

    # Create a numpy array
    arr = np.array([1, 2, 3, 4])
    mean = arr.mean()
    print("Mean:", mean)

    # Iterate over Python collections
    for value in arr:
        print(value)
```

**Context:**
- Purpose: Seamlessly interoperate with Python code and libraries
- Patterns: Import Python modules, use Python objects, convert between Mojo and Python types
- Limitations: Performance overhead when crossing the Mojo-Python boundary
- Related: `PythonObject` type for wrapping Python objects

**Edge Cases and Anti-patterns:**
- Python objects follow Python's reference semantics, not Mojo's value semantics
- Converting large data between Python and Mojo can be expensive

```mojo
# ANTI-PATTERN (crossing boundary frequently):
from python import Python
np = Python.import_module("numpy")
arr = np.array([1, 2, 3, 4])
total = 0
for i in range(len(arr)):
    total += Int(arr[i])  # Crossing boundary for each element

# BETTER:
total_py = arr.sum()
total = Int(total_py)  # Cross boundary only once
```

## Modules and Package Management

### Modules and Packages [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# Import specific members
from module import Item

# Import entire module
import module

# Import with alias
import module as mod
```

**Usage Example:**
```mojo
# Creating a module (mymodule.mojo)
struct MyType:
    var value: Int

    fn __init__(out self, value: Int):
        self.value = value

# Using the module (main.mojo)
from mymodule import MyType
var instance = MyType(42)

# Creating a package (directory with __init__.mojo)
# mypackage/
#   __init__.mojo
#   submodule.mojo

# Using a package
from mypackage.submodule import Component
```

**Context:**
- Purpose: Organize code into reusable, maintainable units
- Patterns: Modules for single-file code, packages for multi-file libraries
- Behavior: Directory with `__init__.mojo` file is treated as a package

**Edge Cases and Anti-patterns:**
- Package directory must contain an `__init__.mojo` file (can be empty)
- Re-export module members from `__init__.mojo` for cleaner imports

```mojo
# mypackage/__init__.mojo
from .mymodule import MyType  # Re-export

# main.mojo
from mypackage import MyType  # Cleaner import
```

## Memory Management

### Memory and Ownership [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# Argument conventions
fn read_only(value: Int)  # Default: read-only reference
fn mutable(mut value: Int)  # Mutable reference
fn take_ownership(owned value: String)  # Take ownership
fn initialize(out value: MyStruct)  # Initialize uninitialized value

# Ownership transfer
take_ownership(my_string^)  # Transfer ownership with ^
```

**Usage Example:**
```mojo
# Simple value semantics
var a = 5
var b = a  # Copy of a
b += 1  # a is still 5

# Modifying through reference
fn increment(mut value: Int):
    value += 1

var x = 10
increment(x)  # x is now 11

# Transferring ownership
fn consume(owned text: String):
    print("Consumed:", text)

var message = String("Hello")
consume(message^)  # message is now uninitialized
# Using message after this would cause an error
```

**Context:**
- Purpose: Ensure memory safety without garbage collection
- Patterns: Explicit ownership transfer with `^`, argument conventions (`read`, `mut`, `owned`, `out`)
- Alternatives: Reference counting or garbage collection in other languages
- Behavior: Compile-time memory management checks

**Edge Cases and Anti-patterns:**
- Using a value after transferring ownership causes a compile-time error
- Not specifying `mut` when modification is needed

```mojo
# ANTI-PATTERN:
fn update_without_mut(counter: Int):
    counter += 1  # Error: cannot modify non-mut argument

# CORRECT:
fn update_with_mut(mut counter: Int):
    counter += 1
```

### Pointers and References [`STABLE`]

**Package:** `memory`
**Status:** Stable

**Dependencies/Imports:**
```mojo
from memory import Pointer, UnsafePointer
```

**Signature:**
```mojo
# Safe, non-owning, non-nullable pointer
var ptr = Pointer.address_of(value)
var deref_value = ptr[]  # Dereference

# Unsafe pointer for low-level memory management
var unsafe_ptr = UnsafePointer[Int].alloc(1)
unsafe_ptr.init_pointee_copy(42)
unsafe_ptr.destroy_pointee()
unsafe_ptr.free()
```

**Usage Example:**
```mojo
from memory import Pointer

# Using safe pointers
var value = 42
var ptr = Pointer.address_of(value)
print(ptr[])  # 42
value = 100
print(ptr[])  # 100 (pointer reflects the updated value)

# Function that returns a reference to an element
fn get_ref_to_element(ref arr: List[Int], index: Int) -> ref [arr] Int:
    return arr[index]
```

**Context:**
- Purpose: Low-level memory access and management
- Patterns: Use `Pointer` for safe references, `UnsafePointer` only when necessary
- Alternatives: Prefer high-level collections and value semantics when possible
- Security: `UnsafePointer` bypasses Mojo's safety checks and should be used carefully

**Edge Cases and Anti-patterns:**
- Using `UnsafePointer` without proper initialization and cleanup
- Accessing memory after it's been freed

```mojo
# ANTI-PATTERN (memory leak):
var ptr = UnsafePointer[Int].alloc(1)
ptr.init_pointee_copy(42)
# Missing: ptr.destroy_pointee() and ptr.free()

# CORRECT:
var ptr = UnsafePointer[Int].alloc(1)
ptr.init_pointee_copy(42)
# Use ptr...
ptr.destroy_pointee()
ptr.free()
```

## Metaprogramming

### Parameterization [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# Parameters (compile-time values) use square brackets
fn function_with_param[size: Int](data: SIMD[DType.float32, size]):
    # ...

# Parameter-dependent code execution
@parameter
if debug_mode:
    print("Debug mode enabled")
```

**Usage Example:**
```mojo
# Generic function with type parameter
fn operate[T: Numeric](a: T, b: T) -> T:
    return a + b

# Function with compile-time numeric parameter
fn create_vector[size: Int]() -> SIMD[DType.float32, size]:
    return SIMD[DType.float32, size](0)

# Call with explicit parameter
var vec = create_vector[4]()  # 4-element vector

# Parameter-dependent iteration
@parameter
for i in range(5):
    print("Compile-time unrolled loop iteration", i)
```

**Context:**
- Purpose: Enable compile-time metaprogramming and generic code
- Patterns: Type parameters for generic code, value parameters for compile-time computation
- Behavior: Parameters are resolved at compile time, can be used for both types and values

**Edge Cases and Anti-patterns:**
- Parameters must be compile-time constants or expressions
- Using parameters when runtime values would be more appropriate

```mojo
# ANTI-PATTERN (using parameter for runtime value):
fn process_data[size: Int](data: List[Int]):  # size must be known at compile time
    @parameter
    for i in range(size):
        # ...

# CORRECT (for runtime-determined sizes):
fn process_data(data: List[Int]):
    for i in range(len(data)):
        # ...
```

## Important Decorators

### Decorators [`STABLE`]

**Package:** `builtin`
**Status:** Stable

**Signature:**
```mojo
# @value - Generate lifecycle methods
@value
struct Point:
    var x: Float64
    var y: Float64

# @parameter - Execute at compile time
@parameter
fn compile_time_function():
    # ...

# @staticmethod - Define a static method
@staticmethod
fn static_function():
    # ...

# @register_passable - Allow passing in registers
@register_passable("trivial")
struct TrivialType:
    var x: Int
```

**Usage Example:**
```mojo
# Using @value for automatic lifecycle methods
@value
struct Vector3D:
    var x: Float64
    var y: Float64
    var z: Float64

    # No need to manually implement __init__, __copyinit__, etc.

    fn magnitude(self) -> Float64:
        return (self.x*self.x + self.y*self.y + self.z*self.z).sqrt()

# Using @always_inline for performance-critical functions
@always_inline
fn critical_operation(a: Int, b: Int) -> Int:
    return a * b + a
```

**Context:**
- Purpose: Modify or enhance the behavior of functions, structs, or methods
- Patterns: Use `@value` for most structs, `@staticmethod` for struct methods that don't need instance access
- Behavior: Decorators are applied at compile time

**Edge Cases and Anti-patterns:**
- `@register_passable("trivial")` requires all fields to be trivial types
- `@value` only generates missing lifecycle methods, existing ones are not overwritten

```mojo
# ANTI-PATTERN (non-trivial field in register-passable struct):
@register_passable("trivial")
struct BadType:
    var x: Int
    var s: String  # Error: String is not register-passable

# CORRECT:
@register_passable("trivial")
struct GoodType:
    var x: Int
    var y: Float64  # Both Int and Float64 are register-passable
```
