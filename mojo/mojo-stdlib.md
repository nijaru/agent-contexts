
# Mojo Standard Library Documentation

## Table of Contents

- [base64](#base64)
- [bit](#bit)
- [hashlib](#hashlib)
- [math](#math)
- [pathlib](#pathlib)
- [pwd](#pwd)
- [random](#random)
- [stat](#stat)
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

## pathlib

Provides filesystem path manipulation.

### Constants

```mojo
alias DIR_SEPARATOR = "\\" if os_is_windows() else "/"
```

### Functions

```mojo
fn cwd() raises -> Path  # Get current working directory
fn _dir_of_current_file() raises -> Path  # Get directory of current file
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
    var _ignore_cleanup_errors: Bool

    # Constructor
    fn __init__(mut self, suffix: String = "", prefix: String = "tmp",
                dir: Optional[String] = None, ignore_cleanup_errors: Bool = False) raises

    # Context manager methods
    fn __enter__(self) -> String
    fn __exit__(self) raises
    fn __exit__(self, err: Error) -> Bool

struct NamedTemporaryFile:
    var _file_handle: FileHandle
    var _delete: Bool
    var name: String  # The path to the temporary file

    # Constructor
    fn __init__(mut self, mode: String = "w", name: Optional[String] = None,
                suffix: String = "", prefix: String = "tmp",
                dir: Optional[String] = None, delete: Bool = True) raises

    # Destructor
    fn __del__(owned self)

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
    var call_location: _SourceLocation

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
    alias element_type = _type_of_width[element_bitwidth, unsigned]()  # Underlying type
    var data: StaticTuple[Self._int_type, size]  # Storage

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

    # Hashing
    fn __hash__[H: _Hasher](self, mut hasher: H)
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
    alias type = __mlir_type[`!pop.array<`, size.value, `, `, Self.element_type, `>`]
    var array: Self.type  # Underlying storage

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
    var storage: OpaquePointer  # Pointer to underlying C++ SpinWaiter

    fn __init__(out self)
    fn __del__(owned self)
    fn wait(self)  # Block current task according to wait policy

struct BlockingSpinLock:
    alias UNLOCKED = -1
    var counter: Atomic[DType.int64]

    fn __init__(out self)
    fn lock(mut self, owner: Int)  # Acquire lock with owner ID
    fn unlock(mut self, owner: Int) -> Bool  # Release lock if owner matches

struct BlockingScopedLock:
    alias LockType = BlockingSpinLock
    var lock: UnsafePointer[Self.LockType]

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
    alias _sentinel: Int = -1
    alias _mlir_type = __mlir_type[`!kgen.variant<[rebind(:`, __type_of(Ts), ` `, Ts, `)]>`]
    var _impl: Self._mlir_type

    # Constructors
    fn __init__(out self, *, unsafe_uninitialized: ())
    fn __init__[T: CollectionElement](mut self, owned value: T)

    # Copy and move
    fn copy(self, out copy: Self)
    fn __copyinit__(out self, other: Self)
    fn __moveinit__(out self, owned other: Self)
    fn __del__(owned self)

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
