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
- [SIMD Types and Operations](#simd-types-and-operations)
- [Floating Point Types](#floating-point-types)

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

### Integer Types

Mojo provides fixed-width integer types:

```mojo
Int8, UInt8       # 8-bit signed/unsigned integer
Int16, UInt16     # 16-bit signed/unsigned integer
Int32, UInt32     # 32-bit signed/unsigned integer
Int64, UInt64     # 64-bit signed/unsigned integer
Int128, UInt128   # 128-bit signed/unsigned integer
Int256, UInt256   # 256-bit signed/unsigned integer
```

Each of these types supports standard integer operations and constants.

### Byte

Alias for UInt8, represents a single byte of data.

```mojo
var b: Byte = 65  # Same as UInt8(65)
```

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

trait Absable:
    fn __abs__(self) -> Self

trait Hashable:
    fn __hash__(self) -> UInt

trait Ceilable:
    fn __ceil__(self) -> Self

trait CeilDivable:
    fn __ceildiv__(self, denominator: Self) -> Self

trait Floorable:
    fn __floor__(self) -> Self

trait Roundable:
    fn __round__(self) -> Self
    fn __round__(self, ndigits: Int) -> Self
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

## SIMD Types and Operations

### Scalar

The Scalar type represents a single-element SIMD vector:

```mojo
Scalar[DType.float32]  # Single-precision float scalar
Scalar[DType.int32]    # 32-bit integer scalar
```

Scalar is a specialization of the SIMD type with size=1.

### SIMD

SIMD (Single Instruction Multiple Data) enables parallel operations on vectors of data.

```mojo
# Create a SIMD vector with 4 float32 elements
var v = SIMD[DType.float32, 4](1.0, 2.0, 3.0, 4.0)
```

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

Standard IEEE 754 floating-point types:

```mojo
var f16 = Float16(1.5)    # 16-bit half precision
var f32 = Float32(3.14)   # 32-bit single precision
var f64 = Float64(2.718)  # 64-bit double precision
```

### BFloat16

Brain floating-point format (bfloat16) optimized for machine learning applications:

```mojo
var bf16 = BFloat16(1.5)  # 16-bit brain floating point
```

Compared to Float16, BFloat16 has fewer mantissa bits but the same exponent range as Float32.

### Float8 Formats

Mojo supports several 8-bit floating point formats:

```mojo
var e5m2 = Float8_e5m2(1.0)           # 1-bit sign, 5-bit exponent, 2-bit mantissa
var e4m3 = Float8_e4m3fn(0.5)         # 1-bit sign, 4-bit exponent, 3-bit mantissa, finite only
var e5m2fnuz = Float8_e5m2fnuz(0.25)  # e5m2 with finite-only, unsigned-zero
var e4m3fnuz = Float8_e4m3fnuz(0.125) # e4m3 with finite-only, unsigned-zero
```

These 8-bit formats provide more compact storage for applications where reduced precision is acceptable, such as in certain machine learning workloads.
