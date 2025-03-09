# Mojo Language Guide

## Overview

Mojo combines Python's syntax and ease of use with systems programming features like memory safety, value semantics, and performance. This guide covers core Mojo concepts, syntax, and programming patterns. For detailed API references of built-in types and functions, see the [Mojo Built-ins Reference](mojo-built-ins.md).

## Language Basics

### Variables and Types

```mojo
# Explicitly declared variables (block-scoped)
var x: Int = 42
var y = 3.14  # Type inference

# Implicitly declared variables (function-scoped)
z = 10  # Type inference

# Literals
var hex = 0xFF
var binary = 0b1010
var octal = 0o755
```

Variables are strongly typed. Once declared, a variable's type cannot change.

### Control Flow

```mojo
# If statements
if x < 0:
    print("negative")
elif x == 0:
    print("zero")
else:
    print("positive")

# Conditional expression (ternary)
result = "positive" if x > 0 else "non-positive"

# While loops
while x > 0:
    x -= 1
    if x == 5:
        continue  # Skip to next iteration
    if x == 2:
        break     # Exit loop

# For loops
for i in range(5):
    print(i)  # 0 through 4

for i in range(1, 10, 2):
    print(i)  # 1, 3, 5, 7, 9
```

### Functions

Mojo supports two types of functions: `fn` and `def`.

#### `fn` Functions

```mojo
# All arguments require type annotations
# Return type is required (unless it returns None)
# Raises keyword required if function can raise errors
fn add(a: Int, b: Int) -> Int:
    return a + b

fn process(path: String) raises -> String:
    if path == "":
        raise Error("Empty path")
    return path
```

#### `def` Functions

```mojo
# Type annotations are optional
# Return type annotation is optional
# Can always raise errors
def add(a: Int, b: Int) -> Int:
    return a + b

# Without type annotations, arguments are 'object' type
def dynamic_add(a, b):
    return a + b
```

#### Argument Conventions

```mojo
# read: Immutable reference (default)
fn process(data: Int):
    # Cannot modify data

# mut: Mutable reference
fn increment(mut count: Int):
    count += 1

# owned: Takes ownership of value
fn consume(owned data: String):
    data += " (modified)"

# Transfer operator to move ownership when calling
var name = String("Mojo")
consume(name^)  # name becomes uninitialized

# out: Used for constructors or named results
fn get_pair(value: Int, out result: Pair):
    result.first = value
    result.second = value * 2
```

#### Parameters for Metaprogramming

```mojo
# Parameters (compile-time values) go in square brackets
fn repeat[count: Int](msg: String):
    @parameter
    for i in range(count):
        print(msg)

# Call with parameter
repeat[3]("Hello")  # Prints "Hello" three times
```

### Error Handling

```mojo
# Try-except blocks
try:
    result = process("data")
except e:
    print("Error:", e)
else:
    print("Success:", result)
finally:
    print("Cleanup")

# Context managers
with open("file.txt", "r") as f:
    content = f.read()
    # File is automatically closed when block exits
```

## Core Language Features

### Structs

```mojo
struct Point:
    var x: Int
    var y: Int

    # Constructor
    fn __init__(out self, x: Int, y: Int):
        self.x = x
        self.y = y

    # Methods
    fn distance(self, other: Point) -> Float64:
        let dx = self.x - other.x
        let dy = self.y - other.y
        return (dx*dx + dy*dy).sqrt()

    # Static method
    @staticmethod
    fn origin() -> Self:
        return Self(0, 0)
```

#### Value Decorator

```mojo
# @value generates boilerplate lifecycle methods
@value
struct Vector:
    var x: Float64
    var y: Float64
    var z: Float64

    # Custom methods can still be defined
    fn magnitude(self) -> Float64:
        return (self.x*self.x + self.y*self.y + self.z*self.z).sqrt()
```

### Traits

```mojo
# Define a trait (interface)
trait Printable:
    fn print(self): ...

# Implement a trait
struct Message(Printable):
    var text: String

    fn __init__(out self, text: String):
        self.text = text

    fn print(self):
        print(self.text)

# Function requiring a trait
fn display[T: Printable](item: T):
    item.print()
```

### Memory and Ownership

```mojo
# Value semantics: default behavior
var a = 5
var b = a  # Copy of a
b += 1     # a is still 5

# References
fn modify(mut value: Int):
    value += 1

var x = 10
modify(x)   # x is now 11

# Ownership transfer
fn take_ownership(owned s: String):
    s += "!"
    print(s)

var message = String("Hello")
take_ownership(message^)  # message is now uninitialized
# Cannot use message after this point
```

### Pointers and References

```mojo
from memory import UnsafePointer, Pointer

# Safe pointer (non-owning, non-nullable)
var value = 42
var ptr = Pointer.address_of(value)
print(ptr[])  # Dereference with []

# Unsafe pointer
var unsafe_ptr = UnsafePointer[Int].alloc(1)  # Allocate memory
unsafe_ptr.init_pointee_copy(10)              # Initialize memory
print(unsafe_ptr[])                           # Dereference
unsafe_ptr.destroy_pointee()                  # Call destructor
unsafe_ptr.free()                             # Free memory

# References
fn ref_example(ref [self] item: Int) -> ref [self] Int:
    return item
```

## Collection Types

### List

