# Mojo Built-ins Reference Guide

This document provides a concise reference of the built-in types, traits, and functions in Mojo. These are available without needing to import them.

## Table of Contents

- [Basic Types](#basic-types)
- [Numerical Operations](#numerical-operations)
- [Core Traits](#core-traits)
- [Core Functions](#core-functions)
- [Collections and Iteration](#collections-and-iteration)
- [String Operations](#string-operations)
- [Error Handling](#error-handling)
- [Type System](#type-system)

## Basic Types

### Bool

A primitive boolean scalar value.

```mojo
var x: Bool = True
var y: Bool = False
```

Methods:
- `__bool__()`: Convert to Bool (identity)
- `__int__()`: Convert to Int (1 for True, 0 for False)
- `__float__()`: Convert to Float64 (1.0 for True, 0.0 for False)
- `__str__()`: Convert to String ("True" or "False")

Operations:
- Logical: `and`, `or`, `not`
- Bitwise: `&`, `|`, `^`, `~`
- Comparison: `==`, `!=`

### Int

Signed integer with platform-specific width.

```mojo
var a: Int = 42
var b: Int = -7
```

Constants:
- `Int.MIN`: Minimum representable integer value
- `Int.MAX`: Maximum representable integer value

Methods:
- `__int__()`: Returns the integer value (identity)
- `__bool__()`: True if non-zero, False otherwise
- `__str__()`: String representation
- `__float__()`: Convert to Float64
- `__abs__()`: Absolute value

Operations:
- Arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Bitwise: `&`, `|`, `^`, `~`, `<<`, `>>`
- Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`

### UInt

Unsigned integer with platform-specific width.

```mojo
var a: UInt = 42
```

Constants:
- `UInt.MIN`: 0
- `UInt.MAX`: Maximum representable unsigned integer value

Methods and operations are similar to Int but with unsigned semantics.

### StringLiteral

Compile-time string constant.

```mojo
var s: StringLiteral = "hello"
```

Methods:
- `byte_length()`: Length in bytes
- `find(substr)`: Find substring position
- `rfind(substr)`: Find substring from end
- `replace(old, new)`: Replace substring
- `join(elements)`: Join elements with this string as separator
- `split(sep)`: Split string by separator
- `strip()`, `lstrip()`, `rstrip()`: Remove whitespace
- `upper()`, `lower()`: Convert case
- `startswith(prefix)`, `endswith(suffix)`: Check prefix/suffix
- `isdigit()`, `isupper()`, `islower()`: Character checks

### DType

Represents data types for SIMD operations.

```mojo
var type_value: DType = DType.float32
```

Common types:
- `DType.bool`
- `DType.int8`, `DType.int16`, `DType.int32`, `DType.int64`
- `DType.uint8`, `DType.uint16`, `DType.uint32`, `DType.uint64`
- `DType.float16`, `DType.float32`, `DType.float64`
- `DType.bfloat16`
- `DType.index`

Methods:
- `is_integral()`: Check if type is integral
- `is_floating_point()`: Check if type is floating point
- `is_signed()`: Check if type is signed
- `is_unsigned()`: Check if type is unsigned
- `sizeof()`: Size in bytes
- `bitwidth()`: Size in bits

### NoneType

Represents absence of a value.

```mojo
var n: NoneType = None
```

Methods:
- `__str__()`: Returns "None"
- `__repr__()`: Returns "None"

### Slice

Represents a slice expression for indexing.

```mojo
var slice_obj = Slice(1, 5)  # Equivalent to [1:5]
```

Methods:
- `indices(length)`: Returns normalized (start, stop, step) tuple

## Numerical Operations

### Math Functions

```mojo
abs(x)         # Absolute value
min(x, y)      # Minimum of values
max(x, y)      # Maximum of values
pow(base, exp) # base raised to power exp
round(x)       # Round to nearest integer
divmod(a, b)   # Return (a//b, a%b)
```

## Core Traits

### Type System Traits

```mojo
trait Movable:
    fn __moveinit__(out self, owned existing: Self)

trait Copyable:
    fn __copyinit__(out self, existing: Self)

trait ExplicitlyCopyable:
    fn copy(self) -> Self

trait Defaultable:
    fn __init__(out self)

trait CollectionElement(Copyable, Movable): pass
```

### Operator Traits

```mojo
trait Boolable:
    fn __bool__(self) -> Bool

trait ImplicitlyBoolable(Boolable):
    fn __as_bool__(self) -> Bool

trait Comparable(EqualityComparable, LessThanComparable, ...): pass

trait EqualityComparable:
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool

trait Stringable:
    fn __str__(self) -> String

trait StringableRaising:
    fn __str__(self) raises -> String

trait Representable:
    fn __repr__(self) -> String

trait Intable:
    fn __int__(self) -> Int

trait IntableRaising:
    fn __int__(self) raises -> Int

trait Floatable:
    fn __float__(self) -> Float64

trait FloatableRaising:
    fn __float__(self) raises -> Float64

trait Indexer:
    fn __index__(self) -> __mlir_type.index
```

### Collection Traits

```mojo
trait Sized:
    fn __len__(self) -> Int

trait SizedRaising:
    fn __len__(self) raises -> Int

trait UIntSized:
    fn __len__(self) -> UInt

trait ReversibleRange:
    fn __reversed__(self) -> _StridedRange
```

### IO Traits

```mojo
trait Writable:
    fn write_to[W: Writer](self, mut writer: W)

trait Writer:
    fn write_bytes(mut self, bytes: Span[Byte, _])
```

## Core Functions

### Input/Output

```mojo
print(*values, sep=" ", end="\n", flush=False, file=stdout)
input(prompt="") raises -> String
```

### Type Conversion

```mojo
str(value) -> String                 # Convert to String (deprecated, use String constructor)
repr(value) -> String                # Get representation
int(value) -> Int                    # Convert to Int (deprecated, use Int constructor)
float(value) -> Float64              # Convert to Float (deprecated, use Float64 constructor)
bool(value) -> Bool                  # Convert to Bool (deprecated, use Bool constructor)
```

### Sequence Operations

```mojo
len(obj) -> Int                      # Length of object
range(end) -> Range                  # Range from 0 to end-1
range(start, end) -> Range           # Range from start to end-1
range(start, end, step) -> Range     # Range with custom step
reversed(obj) -> Iterator            # Reversed iterator
sort(array, cmp_fn=None, stable=False) # Sort in-place
```

### Memory Operations

```mojo
swap(mut a, mut b)                   # Swap values
rebind[dest_type](src) -> dest_type  # Convert between types
```

### Binary String Representation

```mojo
bin(num, prefix="0b") -> String      # Binary representation
hex(num, prefix="0x") -> String      # Hexadecimal representation
oct(num, prefix="0o") -> String      # Octal representation
```

### Logic Operations

```mojo
any(iterable) -> Bool                # True if any element is truthy
all(iterable) -> Bool                # True if all elements are truthy
```

## Collections and Iteration

### Tuple

Fixed-size heterogeneous collection.

```mojo
var t = Tuple(1, "hello", True)
```

Methods:
- `__len__()`: Number of elements
- `__getitem__[idx: Int]()`: Access element by index
- `__contains__()`: Check if value is in tuple

### ListLiteral

List literal expression type.

```mojo
var list = [1, 2, 3]  # Type is ListLiteral
```

Methods:
- `__len__()`: Number of elements
- `get[i, T]()`: Get element at index with type T

### Range

Iterator for numeric sequences.

```mojo
for i in range(10): print(i)        # 0 to 9
for i in range(5, 10): print(i)     # 5 to 9
for i in range(0, 10, 2): print(i)  # 0, 2, 4, 6, 8
```

Methods:
- `__iter__()`: Get iterator
- `__len__()`: Number of elements
- `__getitem__()`: Access element by index

## String Operations

String operations (available on StringLiteral):

```mojo
"hello".byte_length()                # Length in bytes
"hello".find("l")                    # Position of substring
"hello".replace("l", "x")            # Replace substring
",".join(["a", "b", "c"])            # Join elements with delimiter
"a,b,c".split(",")                   # Split string by delimiter
"  hello  ".strip()                  # Remove whitespace
"hello".upper()                      # Convert to uppercase
"HELLO".lower()                      # Convert to lowercase
"hello".startswith("he")             # Check prefix
"hello".endswith("lo")               # Check suffix
"123".isdigit()                      # Check if all digits
```

## Error Handling

### Error

Represents an error with a message.

```mojo
raise Error("Something went wrong")

try:
    # Code that might raise
except e:
    print(e)  # Print error message
```

Methods:
- `__str__()`: Error message
- `__bool__()`: True if error is set
- `unsafe_cstr_ptr()`: Get C-string pointer

## Type System

### Type Constraints

```mojo
constrained[cond: Bool, msg: StringLiteral = "param assertion failed"]()
```

Constrains parameters at compile-time.

### Origin System

```mojo
alias ImmutableOrigin = Origin[False]
alias MutableOrigin = Origin[True]
alias ImmutableAnyOrigin = __mlir_attr.`#lit.any.origin : !lit.origin<0>`
alias MutableAnyOrigin = __mlir_attr.`#lit.any.origin : !lit.origin<1>`
```

Origins track mutability and provide memory safety.

### Type Rebinding

```mojo
rebind[dest_type](src) -> dest_type
```

Converts between types at a low level.
