# Mojo Built-ins Reference Guide

This document provides a comprehensive reference of all built-in types, methods, traits, and functions in Mojo. For language syntax and programming patterns, see the [Mojo Language Guide](mojo-language-guide.md).

## Table of Contents

- [Basic Types](#basic-types)
- [Numerical Operations](#numerical-operations)
- [Core Traits](#core-traits)
- [Core Functions](#core-functions)
- [Collections and Iteration](#collections-and-iteration)
- [String Operations](#string-operations)
- [Error Handling](#error-handling)
- [SIMD Types and Operations](#simd-types-and-operations)
- [Floating Point Types](#floating-point-types)

## Basic Types

### Bool

A primitive boolean scalar value.

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

Constants:
- `UInt.MIN`: 0
- `UInt.MAX`: Maximum representable unsigned integer value

Methods and operations are similar to Int but with unsigned semantics.

### Integer Types

Mojo provides fixed-width integer types:

- `Int8, UInt8`: 8-bit signed/unsigned integer
- `Int16, UInt16`: 16-bit signed/unsigned integer
- `Int32, UInt32`: 32-bit signed/unsigned integer
- `Int64, UInt64`: 64-bit signed/unsigned integer
- `Int128, UInt128`: 128-bit signed/unsigned integer
- `Int256, UInt256`: 256-bit signed/unsigned integer

Each of these types supports standard integer operations and constants.

### Byte

Alias for UInt8, represents a single byte of data.

### StringLiteral

Compile-time string constant.

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

Common types:
- `DType.bool`
- `DType.int8`, `DType.int16`, `DType.int32`, `DType.int64`
- `DType.uint8`, `DType.uint16`, `DType.uint32`, `DType.uint64`
- `DType.int128`, `DType.uint128`
- `DType.int256`, `DType.uint256`
- `DType.float16`, `DType.float32`, `DType.float64`
- `DType.bfloat16`
- `DType.float8_e5m2`, `DType.float8_e4m3fn`
- `DType.float8_e5m2fnuz`, `DType.float8_e4m3fnuz`
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

Methods:
- `__str__()`: Returns "None"
- `__repr__()`: Returns "None"

### Slice

Represents a slice expression for indexing.

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

### Common Traits

```mojo
trait Copyable:
    fn __copyinit__(out self, existing: Self)

trait Movable:
    fn __moveinit__(out self, owned existing: Self)

trait Defaultable:
    fn __init__(out self)

trait Comparable: pass

trait Stringable:
    fn __str__(self) -> String

trait Representable:
    fn __repr__(self) -> String

trait Hashable:
    fn __hash__(self) -> UInt
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

Methods:
- `__len__()`: Number of elements
- `__getitem__[idx: Int]()`: Access element by index
- `__contains__()`: Check if value is in tuple

### ListLiteral

List literal expression type.

Methods:
- `__len__()`: Number of elements
- `get[i, T]()`: Get element at index with type T

### Range

Iterator for numeric sequences.

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

Methods:
- `__str__()`: Error message
- `__bool__()`: True if error is set

## SIMD Types and Operations

### Scalar

The Scalar type represents a single-element SIMD vector:

Scalar is a specialization of the SIMD type with size=1.

### SIMD

SIMD (Single Instruction Multiple Data) enables parallel operations on vectors of data.

#### Initialization

```mojo
# Default initialization (zeros)
var v1 = SIMD[DType.int32, 4]()

# Value broadcast
var v2 = SIMD[DType.float32, 4](3.14)

# Element-wise initialization
var v3 = SIMD[DType.int8, 4](1, 2, 3, 4)

# Cast from another SIMD
var v4 = SIMD[DType.int16, 4](v3)

# From bits
var v5 = SIMD[DType.float32, 1].from_bits(SIMD[DType.uint32, 1](0x3f800000))
```

#### Constants
```mojo
SIMD[DType.float32, 4].MAX       # Maximum representable value (or +inf)
SIMD[DType.float32, 4].MIN       # Minimum representable value (or -inf)
SIMD[DType.float32, 4].MAX_FINITE # Maximum finite value
SIMD[DType.float32, 4].MIN_FINITE # Minimum finite value
```

#### Element Access
```mojo
var x = v[2]  # Get element at index 2
v[1] = 42     # Set element at index 1
```

#### Arithmetic Operations
```mojo
var sum = v1 + v2        # Element-wise addition
var diff = v1 - v2       # Element-wise subtraction
var prod = v1 * v2       # Element-wise multiplication
var quot = v1 / v2       # Element-wise division
var fdiv = v1 // v2      # Element-wise floor division
var mod = v1 % v2        # Element-wise modulo
var neg = -v1            # Element-wise negation
var pow = v1**2          # Element-wise power
```

#### Comparison Operations
```mojo
var eq = v1 == v2        # Element-wise equality
var ne = v1 != v2        # Element-wise inequality
var lt = v1 < v2         # Element-wise less than
var le = v1 <= v2        # Element-wise less than or equal
var gt = v1 > v2         # Element-wise greater than
var ge = v1 >= v2        # Element-wise greater than or equal
```

#### Bitwise Operations
```mojo
var and_result = v1 & v2  # Element-wise AND
var or_result = v1 | v2   # Element-wise OR
var xor_result = v1 ^ v2  # Element-wise XOR
var not_result = ~v1      # Element-wise NOT
var shl = v1 << SIMD[DType.int32, 4](2)  # Element-wise left shift
var shr = v1 >> SIMD[DType.int32, 4](2)  # Element-wise right shift
```

#### Special Methods
```mojo
v.cast[DType.float64]()       # Cast to different element type
v.to_bits()                   # Convert to integer representation
v.clamp(min_val, max_val)     # Clamp values to range
v.fma(multiplier, acc)        # Fused multiply-add

# Mathematical functions
v.__abs__()                   # Element-wise absolute value
v.__floor__()                 # Element-wise floor
v.__ceil__()                  # Element-wise ceiling
v.__trunc__()                 # Element-wise truncation
v.__round__()                 # Element-wise rounding
v.roundeven()                 # Element-wise banker's rounding
```

#### Vector Manipulation
```mojo
# Slicing
var slice = v.slice[2, offset=1]()    # Extract 2 elements starting at index 1

# Insertion
var new_v = v.insert[offset=1](SIMD[DType.float32, 2](5.0, 6.0))

# Combining vectors
var joined = v1.join(v2)              # Concatenate two vectors
var interleaved = v1.interleave(v2)   # Interleave elements

# Splitting and deinterleaving
var halves = v.split()                # Split into two halves
var even_odd = v.deinterleave()       # Separate even and odd elements

# Element reordering
var mask = IndexList[4](3, 2, 1, 0)
var reversed = v.shuffle[mask]()      # Reverse order of elements
var rotated = v.rotate_left[1]()      # Rotate elements left
var shifted = v.shift_right[2]()      # Shift elements right, filling with zeros
```

#### Reduction Operations
```mojo
var sum = v.reduce_add()       # Sum of all elements
var product = v.reduce_mul()   # Product of all elements
var maximum = v.reduce_max()   # Maximum element
var minimum = v.reduce_min()   # Minimum element
var all_true = v.reduce_and()  # Logical AND of all elements
var any_true = v.reduce_or()   # Logical OR of all elements
var bit_count = v.reduce_bit_count() # Count of set bits across all elements
```

#### Conditional Operations
```mojo
var mask = SIMD[DType.bool, 4](True, False, True, False)
var result = mask.select(v1, v2)  # Select from v1 or v2 based on mask
```

## Floating Point Types

Mojo supports various floating-point formats:

### Float16, Float32, Float64

Standard IEEE 754 floating-point types.

### BFloat16

Brain floating-point format (bfloat16) optimized for machine learning applications.

Compared to Float16, BFloat16 has fewer mantissa bits but the same exponent range as Float32.

### Float8 Formats

Mojo supports several 8-bit floating point formats:

- `Float8_e5m2`: 1-bit sign, 5-bit exponent, 2-bit mantissa
- `Float8_e4m3fn`: 1-bit sign, 4-bit exponent, 3-bit mantissa, finite only
- `Float8_e5m2fnuz`: e5m2 with finite-only, unsigned-zero
- `Float8_e4m3fnuz`: e4m3 with finite-only, unsigned-zero

These 8-bit formats provide more compact storage for applications where reduced precision is acceptable, such as in certain machine learning workloads.