```mojo
from collections import List

# Create and initialize a List
var numbers = List[Int](1, 2, 3)
var empty = List[String]()

# Methods
numbers.append(4)
var last = numbers.pop()
var size = len(numbers)

# Access elements
var first = numbers[0]

# Iterate (currently returns a Reference)
for item in numbers:
    print(item[])  # Need to dereference

# Alternative iteration
for i in range(len(numbers)):
    print(numbers[i])
```

### Dict

```mojo
from collections import Dict

# Create and initialize a Dict
var scores = Dict[String, Int]()
scores["Alice"] = 95
scores["Bob"] = 87

# Check if key exists
if "Alice" in scores:
    print(scores["Alice"])

# Iterate
for key in scores:
    print(key[], scores[key[]])  # Need to dereference

# Use items()
for item in scores.items():
    print(item[].key, item[].value)  # Need to dereference
```

### Set

```mojo
from collections import Set

# Create and initialize a Set
var fruits = Set[String]("apple", "banana", "cherry")
var empty = Set[Int]()

# Methods
fruits.add("orange")
fruits.remove("apple")
var size = len(fruits)

# Set operations
var more_fruits = Set[String]("banana", "kiwi", "mango")
var common = fruits.intersection(more_fruits)
var all_fruits = fruits.union(more_fruits)
```

### Optional

```mojo
from collections import Optional

# Create Optional values
var with_value: Optional[Int] = 42
var no_value: Optional[Int] = None

# Check if value exists
if with_value:
    print(with_value.value())

# Provide default for missing value
print(no_value.or_else(0))
```

## Strings

Basic string usage and creation:

```mojo
# Create String values
var s1: String = "Hello"
var s2 = String("World")

# Concatenation
var greeting = s1 + ", " + s2 + "!"

# Multiple arguments to String constructor
var message = String("The answer is: ", 42)

# String indexing and slicing
var first_char = greeting[0]
var substring = greeting[7:12]  # "World"
```

For detailed string operations, see the [Mojo Built-ins Reference](mojo-built-ins.md).

## Python Integration

```mojo
from python import Python, PythonObject

def use_numpy():
    # Import a Python module
    np = Python.import_module("numpy")

    # Create a numpy array
    arr = np.array([1, 2, 3, 4])
    print(arr.mean())

    # Convert Python object to Mojo type
    py_int = np.int64(42)
    mojo_int = Int(py_int)

    # Add Python package directory to import path
    Python.add_to_path("./my_package")
    custom_module = Python.import_module("custom_module")
```

## Common Patterns

### Implementing a Custom Type

```mojo
@value
struct Complex(Stringable, Comparable):
    var real: Float64
    var imag: Float64

    # Constructor with default value
    fn __init__(out self, real: Float64, imag: Float64 = 0.0):
        self.real = real
        self.imag = imag

    # Operator overloading
    fn __add__(self, other: Self) -> Self:
        return Self(self.real + other.real, self.imag + other.imag)

    # In-place operator
    fn __iadd__(mut self, other: Self):
        self.real += other.real
        self.imag += other.imag

    # String representation
    fn __str__(self) -> String:
        if self.imag >= 0:
            return String(self.real, " + ", self.imag, "i")
        return String(self.real, " - ", -self.imag, "i")

    # Comparison operator (for Comparable trait)
    fn __lt__(self, other: Self) -> Bool:
        let self_mag = self.real*self.real + self.imag*self.imag
        let other_mag = other.real*other.real + other.imag*other.imag
        return self_mag < other_mag
```

### Working with Files

```mojo
# Reading a file
fn read_file(path: String) raises -> String:
    with open(path, "r") as file:
        return file.read()

# Writing to a file
fn write_file(path: String, content: String) raises:
    with open(path, "w") as file:
        file.write(content)

# Reading a file line by line
fn process_lines(path: String) raises:
    with open(path, "r") as file:
        for line in file:
            print(line[])  # Need to dereference
```

### Creating a Module

Structure a module in a directory with an `__init__.mojo` file:

```
mymodule/
    __init__.mojo
    utilities.mojo
```

Import the module:

```mojo
from mymodule import SomeStruct
# or
import mymodule
var instance = mymodule.SomeStruct()
```

## Important Decorators

```mojo
# @value - Generate lifecycle methods
@value
struct Point:
    var x: Float64
    var y: Float64

# @always_inline - Force inlining of functions
@always_inline
fn add(a: Int, b: Int) -> Int:
    return a + b

# @parameter - Execute at compile time
@parameter
if debug_mode:
    print("Debug mode")

# @staticmethod - Define a static method
@staticmethod
fn create_default() -> Self:
    return Self(0, 0)

# @register_passable - Allow passing in registers
@register_passable("trivial")
struct Coordinate:
    var x: Int
    var y: Int
```

## Lifetimes and Origins

```mojo
# Use ref to return a reference
fn get_item(ref self, index: Int) -> ref [self] Int:
    return self.items[index]

# Define a struct with parametric mutability
struct SafeRef[
    is_mutable: Bool, //,
    T: AnyType,
    origin: Origin[is_mutable]
]:
    var ptr: UnsafePointer[T]

    fn __getitem__(self) -> T:
        return self.ptr[]

    @parameter
    fn __setitem__(mut self, value: T):
        if is_mutable:
            self.ptr[] = value
```
