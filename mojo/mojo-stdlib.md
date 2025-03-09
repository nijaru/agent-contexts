# Mojo Standard Library Documentation

## Table of Contents

- [base64](#base64)
- [bit](#bit)
- [collections](#collections)
- [hashlib](#hashlib)
- [math](#math)
- [memory](#memory)
- [os](#os)
- [pathlib](#pathlib)
- [pwd](#pwd)
- [python](#python)
- [random](#random)
- [stat](#stat)
- [sys](#sys)
- [tempfile](#tempfile)
- [testing](#testing)
- [time](#time)
- [utils](#utils)

## base64

Provides functions for Base64 and Base16 encoding and decoding.

### Functions

```mojo
fn b64encode(input_bytes: Span[Byte, _]) -> String
fn b64encode(input_string: StringSlice) -> String
fn b64decode[validate: Bool = False](str: StringSlice) raises -> String
fn b16encode(str: StringSlice) -> String
fn b16decode(str: StringSlice) -> String
```

## bit

Provides bit manipulation utilities.

### Functions

```mojo
# Counting zeros
fn count_leading_zeros(val: Int) -> Int
fn count_leading_zeros[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn count_trailing_zeros(val: Int) -> Int
fn count_trailing_zeros[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Bit reversing and swapping
fn bit_reverse(val: Int) -> Int
fn bit_reverse[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn byte_swap(val: Int) -> Int
fn byte_swap[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Bit counting and operations
fn pop_count(val: Int) -> Int
fn pop_count[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn bit_not[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn bit_width(val: Int) -> Int
fn bit_width[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Power of 2 functions
fn log2_floor(val: Int) -> Int
fn is_power_of_two(val: Int) -> Bool
fn is_power_of_two[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[DType.bool, width]
fn next_power_of_two(val: Int) -> Int
fn next_power_of_two[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn prev_power_of_two(val: Int) -> Int
fn prev_power_of_two[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Bit rotation
fn rotate_bits_left[shift: Int](x: Int) -> Int
fn rotate_bits_left[type: DType, width: Int, shift: Int](x: SIMD[type, width]) -> SIMD[type, width]
fn rotate_bits_right[shift: Int](x: Int) -> Int
fn rotate_bits_right[type: DType, width: Int, shift: Int](x: SIMD[type, width]) -> SIMD[type, width]
```

## collections

Provides collection data types for storing and manipulating data.

### Types and Traits

```mojo
trait KeyElement(CollectionElement, Hashable, EqualityComparable):
    # Trait for types that can be used as dictionary keys

trait IntervalElement(CollectionElement, Writable, Intable, Comparable, _CopyableGreaterThanComparable):
    # Trait for interval bounds
    fn __sub__(self, rhs: Self) -> Self

trait IntervalPayload(CollectionElement, Stringable, Comparable):
    # Trait for data associated with intervals
```

### Counter

```mojo
struct Counter[V: KeyElement](Sized, CollectionElement, Boolable):
    # Constructors
    fn __init__(out self)  # Create empty Counter
    fn __init__(out self, items: List[V, *_])  # Create from list of items
    fn copy(self) -> Self  # Create a copy

    # Static methods
    fn fromkeys(keys: List[V, *_], value: Int) -> Self

    # Operators
    fn __getitem__(self, key: V) -> Int  # Get count of key
    fn __setitem__(mut self, value: V, count: Int)  # Set count for value
    fn __iter__(self) -> _  # Return iterator over keys
    fn __contains__(self, key: V) -> Bool
    fn __len__(self) -> Int
    fn __bool__(self) -> Bool
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool
    fn __le__(self, other: Self) -> Bool  # Check if all counts are less than or equal
    fn __lt__(self, other: Self) -> Bool  # Check if all counts are less than
    fn __gt__(self, other: Self) -> Bool
    fn __ge__(self, other: Self) -> Bool
    fn __add__(self, other: Self) -> Self  # Add counts
    fn __iadd__(mut self, other: Self)  # Add counts in place
    fn __sub__(self, other: Self) -> Self  # Subtract counts
    fn __isub__(mut self, other: Self)  # Subtract counts in place
    fn __and__(self, other: Self) -> Self  # Intersection: minimum counts
    fn __iand__(mut self, other: Self)
    fn __or__(self, other: Self) -> Self  # Union: maximum counts
    fn __ior__(mut self, other: Self)
    fn __pos__(self) -> Self  # Return copy with positive counts
    fn __neg__(self) -> Self  # Return copy with negative counts flipped

    # Methods
    fn get(self, value: V) -> Optional[Int]
    fn get(self, value: V, default: Int) -> Int
    fn pop(mut self, value: V) raises -> Int
    fn pop(mut self, value: V, owned default: Int) raises -> Int
    fn keys(ref self) -> _  # Return iterator over keys
    fn values(ref self) -> _  # Return iterator over values
    fn items(self) -> _  # Return iterator over items
    fn clear(mut self)
    fn popitem(mut self) raises -> CountTuple[V]
    fn total(self) -> Int  # Sum of all counts
    fn most_common(self, n: Int) -> List[CountTuple[V]]
    fn elements(self) -> List[V]  # Expand each element based on its count
    fn update(mut self, other: Self)  # Add counts from other
    fn subtract(mut self, other: Self)  # Subtract counts from other

struct CountTuple[V: KeyElement](CollectionElement):
    # Fields
    var _value: V
    var _count: Int

    # Methods
    fn __getitem__(self, idx: Int) -> Variant[V, Int]
```

### Deque

```mojo
struct Deque[ElementType: CollectionElement](Movable, ExplicitlyCopyable, Sized, Boolable):
    # A double-ended queue implementation

    # Constructors
    fn __init__(out self, *, owned elements: Optional[List[ElementType]] = None,
                capacity: Int = default_capacity, min_capacity: Int = default_capacity,
                maxlen: Int = -1, shrink: Bool = True)
    fn __init__(out self, owned *values: ElementType)
    fn copy(self) -> Self

    # Operators
    fn __add__(self, other: Self) -> Self
    fn __iadd__(mut self, other: Self)
    fn __mul__(self, n: Int) -> Self
    fn __imul__(mut self, n: Int)
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool
    fn __contains__(self, value: ElementType) -> Bool
    fn __iter__(ref self) -> _  # Return iterator
    fn __reversed__(ref self) -> _  # Return reversed iterator
    fn __bool__(self) -> Bool
    fn __len__(self) -> Int
    fn __getitem__(ref self, idx: Int) -> ref [self] ElementType

    # Methods
    fn append(mut self, owned value: ElementType)  # Add to right side
    fn appendleft(mut self, owned value: ElementType)  # Add to left side
    fn clear(mut self)  # Remove all elements
    fn count(self, value: ElementType) -> Int
    fn extend(mut self, owned values: List[ElementType])  # Add all elements to right
    fn extendleft(mut self, owned values: List[ElementType])  # Add all elements to left (reversed)
    fn index(self, value: ElementType, start: Int = 0, stop: Optional[Int] = None) raises -> Int
    fn insert(mut self, idx: Int, owned value: ElementType) raises  # Insert at index
    fn remove(mut self, value: ElementType) raises  # Remove first occurrence
    fn peek(self) raises -> ElementType  # Get rightmost element without removing
    fn peekleft(self) raises -> ElementType  # Get leftmost element without removing
    fn pop(mut self) raises -> ElementType  # Remove and return rightmost element
    fn popleft(mut self) raises -> ElementType  # Remove and return leftmost element
    fn reverse(mut self)  # Reverse in place
    fn rotate(mut self, n: Int = 1)  # Rotate n steps right (negative = left)
```

### Dict

```mojo
struct Dict[K: KeyElement, V: CollectionElement](Sized, CollectionElement, CollectionElementNew, Boolable):
    # A dictionary mapping keys to values

    # Constructors
    fn __init__(out self)  # Empty dictionary
    fn __init__(out self, *, power_of_two_initial_capacity: Int)  # Pre-reserved capacity
    fn copy(self) -> Self

    # Static methods
    fn fromkeys(keys: List[K, *_], value: V) -> Self
    fn fromkeys(keys: List[K, *_], value: Optional[V] = None) -> Dict[K, Optional[V]]

    # Operators
    fn __getitem__(self, key: K) raises -> ref V
    fn __setitem__(mut self, owned key: K, owned value: V)
    fn __contains__(self, key: K) -> Bool
    fn __iter__(ref self) -> _  # Return iterator over keys
    fn __reversed__(ref self) -> _  # Return reversed iterator over keys
    fn __or__(self, other: Self) -> Self  # Merge dictionaries
    fn __ior__(mut self, other: Self)  # Update with other dictionary
    fn __len__(self) -> Int
    fn __bool__(self) -> Bool

    # Methods
    fn find(self, key: K) -> Optional[V]  # Find value by key
    fn get_ptr(ref self, key: K) -> Optional[Pointer[V, _]]
    fn get(self, key: K) -> Optional[V]
    fn get(self, key: K, default: V) -> V
    fn pop(mut self, key: K, owned default: V) -> V
    fn pop(mut self, key: K) raises -> V
    fn popitem(mut self) raises -> DictEntry[K, V]
    fn keys(ref self) -> _  # Return iterator over keys
    fn values(ref self) -> _  # Return iterator over values
    fn items(ref self) -> _  # Return iterator over items
    fn update(mut self, other: Self)
    fn clear(mut self)
    fn setdefault(mut self, key: K, owned default: V) raises -> ref V
```

### InlineArray

```mojo
struct InlineArray[ElementType: CollectionElement, size: Int, *, run_destructors: Bool = False](Sized, Movable, Copyable, ExplicitlyCopyable):
    # A fixed-size array with compile-time size checking

    # Constructors
    fn __init__(out self, *, uninitialized: Bool)
    fn __init__(out self, *, owned unsafe_assume_initialized: InlineArray[UnsafeMaybeUninitialized[ElementType], size])
    fn __init__(out self, fill: ElementType)
    fn __init__(out self, owned *elems: ElementType)
    fn copy(self) -> Self

    # Operators
    fn __getitem__(ref self, idx: I) -> ref [self] ElementType
    fn __contains__(self, value: ElementType) -> Bool

    # Methods
    fn __len__(self) -> Int
    fn unsafe_get(ref self, idx: Int) -> ref [self] ElementType  # No bounds checking
    fn unsafe_ptr(ref self) -> UnsafePointer[ElementType, ...]
```

### Interval & IntervalTree

```mojo
struct Interval[T: IntervalElement](CollectionElement):
    # A half-open interval [start, end)

    # Fields
    var start: T  # Inclusive start
    var end: T  # Exclusive end

    # Constructors
    fn __init__(out self, start: T, end: T)
    fn __init__(out self, interval: Tuple[T, T])

    # Operators
    fn __contains__(self, other: T) -> Bool
    fn __contains__(self, other: Self) -> Bool
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool
    fn __le__(self, other: Self) -> Bool
    fn __ge__(self, other: Self) -> Bool
    fn __lt__(self, other: Self) -> Bool
    fn __gt__(self, other: Self) -> Bool
    fn __len__(self) -> Int
    fn __bool__(self) -> Bool

    # Methods
    fn overlaps(self, other: Self) -> Bool
    fn union(self, other: Self) -> Self
    fn intersection(self, other: Self) -> Self

struct IntervalTree[T: IntervalElement, U: IntervalPayload]:
    # An interval tree for efficient range queries

    # Constructors
    fn __init__(out self)

    # Methods
    fn insert(mut self, interval: Tuple[T, T], data: U)
    fn insert(mut self, interval: Interval[T], data: U)
    fn search(self, interval: Tuple[T, T]) raises -> List[U]
    fn search(self, interval: Interval[T]) raises -> List[U]
    fn depth(self) -> Int
```

### LinkedList

```mojo
struct LinkedList[ElementType: CollectionElement]:
    # A doubly-linked list

    # Constructors
    fn __init__(out self)
    fn __init__(mut self, owned *elements: ElementType)
    fn __copyinit__(mut self, read other: Self)
    fn copy(self) -> Self

    # Operators
    fn __len__(self) -> Int
    fn __bool__(self) -> Bool
    fn __getitem__(ref self, index: Int) -> ref [self] ElementType
    fn __setitem__(mut self, index: Int, owned value: ElementType)
    fn __iter__(self) -> _  # Return iterator
    fn __reversed__(self) -> _  # Return reversed iterator
    fn __contains__(self, value: ElementType) -> Bool
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool

    # Methods
    fn append(mut self, owned value: ElementType)
    fn prepend(mut self, owned value: ElementType)
    fn reverse(mut self)
    fn pop(mut self) raises -> ElementType
    fn pop(mut self, owned i: Int) raises -> ElementType
    fn maybe_pop(mut self) -> Optional[ElementType]
    fn maybe_pop(mut self, owned i: Int) -> Optional[ElementType]
    fn clear(mut self)
    fn insert(mut self, idx: Int, owned elem: ElementType) raises
    fn extend(mut self, owned other: Self)
    fn count(self, read elem: ElementType) -> UInt
```

### List

```mojo
struct List[T: CollectionElement, hint_trivial_type: Bool = False](CollectionElement, CollectionElementNew, Sized, Boolable):
    # A dynamically-allocated list

    # Constructors
    fn __init__(out self)
    fn __init__(out self, *, capacity: Int)
    fn __init__(out self, owned *values: T)
    fn __init__(out self, span: Span[T])
    fn copy(self) -> Self

    # Operators
    fn __mul__(self, x: Int) -> Self
    fn __imul__(mut self, x: Int)
    fn __add__(self, owned other: Self) -> Self
    fn __iadd__(mut self, owned other: Self)
    fn __iter__(ref self) -> _  # Return iterator
    fn __reversed__(ref self) -> _  # Return reversed iterator
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool
    fn __contains__(self, value: T) -> Bool
    fn __len__(self) -> Int
    fn __bool__(self) -> Bool
    fn __getitem__(self, span: Slice) -> Self
    fn __getitem__(ref self, idx: Int) -> ref [self] T

    # Methods
    fn byte_length(self) -> Int
    fn append(mut self, owned value: T)
    fn insert(mut self, i: Int, owned value: T)
    fn extend(mut self, owned other: List[T, *_])
    fn extend(mut self, value: SIMD[DType, _])
    fn extend(mut self, value: Span[Scalar[DType]])
    fn pop(mut self, i: Int = -1) -> T
    fn reserve(mut self, new_capacity: Int)
    fn resize(mut self, new_size: Int, value: T)
    fn resize(mut self, new_size: Int)
    fn reverse(mut self)
    fn index(ref self, value: T, start: Int = 0, stop: Optional[Int] = None) raises -> Int
    fn count(self, value: T) -> Int
    fn swap_elements(mut self, elt_idx_1: Int, elt_idx_2: Int)
    fn clear(mut self)
    fn steal_data(mut self) -> UnsafePointer[T]
    fn unsafe_get(ref self, idx: Int) -> ref [self] T
    fn unsafe_set(mut self, idx: Int, owned value: T)
    fn unsafe_ptr(ref self) -> UnsafePointer[T, ...]
```

### Optional

```mojo
struct Optional[T: CollectionElement](CollectionElement, CollectionElementNew, Boolable):
    # A type modeling a value which may or may not be present

    # Constructors
    fn __init__(out self)  # Empty optional
    fn __init__(out self, owned value: T)  # With value
    fn __init__(out self, value: NoneType)  # Empty optional
    fn copy(self) -> Self

    # Operators
    fn __is__(self, other: NoneType) -> Bool
    fn __isnot__(self, other: NoneType) -> Bool
    fn __eq__(self, rhs: NoneType) -> Bool
    fn __eq__(self, rhs: Optional[T]) -> Bool
    fn __ne__(self, rhs: NoneType) -> Bool
    fn __ne__(self, rhs: Optional[T]) -> Bool
    fn __bool__(self) -> Bool
    fn __invert__(self) -> Bool

    # Methods
    fn value(ref self) -> ref [self._value] T  # Get value or abort
    fn unsafe_value(ref self) -> ref [self._value] T  # Get value without check
    fn take(mut self) -> T  # Move value out
    fn unsafe_take(mut self) -> T  # Move value out without check
    fn or_else(self, default: T) -> T  # Get value or default
    fn copied(self) -> Optional[T]  # Convert Optional[Pointer[T]] to Optional[T]

struct OptionalReg[T: AnyTrivialRegType](Boolable):
    # A register-passable optional type

    # Constructors
    fn __init__(out self)
    fn __init__(out self, value: T)
    fn __init__(out self, value: NoneType)

    # Operators
    fn __is__(self, other: NoneType) -> Bool
    fn __isnot__(self, other: NoneType) -> Bool
    fn __bool__(self) -> Bool

    # Methods
    fn value(self) -> T
    fn or_else(owned self, owned default: T) -> T
```

### Set

```mojo
struct Set[T: KeyElement](Sized, Comparable, Hashable, Boolable):
    # A set data type

    # Constructors
    fn __init__(out self, *ts: T)
    fn __init__(out self, elements: Self)
    fn __init__(out self, elements: List[T, *_])

    # Operators
    fn __contains__(self, t: T) -> Bool
    fn __eq__(self, other: Self) -> Bool
    fn __ne__(self, other: Self) -> Bool
    fn __and__(self, other: Self) -> Self  # Intersection
    fn __iand__(mut self, other: Self)  # In-place intersection
    fn __or__(self, other: Self) -> Self  # Union
    fn __ior__(mut self, other: Self)  # In-place union
    fn __sub__(self, other: Self) -> Self  # Difference
    fn __isub__(mut self, other: Self)  # In-place difference
    fn __le__(self, other: Self) -> Bool  # Subset check
    fn __ge__(self, other: Self) -> Bool  # Superset check
    fn __gt__(self, other: Self) -> Bool  # Strict superset check
    fn __lt__(self, other: Self) -> Bool  # Strict subset check
    fn __xor__(self, other: Self) -> Self  # Symmetric difference
    fn __ixor__(mut self, other: Self)  # In-place symmetric difference
    fn __bool__(self) -> Bool
    fn __len__(self) -> Int
    fn __hash__(self) -> UInt

    # Methods
    fn __iter__(ref self) -> _  # Return iterator
    fn add(mut self, t: T)
    fn remove(mut self, t: T) raises
    fn pop(mut self) raises -> T
    fn union(self, other: Self) -> Self
    fn intersection(self, other: Self) -> Self
    fn difference(self, other: Self) -> Self
    fn update(mut self, other: Self)
    fn intersection_update(mut self, other: Self)
    fn difference_update(mut self, other: Self)
    fn issubset(self, other: Self) -> Bool
    fn isdisjoint(self, other: Self) -> Bool
    fn issuperset(self, other: Self) -> Bool
    fn symmetric_difference(self, other: Self) -> Self
    fn symmetric_difference_update(mut self, other: Self)
    fn discard(mut self, value: T)
    fn clear(mut self)
```

## hashlib

Provides hash functions and hashable interfaces.

### Types and Traits

```mojo
trait Hashable:
    # Get the hash value for this object
    fn __hash__(self) -> UInt
```

### Functions

```mojo
# Hash a hashable type
fn hash[T: Hashable](hashable: T) -> UInt

# Hash a byte array
fn hash(bytes: UnsafePointer[UInt8], n: Int) -> UInt
```

## math

Provides mathematical constants, functions, and utilities.

### Constants

```mojo
alias pi = 3.1415926535897932384626433832795028841971693993751058209749445923
alias e = 2.7182818284590452353602874713526624977572470936999595749669676277
alias tau = 2 * pi
```

### Traits

```mojo
trait Floorable:
    fn __floor__(self) -> Self

trait Ceilable:
    fn __ceil__(self) -> Self

trait CeilDivable:
    fn __ceildiv__(self, denominator: Self) -> Self

trait Truncable:
    fn __trunc__(self) -> Self
```

### Functions

```mojo
# Basic rounding operations
fn floor[T: Floorable](value: T) -> T
fn ceil[T: Ceilable](value: T) -> T
fn ceildiv[T: CeilDivable](numerator: T, denominator: T) -> T
fn trunc[T: Truncable](value: T) -> T

# Root functions
fn sqrt(x: Int) -> Int
fn sqrt[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn isqrt(x: SIMD) -> __type_of(x)
fn cbrt(x: SIMD) -> __type_of(x)

# Reciprocal
fn recip(x: SIMD) -> __type_of(x)

# Exponential functions
fn exp2[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn exp[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn expm1(x: SIMD) -> __type_of(x)

# Logarithmic functions
fn log(x: SIMD) -> __type_of(x)
fn log2(x: SIMD) -> __type_of(x)
fn log10(x: SIMD) -> __type_of(x)
fn log1p(x: SIMD) -> __type_of(x)
fn logb(x: SIMD) -> __type_of(x)

# Trigonometric functions
fn sin[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn cos[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn tan(x: SIMD) -> __type_of(x)
fn asin(x: SIMD) -> __type_of(x)
fn acos(x: SIMD) -> __type_of(x)
fn atan(x: SIMD) -> __type_of(x)
fn atan2[type: DType, simd_width: Int](y: SIMD[type, simd_width], x: SIMD[type, simd_width]) -> SIMD[type, simd_width]

# Hyperbolic functions
fn sinh(x: SIMD) -> __type_of(x)
fn cosh(x: SIMD) -> __type_of(x)
fn tanh[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn asinh(x: SIMD) -> __type_of(x)
fn acosh(x: SIMD) -> __type_of(x)
fn atanh(x: SIMD) -> __type_of(x)

# Error functions
fn erf[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn erfc(x: SIMD) -> __type_of(x)

# Gamma functions
fn gamma(x: SIMD) -> __type_of(x)
fn lgamma(x: SIMD) -> __type_of(x)

# Bessel functions
fn j0(x: SIMD) -> __type_of(x)
fn j1(x: SIMD) -> __type_of(x)
fn y0(x: SIMD) -> __type_of(x)
fn y1(x: SIMD) -> __type_of(x)

# Utility functions
fn copysign[type: DType, simd_width: Int](magnitude: SIMD[type, simd_width], sign: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn isclose[type: DType, simd_width: Int](a: SIMD[type, simd_width], b: SIMD[type, simd_width], *, atol: Float64 = 1e-08, rtol: Float64 = 1e-05, equal_nan: Bool = False) -> SIMD[DType.bool, simd_width]
fn clamp(val: Int, lower_bound: Int, upper_bound: Int) -> Int
fn clamp(val: SIMD, lower_bound: SIMD, upper_bound: SIMD) -> SIMD

# Integer functions
fn gcd(m: Int, n: Int) -> Int
fn gcd(s: Span[Int]) -> Int
fn gcd(*values: Int) -> Int
fn lcm(m: Int, n: Int) -> Int
fn lcm(s: Span[Int]) -> Int
fn lcm(*values: Int) -> Int
fn factorial(n: Int) -> Int

# Vector and numeric functions
fn iota[type: DType, simd_width: Int](offset: Scalar[type] = 0) -> SIMD[type, simd_width]
fn fma(a: Int, b: Int, c: Int) -> Int
fn fma[type: DType, simd_width: Int](a: SIMD[type, simd_width], b: SIMD[type, simd_width], c: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn frexp[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> StaticTuple[SIMD[type, simd_width], 2]
fn ldexp[type: DType, simd_width: Int](x: SIMD[type, simd_width], exp: SIMD[DType.int32, simd_width]) -> SIMD[type, simd_width]
fn modf(x: SIMD) -> Tuple[__type_of(x), __type_of(x)]

# Alignment functions
fn align_down(value: Int, alignment: Int) -> Int
fn align_up(value: Int, alignment: Int) -> Int

# Other functions
fn hypot[type: DType, simd_width: Int](arg0: SIMD[type, simd_width], arg1: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn remainder[type: DType, simd_width: Int](x: SIMD[type, simd_width], y: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn scalb[type: DType, simd_width: Int](arg0: SIMD[type, simd_width], arg1: SIMD[type, simd_width]) -> SIMD[type, simd_width]

# Polynomial evaluation
fn polynomial_evaluate[dtype: DType, simd_width: Int, coefficients: List[SIMD[dtype, simd_width], *_]](x: SIMD[dtype, simd_width]) -> SIMD[dtype, simd_width]
```

## memory

Provides several pointer types and utility functions for memory management.

### Types

```mojo
struct ArcPointer[T: Movable]
    # Reference-counted pointer that owns an instance of T on the heap
    # Methods
    fn __init__(out self, owned value: T)
    fn copy(self) -> Self
    fn __getitem__[self_life: ImmutableOrigin](ref [self_life]self) -> ref [MutableOrigin.cast_from[self_life].result] T
    fn unsafe_ptr(self) -> UnsafePointer[T]
    fn count(self) -> UInt64
    fn __is__(self, rhs: Self) -> Bool
    fn __isnot__(self, rhs: Self) -> Bool

struct OwnedPointer[T: AnyType]
    # A safe, owning smart pointer
    # Methods
    fn __init__[T: Movable](mut self: OwnedPointer[T], owned value: T)
    fn __init__[T: ExplicitlyCopyable](mut self: OwnedPointer[T], *, copy_value: T)
    fn __init__[T: Copyable, U: NoneType = None](mut self: OwnedPointer[T], value: T)
    fn __init__[T: ExplicitlyCopyable](mut self: OwnedPointer[T], *, other: OwnedPointer[T])
    fn __getitem__(ref [AddressSpace.GENERIC]self) -> ref [self, AddressSpace.GENERIC] T
    fn unsafe_ptr(self) -> UnsafePointer[T]
    fn take[T: Movable](owned self: OwnedPointer[T]) -> T
    fn steal_data(owned self) -> UnsafePointer[T]

struct UnsafeMaybeUninitialized[ElementType: AnyType]
    # A memory location that may or may not be initialized
    # Methods
    fn __init__(out self)
    fn __init__[MovableType: Movable](mut self: UnsafeMaybeUninitialized[MovableType], owned value: MovableType)
    fn copy_from[CopyableType: ExplicitlyCopyable](mut self: UnsafeMaybeUninitialized[CopyableType], other: UnsafeMaybeUninitialized[CopyableType])
    fn copy_from[CopyableType: ExplicitlyCopyable](mut self: UnsafeMaybeUninitialized[CopyableType], other: CopyableType)
    fn move_from[MovableType: Movable](mut self: UnsafeMaybeUninitialized[MovableType], mut other: UnsafeMaybeUninitialized[MovableType])
    fn move_from[MovableType: Movable](mut self: UnsafeMaybeUninitialized[MovableType], other: UnsafePointer[MovableType])
    fn write[MovableType: Movable](mut self: UnsafeMaybeUninitialized[MovableType], owned value: MovableType)
    fn assume_initialized(ref self) -> ref [self] Self.ElementType
    fn unsafe_ptr(self) -> UnsafePointer[Self.ElementType]
    fn assume_initialized_destroy(mut self)

struct Pointer[mut: Bool, type: AnyType, origin: Origin[mut], address_space: AddressSpace = AddressSpace.GENERIC]
    # Non-nullable safe pointer
    # Methods
    fn address_of(ref [origin, address_space]value: type) -> Self
    fn __getitem__(self) -> ref [origin, address_space] type

struct Span[mut: Bool, T: CollectionElement, origin: Origin[mut], *, address_space: AddressSpace = AddressSpace.GENERIC, alignment: Int = _default_alignment[T]()]
    # A non-owning view of contiguous data
    # Methods
    fn __getitem__[I: Indexer](self, idx: I) -> ref [origin, address_space] T
    fn __getitem__(self, slc: Slice) -> Self
    fn __len__(self) -> Int
    fn unsafe_ptr(self) -> UnsafePointer[T, mut=mut, origin=origin, address_space=address_space, alignment=alignment]
    fn as_ref(self) -> Pointer[T, origin, address_space=address_space]
    fn copy_from[origin: MutableOrigin](self: Span[T, origin], other: Span[T, _])
    fn fill[origin: MutableOrigin](self: Span[T, origin], value: T)
    fn get_immutable(self) -> Span[T, ImmutableOrigin.cast_from[origin].result, address_space=address_space, alignment=alignment]

@register_passable("trivial")
struct UnsafePointer[type: AnyType, *, address_space: AddressSpace = AddressSpace.GENERIC, alignment: Int = _default_alignment[type](), mut: Bool = True, origin: Origin[mut] = Origin[mut].cast_from[MutableAnyOrigin].result]
    # Unsafe pointer representing an indirect reference to values of type T
    # Methods
    fn __init__(out self)
    fn alloc(count: Int) -> UnsafePointer[type, address_space = AddressSpace.GENERIC, alignment=alignment, origin = MutableOrigin.empty]
    fn __getitem__(self) -> ref [origin, address_space] type
    fn offset[I: Indexer](self, idx: I) -> Self
    fn __getitem__[I: Indexer](self, offset: I) -> ref [origin, address_space] type
    fn load[type: DType, width: Int = 1](self: UnsafePointer[Scalar[type], **_]) -> SIMD[type, width]
    fn store[type: DType, width: Int = 1](self: UnsafePointer[Scalar[type], **_], val: SIMD[type, width])
    fn bitcast[T: AnyType = Self.type](self) -> UnsafePointer[T, address_space=address_space, alignment=alignment, mut=mut, origin=origin]
    fn free(self: UnsafePointer[_, address_space = AddressSpace.GENERIC, **_])
    fn destroy_pointee(self: UnsafePointer[type, address_space = AddressSpace.GENERIC, **_])
    fn take_pointee[T: Movable](self: UnsafePointer[T, address_space = AddressSpace.GENERIC, **_]) -> T
    fn init_pointee_move[T: Movable](self: UnsafePointer[T, address_space = AddressSpace.GENERIC, **_], owned value: T)
    fn init_pointee_copy[T: Copyable](self: UnsafePointer[T, address_space = AddressSpace.GENERIC, **_], value: T)
    fn init_pointee_explicit_copy[T: ExplicitlyCopyable](self: UnsafePointer[T, address_space = AddressSpace.GENERIC, **_], value: T)
```

### Functions

```mojo
# Memory operations
fn memcmp[type: AnyType, address_space: AddressSpace](s1: UnsafePointer[type, address_space=address_space], s2: UnsafePointer[type, address_space=address_space], count: Int) -> Int
fn memcpy[T: AnyType](dest: UnsafePointer[T, address_space = AddressSpace.GENERIC, **_], src: UnsafePointer[T, address_space = AddressSpace.GENERIC, **_], count: Int)
fn memset[type: AnyType, address_space: AddressSpace](ptr: UnsafePointer[type, address_space=address_space], value: Byte, count: Int)
fn memset_zero[type: AnyType, address_space: AddressSpace](ptr: UnsafePointer[type, address_space=address_space], count: Int)
fn stack_allocation[count: Int, type: DType, alignment: Int = alignof[type]() if is_gpu() else 1, address_space: AddressSpace = AddressSpace.GENERIC]() -> UnsafePointer[Scalar[type], address_space=address_space]
fn stack_allocation[count: Int, type: AnyType, name: Optional[StringLiteral] = None, alignment: Int = alignof[type]() if is_gpu() else 1, address_space: AddressSpace = AddressSpace.GENERIC]() -> UnsafePointer[type, address_space=address_space]

# Type conversions
fn bitcast[type: DType, width: Int, new_type: DType, new_width: Int = width](val: SIMD[type, width]) -> SIMD[new_type, new_width]
fn pack_bits[width: Int, new_type: DType = _uint(width)](val: SIMD[DType.bool, width]) -> Scalar[new_type]
```

## os

Provides operating system interfaces, including environment variables, file operations, and atomic operations.

### Constants and Types

```mojo
# File-related constants
alias sep = "\\" if os_is_windows() else "/"
alias SEEK_SET: UInt8 = 0
alias SEEK_CUR: UInt8 = 1
alias SEEK_END: UInt8 = 2

# File descriptors
alias stdout: FileDescriptor = 1
alias stderr: FileDescriptor = 2

# Stat result
struct stat_result:
    var st_mode: Int
    var st_ino: Int
    var st_dev: Int
    var st_nlink: Int
    var st_uid: Int
    var st_gid: Int
    var st_size: Int
    var st_atimespec: _CTimeSpec
    var st_mtimespec: _CTimeSpec
    var st_ctimespec: _CTimeSpec
    var st_birthtimespec: _CTimeSpec
    var st_blocks: Int
    var st_blksize: Int
    var st_rdev: Int
    var st_flags: Int

# Atomic operations
struct Atomic[type: DType, *, scope: StringLiteral = ""]:
    var value: Scalar[type]
    fn load(self) -> Scalar[type]
    fn fetch_add(self, rhs: Scalar[type]) -> Scalar[type]
    fn fetch_sub(self, rhs: Scalar[type]) -> Scalar[type]
    fn compare_exchange_weak(self, mut expected: Scalar[type], desired: Scalar[type]) -> Bool
    fn max(self, rhs: Scalar[type])
    fn min(self, rhs: Scalar[type])
```

### Traits

```mojo
trait PathLike:
    fn __fspath__(self) -> String
```

### Functions

```mojo
# Environment functions
fn getenv(name: String, default: String = "") -> String
fn setenv(name: String, value: String, overwrite: Bool = True) -> Bool
fn unsetenv(name: String) -> Bool

# File system operations
fn stat[PathLike: os.PathLike](path: PathLike) raises -> stat_result
fn lstat[PathLike: os.PathLike](path: PathLike) raises -> stat_result
fn listdir[PathLike: os.PathLike](path: PathLike) raises -> List[String]
fn remove[PathLike: os.PathLike](path: PathLike) raises
fn unlink[PathLike: os.PathLike](path: PathLike) raises
fn mkdir[PathLike: os.PathLike](path: PathLike, mode: Int = 0o777) raises
fn makedirs[PathLike: os.PathLike](path: PathLike, mode: Int = 0o777, exist_ok: Bool = False) -> None
fn rmdir[PathLike: os.PathLike](path: PathLike) raises
fn removedirs[PathLike: os.PathLike](path: PathLike) -> None

# System information
fn getuid() -> Int
fn abort[result: AnyType = NoneType._mlir_type]() -> result
fn abort[result: AnyType = NoneType._mlir_type, *Ts: Writable](*messages: *Ts) -> result
```

## pathlib

Provides filesystem path manipulation.

### Constants

```mojo
alias DIR_SEPARATOR = "\\" if os_is_windows() else "/"
```

### Functions

```mojo
fn cwd() raises -> Path  # Get current working directory
```

### Types

```mojo
@value
struct Path(Stringable, Boolable, Writable, CollectionElement, CollectionElementNew, PathLike, KeyElement):
    var path: String  # The underlying path string

    # Constructors
    fn __init__(out self) raises  # Current directory
    fn __init__(out self, path: StringSlice)
    fn __init__(out self, owned path: String)

    # Path operations
    fn copy(self) -> Self
    fn __truediv__(self, suffix: Self) -> Self  # Path joining with /
    fn __truediv__(self, suffix: StringSlice) -> Self
    fn __itruediv__(mut self, suffix: StringSlice)
    fn joinpath(self, *pathsegments: String) -> Path

    # String conversion
    fn __str__(self) -> String
    fn __repr__(self) -> String
    fn __fspath__(self) -> String  # For os.PathLike compatibility
    fn __bool__(self) -> Bool  # True if path is not empty

    # Comparison
    fn __eq__(self, other: Self) -> Bool
    fn __eq__(self, other: StringSlice) -> Bool
    fn __ne__(self, other: Self) -> Bool

    # Hashing
    fn __hash__(self) -> UInt

    # File system operations
    fn stat(self) raises -> stat_result  # Get file stats
    fn lstat(self) raises -> stat_result  # Get symlink stats
    fn exists(self) -> Bool  # Check if path exists
    fn expanduser(self) raises -> Path  # Expand ~ to home directory
    fn is_dir(self) -> Bool  # Check if path is a directory
    fn is_file(self) -> Bool  # Check if path is a file
    fn read_text(self) raises -> String  # Read file as text
    fn read_bytes(self) raises -> List[UInt8]  # Read file as bytes
    fn write_text[stringable: Stringable](self, value: stringable) raises  # Write text to file
    fn listdir(self) raises -> List[Path]  # List directory contents

    # Path information
    fn suffix(self) -> String  # Get file extension

    # Static methods
    @staticmethod
    fn home() raises -> Path  # Get user's home directory
```

## pwd

Provides access to the password database.

### Types

```mojo
@value
struct Passwd(Stringable):
    var pw_name: String    # User name
    var pw_passwd: String  # User password
    var pw_uid: Int        # User ID
    var pw_gid: Int        # Group ID
    var pw_gecos: String   # User information
    var pw_dir: String     # Home directory
    var pw_shell: String   # Shell program
```

### Functions

```mojo
# Retrieve password database entry by user name
fn getpwnam(name: String) raises -> Passwd

# Retrieve password database entry by user ID
fn getpwuid(uid: Int) raises -> Passwd
```

## python

Provides Python interoperability.

### Types

```mojo
@register_passable
struct PythonObject(ImplicitlyBoolable, ImplicitlyIntable, Indexer, KeyElement, SizedRaising, Stringable, Writable, _HashableWithHasher):
    # Methods
    fn __init__(out self)  # Initialize with None
    fn __init__(out self, ptr: PyObjectPtr)
    fn __init__(out self, none: NoneType)
    fn __init__(out self, value: Bool)
    fn __init__(out self, integer: Int)
    fn __init__[dt: DType](mut self, value: SIMD[dt, 1])
    fn __init__(out self, value: StringLiteral)
    fn __init__(out self, value: String)
    fn __init__(out self, string: StringSlice)
    fn __init__[*Ts: CollectionElement](mut self, value: ListLiteral[*Ts])
    fn __init__[*Ts: CollectionElement](mut self, value: Tuple[*Ts])
    fn __init__(out self, slice: Slice)
    fn __init__(out self, value: Dict[Self, Self])

    # Conversion methods
    fn __bool__(self) -> Bool
    fn __int__(self) -> Int
    fn __float__(self) -> Float64
    fn __str__(self) -> String

    # Python operations
    fn __getattr__(self, name: StringLiteral) raises -> PythonObject
    fn __setattr__(self, name: StringLiteral, new_value: PythonObject) raises
    fn __getitem__(self, *args: PythonObject) raises -> PythonObject
    fn __getitem__(self, *args: Slice) raises -> PythonObject
    fn __setitem__(mut self, *args: PythonObject, value: PythonObject) raises
    fn __call__(self, *args: PythonObject, **kwargs: PythonObject) raises -> PythonObject
    fn __iter__(self) raises -> _PyIter
    fn __contains__(self, rhs: PythonObject) raises -> Bool

    # Arithmetic operations
    fn __add__(self, rhs: PythonObject) raises -> PythonObject
    fn __sub__(self, rhs: PythonObject) raises -> PythonObject
    fn __mul__(self, rhs: PythonObject) raises -> PythonObject
    fn __truediv__(self, rhs: PythonObject) raises -> PythonObject
    fn __floordiv__(self, rhs: PythonObject) raises -> PythonObject
    fn __mod__(self, rhs: PythonObject) raises -> PythonObject
    fn __pow__(self, exp: PythonObject) raises -> PythonObject

@register_passable
struct TypedPythonObject[type_hint: StringLiteral](SizedRaising):
    var _obj: PythonObject

    # Specialized methods for different type hints
    fn __getitem__(self: TypedPythonObject["Tuple"], pos: I) raises -> PythonObject
```

### Functions

```mojo
struct Python:
    # Evaluation functions
    fn eval(mut self, code: StringSlice) -> Bool
    @staticmethod
    fn evaluate(expr: StringSlice, file: Bool = False, name: StringSlice[StaticConstantOrigin] = "__main__") raises -> PythonObject

    # Path functions
    @staticmethod
    fn add_to_path(dir_path: StringSlice) raises

    # Module operations
    @staticmethod
    fn import_module(module: StringSlice) raises -> PythonObject
    @staticmethod
    fn create_module(name: String) raises -> TypedPythonObject["Module"]
    @staticmethod
    fn add_functions(mut module: TypedPythonObject["Module"], owned functions: List[PyMethodDef]) raises
    @staticmethod
    fn add_object(mut module: TypedPythonObject["Module"], name: StringLiteral, value: PythonObject) raises

    # Container creation
    @staticmethod
    fn dict() -> PythonObject
    @staticmethod
    fn list() -> PythonObject

    # Utility methods
    @staticmethod
    fn none() -> PythonObject
    @staticmethod
    fn is_type(x: PythonObject, y: PythonObject) -> Bool
    @staticmethod
    fn type(obj: PythonObject) -> PythonObject
```

## random

Provides random number generation.

### Functions

```mojo
# Seed the random number generator
fn seed()  # Seed with current time
fn seed(a: Int)  # Seed with a specific value

# Generate random floating point numbers
fn random_float64(min: Float64 = 0, max: Float64 = 1) -> Float64
fn randn_float64(mean: Float64 = 0.0, variance: Float64 = 1.0) -> Float64

# Generate random integers
fn random_si64(min: Int64, max: Int64) -> Int64
fn random_ui64(min: UInt64, max: UInt64) -> UInt64

# Fill memory with random values
fn randint[type: DType](ptr: UnsafePointer[Scalar[type]], size: Int, low: Int, high: Int)
fn rand[type: DType](ptr: UnsafePointer[Scalar[type], mut=True, **_], size: Int, /, *, min: Float64 = 0.0, max: Float64 = 1.0, int_scale: Optional[Int] = None)
fn randn[type: DType](ptr: UnsafePointer[Scalar[type]], size: Int, mean: Float64 = 0.0, variance: Float64 = 1.0)

# Shuffle a list in place
fn shuffle[T: CollectionElement](mut list: List[T])
```

## stat

Provides file status constants and functions.

### Constants

```mojo
alias S_IFMT = 0o0170000    # Bit mask for file type
alias S_IFDIR = 0o040000    # Directory
alias S_IFCHR = 0o020000    # Character device
alias S_IFBLK = 0o060000    # Block device
alias S_IFREG = 0o0100000   # Regular file
alias S_IFIFO = 0o010000    # FIFO
alias S_IFLNK = 0o0120000   # Symbolic link
alias S_IFSOCK = 0o0140000  # Socket
```

### Functions

```mojo
# Check file type from mode
fn S_ISLNK[intable: Intable](mode: intable) -> Bool  # Is a symbolic link
fn S_ISREG[intable: Intable](mode: intable) -> Bool  # Is a regular file
fn S_ISDIR[intable: Intable](mode: intable) -> Bool  # Is a directory
fn S_ISCHR[intable: Intable](mode: intable) -> Bool  # Is a character device
fn S_ISBLK[intable: Intable](mode: intable) -> Bool  # Is a block device
fn S_ISFIFO[intable: Intable](mode: intable) -> Bool  # Is a FIFO
fn S_ISSOCK[intable: Intable](mode: intable) -> Bool  # Is a socket
```

## sys

Provides system information, intrinsics, and utilities for interacting with the operating system.

### Types

```mojo
# FFI types
alias c_char = Int8
alias c_uchar = UInt8
alias c_int = Int32
alias c_uint = UInt32
alias c_short = Int16
alias c_ushort = UInt16
alias c_long = Scalar[_c_long_dtype()]
alias c_long_long = Scalar[_c_long_long_dtype()]
alias c_size_t = UInt
alias c_ssize_t = Int
alias c_float = Float32
alias c_double = Float64
alias OpaquePointer = UnsafePointer[NoneType]

# Dynamic library loading
struct RTLD:
    alias LAZY = 1
    alias NOW = 2
    alias LOCAL = 4
    alias GLOBAL = 256 if os_is_linux() else 8

@value
@register_passable("trivial")
struct DLHandle(CollectionElement, CollectionElementNew, Boolable):
    # Methods
    fn __init__(out self, path: String, flags: Int = DEFAULT_RTLD)
    fn check_symbol(self, name: String) -> Bool
    fn close(mut self)
    fn get_function[result_type: AnyTrivialRegType](self, name: String) -> result_type
    fn get_symbol[result_type: AnyType](self, name: StringLiteral) -> UnsafePointer[result_type]
    fn call[name: StringLiteral, return_type: AnyTrivialRegType = NoneType, *T: AnyType](self, *args: *T) -> return_type

# Prefetch options
@register_passable("trivial")
struct PrefetchLocality:
    var value: Int32
    alias NONE = PrefetchLocality(0)
    alias LOW = PrefetchLocality(1)
    alias MEDIUM = PrefetchLocality(2)
    alias HIGH = PrefetchLocality(3)

@register_passable("trivial")
struct PrefetchRW:
    var value: Int32
    alias READ = PrefetchRW(0)
    alias WRITE = PrefetchRW(1)

@register_passable("trivial")
struct PrefetchCache:
    var value: Int32
    alias INSTRUCTION = PrefetchCache(0)
    alias DATA = PrefetchCache(1)

@register_passable("trivial")
struct PrefetchOptions:
    var rw: PrefetchRW
    var locality: PrefetchLocality
    var cache: PrefetchCache
    # Methods
    fn for_read(self) -> Self
    fn for_write(self) -> Self
    fn no_locality(self) -> Self
    fn low_locality(self) -> Self
    fn medium_locality(self) -> Self
    fn high_locality(self) -> Self
    fn to_data_cache(self) -> Self
    fn to_instruction_cache(self) -> Self
```

### Variables and Constants

```mojo
alias DEFAULT_RTLD = RTLD.NOW | RTLD.GLOBAL
alias is_compile_time = __mlir_op.`kgen.is_compile_time`
alias OptimizationLevel = _OptimizationLevel()
alias DebugLevel = _DebugLevel()
alias stdout: FileDescriptor = 1
alias stderr: FileDescriptor = 2
alias argv = () -> VariadicList[StringSlice[StaticConstantOrigin]]  # Command line arguments
```

### Functions

```mojo
# FFI utilities
fn external_call[callee: StringLiteral, return_type: AnyTrivialRegType, *types: AnyType](*args: *types) -> return_type

# System information
fn is_x86() -> Bool
fn has_sse4() -> Bool
fn has_avx() -> Bool
fn has_avx2() -> Bool
fn has_avx512f() -> Bool
fn has_fma() -> Bool
fn has_vnni() -> Bool
fn has_neon() -> Bool
fn has_neon_int8_dotprod() -> Bool
fn has_neon_int8_matmul() -> Bool
fn is_apple_m1() -> Bool
fn is_apple_m2() -> Bool
fn is_apple_m3() -> Bool
fn is_apple_silicon() -> Bool
fn is_neoverse_n1() -> Bool
fn has_intel_amx() -> Bool
fn os_is_macos() -> Bool
fn os_is_linux() -> Bool
fn os_is_windows() -> Bool
fn is_nvidia_gpu() -> Bool
fn is_amd_gpu() -> Bool
fn is_gpu() -> Bool
fn is_little_endian[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn is_big_endian[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn is_32bit[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn is_64bit[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn simdbitwidth[target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn simdbytewidth[target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn sizeof[type: AnyType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn alignof[type: AnyType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn bitwidthof[type: AnyTrivialRegType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn simdwidthof[type: AnyTrivialRegType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn num_physical_cores() -> Int
fn num_logical_cores() -> Int
fn num_performance_cores() -> Int
fn has_accelerator() -> Bool
fn has_amd_gpu_accelerator() -> Bool
fn has_nvidia_gpu_accelerator() -> Bool

# SIMD and memory operations
fn gather[type: DType, size: Int](owned base: SIMD[DType.index, size], mask: SIMD[DType.bool, size], passthrough: SIMD[type, size], alignment: Int = 0) -> SIMD[type, size]
fn scatter[type: DType, size: Int](value: SIMD[type, size], owned base: SIMD[DType.index, size], mask: SIMD[DType.bool, size], alignment: Int = 0)
fn prefetch[type: DType](addr: UnsafePointer[Scalar[type], **_])
fn masked_load[type: DType](addr: UnsafePointer[Scalar[type], **_], mask: SIMD[DType.bool, size], passthrough: SIMD[type, size], alignment: Int = 1) -> SIMD[type, size]
fn masked_store[size: Int](value: SIMD, addr: UnsafePointer[Scalar[value.type], **_], mask: SIMD[DType.bool, size], alignment: Int = 1)
fn compressed_store[type: DType, size: Int](value: SIMD[type, size], addr: UnsafePointer[Scalar[type], **_], mask: SIMD[DType.bool, size])
fn strided_load[type: DType](addr: UnsafePointer[Scalar[type], **_], stride: Int, mask: SIMD[DType.bool, simd_width] = True) -> SIMD[type, simd_width]
fn strided_store[type: DType](value: SIMD[type, simd_width], addr: UnsafePointer[Scalar[type], **_], stride: Int, mask: SIMD[DType.bool, simd_width] = True)

# Debug and optimization
fn breakpointhook()
fn expect[T: AnyTrivialRegType](val: T) -> T
fn likely(val: Bool) -> Bool
fn unlikely(val: Bool) -> Bool
fn assume(val: Bool)

# Parameter environment
fn is_defined[name: StringLiteral]() -> Bool
fn env_get_bool[name: StringLiteral]() -> Bool
fn env_get_bool[name: StringLiteral, default: Bool]() -> Bool
fn env_get_int[name: StringLiteral]() -> Int
fn env_get_int[name: StringLiteral, default: Int]() -> Int
fn env_get_string[name: StringLiteral]() -> StringLiteral
fn env_get_string[name: StringLiteral, default: StringLiteral]() -> StringLiteral
fn env_get_dtype[name: StringLiteral, default: DType]() -> DType

# Process control
fn exit()
fn exit[intable: Intable](code: intable)
```

## tempfile

Provides temporary file and directory handling.

### Functions

```mojo
# Get temporary directory
fn gettempdir() -> Optional[String]

# Create a temporary directory
fn mkdtemp(suffix: String = "", prefix: String = "tmp", dir: Optional[String] = None) raises -> String
```

### Types

```mojo
struct TemporaryDirectory:
    var name: String  # The path to the temporary directory

    # Constructor
    fn __init__(mut self, suffix: String = "", prefix: String = "tmp",
                dir: Optional[String] = None, ignore_cleanup_errors: Bool = False) raises

    # Context manager methods
    fn __enter__(self) -> String
    fn __exit__(self) raises
    fn __exit__(self, err: Error) -> Bool

struct NamedTemporaryFile:
    var name: String  # The path to the temporary file

    # Constructor
    fn __init__(mut self, mode: String = "w", name: Optional[String] = None,
                suffix: String = "", prefix: String = "tmp",
                dir: Optional[String] = None, delete: Bool = True) raises

    # File operations
    fn close(mut self) raises
    fn read(self, size: Int64 = -1) raises -> String
    fn read_bytes(self, size: Int64 = -1) raises -> List[UInt8]
    fn seek(self, offset: UInt64, whence: UInt8 = os.SEEK_SET) raises -> UInt64
    fn write[*Ts: Writable](mut self, *args: *Ts)
    fn write_bytes(mut self, bytes: Span[Byte, _])

    # Context manager
    fn __enter__(owned self) -> Self
```

## testing

Provides test assertion utilities.

### Functions

```mojo
# Boolean assertions
fn assert_true[T: Boolable](val: T, msg: String = "condition was unexpectedly False", *, location: Optional[_SourceLocation] = None) raises
fn assert_false[T: Boolable](val: T, msg: String = "condition was unexpectedly True", *, location: Optional[_SourceLocation] = None) raises

# Equality assertions
fn assert_equal[T: Testable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_equal(lhs: String, rhs: String, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_equal[type: DType, size: Int](lhs: SIMD[type, size], rhs: SIMD[type, size], msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_equal[T: TestableCollectionElement](lhs: List[T], rhs: List[T], msg: String = "", *, location: Optional[_SourceLocation] = None) raises

# Non-equality assertions
fn assert_not_equal[T: Testable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_not_equal(lhs: String, rhs: String, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_not_equal[type: DType, size: Int](lhs: SIMD[type, size], rhs: SIMD[type, size], msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_not_equal[T: TestableCollectionElement](lhs: List[T], rhs: List[T], msg: String = "", *, location: Optional[_SourceLocation] = None) raises

# Approximate equality for floating point
fn assert_almost_equal[type: DType, size: Int](lhs: SIMD[type, size], rhs: SIMD[type, size], msg: String = "", *, atol: Float64 = 1e-08, rtol: Float64 = 1e-05, equal_nan: Bool = False, location: Optional[_SourceLocation] = None) raises

# Identity assertions
fn assert_is[T: StringableIdentifiable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_is_not[T: StringableIdentifiable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises

# Exception testing
struct assert_raises:
    var message_contains: Optional[String]  # Optional text the error must contain

    fn __init__(out self, *, location: Optional[_SourceLocation] = None)
    fn __init__(mut self, *, contains: String, location: Optional[_SourceLocation] = None)
    fn __enter__(self)
    fn __exit__(self) raises
    fn __exit__(self, error: Error) raises -> Bool
```

### Traits

```mojo
trait Testable(EqualityComparable, Stringable):
    # Trait for types that can be tested with equality assertions

trait TestableCollectionElement(EqualityComparableCollectionElement, RepresentableCollectionElement):
    # Trait for collection elements that can be tested
```

## time

Provides time-related utilities.

### Functions

```mojo
# Time measurement functions
fn perf_counter() -> Float64  # High-resolution time in seconds
fn perf_counter_ns() -> UInt  # High-resolution time in nanoseconds
fn monotonic() -> UInt  # Monotonic time in nanoseconds

# Time execution of a function
fn time_function[func: fn () raises capturing [_] -> None]() raises -> UInt
fn time_function[func: fn () capturing [_] -> None]() -> UInt

# Sleep function
fn sleep(sec: Float64)  # Sleep for floating point seconds
fn sleep(sec: UInt)     # Sleep for integer seconds
```

## utils

Provides various utility types and functions.

### IndexList

```mojo
@value
@register_passable("trivial")
struct IndexList[size: Int, *, element_bitwidth: Int = bitwidthof[Int](), unsigned: Bool = False](Sized, Stringable, Writable, Comparable):
    # Constructors
    fn __init__(out self)  # Initialize with zeros
    fn __init__(out self, data: StaticTuple[Self._int_type, size])
    fn __init__(out self, value: __mlir_type.index)  # Sized 1 constructor
    fn __init__(out self, elems: (Int, Int))  # 2D constructor
    fn __init__(out self, elems: (Int, Int, Int))  # 3D constructor
    fn __init__(out self, elems: (Int, Int, Int, Int))  # 4D constructor
    fn __init__(out self, *elems: Int)  # Variadic constructor
    fn __init__(out self, elem: Int)  # Splat constructor
    fn __init__(out self, values: VariadicList[Int])  # From variadic list

    # Size and element access
    fn __len__(self) -> Int
    fn __getitem__[idx: Int](self) -> Int
    fn __getitem__[I: Indexer](self, idx: I) -> Int
    fn __setitem__[idx: Int](mut self, val: Int)
    fn __setitem__[idx: Int](mut self, val: Self._int_type)
    fn __setitem__(mut self, idx: Int, val: Int)

    # Conversion
    fn as_tuple(self) -> StaticTuple[Int, size]
    fn canonicalize(self, out result: IndexList[size, element_bitwidth = bitwidthof[Int](), unsigned=False])

    # Operations
    fn flattened_length(self) -> Int
    fn __add__(self, rhs: Self) -> Self
    fn __sub__(self, rhs: Self) -> Self
    fn __mul__(self, rhs: Self) -> Self
    fn __floordiv__(self, rhs: Self) -> Self
    fn __rfloordiv__(self, rhs: Self) -> Self
    fn remu(self, rhs: Self) -> Self

    # Comparison
    fn __eq__(self, rhs: Self) -> Bool
    fn __ne__(self, rhs: Self) -> Bool
    fn __lt__(self, rhs: Self) -> Bool
    fn __le__(self, rhs: Self) -> Bool
    fn __gt__(self, rhs: Self) -> Bool
    fn __ge__(self, rhs: Self) -> Bool

    # Conversion
    fn cast[type: DType](self, out result: IndexList[size, element_bitwidth = bitwidthof[type](), unsigned = _is_unsigned[type]()])
    fn cast[*, element_bitwidth: Int = Self.element_bitwidth, unsigned: Bool = Self.unsigned](self, out result: IndexList[size, element_bitwidth=element_bitwidth, unsigned=unsigned])
```

```mojo
# Factory functions for indices
fn Index[T0: Intable, *, element_bitwidth: Int = bitwidthof[Int](), unsigned: Bool = False](x: T0, out result: IndexList[1, element_bitwidth=element_bitwidth, unsigned=unsigned])
fn Index[*, element_bitwidth: Int = bitwidthof[Int](), unsigned: Bool = False](x: UInt, out result: IndexList[1, element_bitwidth=element_bitwidth, unsigned=unsigned])
fn Index[T0: Intable, T1: Intable, *, element_bitwidth: Int = bitwidthof[Int](), unsigned: Bool = False](x: T0, y: T1, out result: IndexList[2, element_bitwidth=element_bitwidth, unsigned=unsigned])
# ... and similar for 3D, 4D, 5D indices ...

# Utility function for products
fn product[size: Int](tuple: IndexList[size, **_], end_idx: Int = size) -> Int
fn product[size: Int](tuple: IndexList[size, **_], start_idx: Int, end_idx: Int) -> Int
```

### StaticTuple

```mojo
@value
@register_passable("trivial")
struct StaticTuple[element_type: AnyTrivialRegType, size: Int](Sized):
    # Constructors
    fn __init__(out self)  # Uninitialized constructor
    fn __init__(out self, array: Self.type)  # From array type
    fn __init__(out self, *elems: Self.element_type)  # Variadic constructor
    fn __init__(out self, values: VariadicList[Self.element_type])  # From variadic list

    # Size and element access
    fn __len__(self) -> Int
    fn __getitem__[index: Int](self) -> Self.element_type
    fn __getitem__[I: Indexer](self, idx: I) -> Self.element_type
    fn __setitem__[idx: Int](mut self, val: Self.element_type)
    fn __setitem__[I: Indexer](mut self, idx: I, val: Self.element_type)
```

### Writer and Writable

```mojo
trait Writer:
    # Write bytes to this writer
    fn write_bytes(mut self, bytes: Span[Byte, _])

    # Write multiple writable objects
    fn write[*Ts: Writable](mut self, *args: *Ts)

trait Writable:
    # Format self to a writer
    fn write_to[W: Writer](self, mut writer: W)
```

### Locking

```mojo
struct SpinWaiter:
    fn __init__(out self)
    fn wait(self)  # Block current task according to wait policy

struct BlockingSpinLock:
    alias UNLOCKED = -1

    fn __init__(out self)
    fn lock(mut self, owner: Int)  # Acquire lock with owner ID
    fn unlock(mut self, owner: Int) -> Bool  # Release lock if owner matches

struct BlockingScopedLock:
    alias LockType = BlockingSpinLock

    fn __init__(mut self, lock: UnsafePointer[Self.LockType])
    fn __init__(mut self, mut lock: Self.LockType)
    fn __enter__(mut self)  # Acquire lock on entry
    fn __exit__(mut self)  # Release lock on exit
```

### Loop Utilities

```mojo
# Unroll loops at compile time
fn unroll[func: fn[idx0: Int, idx1: Int] () capturing [_] -> None, dim0: Int, dim1: Int]()
fn unroll[func: fn[idx0: Int, idx1: Int, idx2: Int] () capturing [_] -> None, dim0: Int, dim1: Int, dim2: Int]()
fn unroll[func: fn[idx: Int] () capturing [_] -> None, zero_starting_range: _ZeroStartingRange]()
fn unroll[func: fn[idx: Int] () raises capturing [_] -> None, zero_starting_range: _ZeroStartingRange]() raises
fn unroll[func: fn[idx: Int] () capturing [_] -> None, sequential_range: _SequentialRange]()
fn unroll[func: fn[idx: Int] () raises capturing [_] -> None, sequential_range: _SequentialRange]() raises
fn unroll[func: fn[idx: Int] () capturing [_] -> None, strided_range: _StridedRange]()
fn unroll[func: fn[idx: Int] () raises capturing [_] -> None, strided_range: _StridedRange]() raises
```

### Variant

```mojo
struct Variant[*Ts: CollectionElement](CollectionElement, ExplicitlyCopyable):
    # Constructors
    fn __init__(out self, *, unsafe_uninitialized: ())
    fn __init__[T: CollectionElement](mut self, owned value: T)

    # Copy and move
    fn copy(self, out copy: Self)
    fn __copyinit__(out self, other: Self)
    fn __moveinit__(out self, owned other: Self)

    # Access
    fn __getitem__[T: CollectionElement](ref self) -> ref [self] T

    # Get and set
    fn take[T: CollectionElement](mut self) -> T
    fn unsafe_take[T: CollectionElement](mut self) -> T
    fn replace[Tin: CollectionElement, Tout: CollectionElement](mut self, owned value: Tin) -> Tout
    fn unsafe_replace[Tin: CollectionElement, Tout: CollectionElement](mut self, owned value: Tin) -> Tout
    fn set[T: CollectionElement](mut self, owned value: T)

    # Type checking
    fn isa[T: CollectionElement](self) -> Bool
    fn unsafe_get[T: CollectionElement](ref self) -> ref [self] T
```

### Buffered Writing

```mojo
# Write multiple arguments to a writer with buffering
fn write_buffered[W: Writer, *Ts: Writable, buffer_size: Int = 4096, use_heap: Bool = False](mut writer: W, args: VariadicPack[_, Writable, *Ts], *, sep: StaticString = "", end: StaticString = "")

# Write a list to a writer with buffering
fn write_buffered[W: Writer, T: WritableCollectionElement, buffer_size: Int = 4096](mut writer: W, values: List[T, *_], *, sep: StaticString = "")
```
