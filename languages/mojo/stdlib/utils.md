# utils

Provides various utility types and functions.

## IndexList

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

## StaticTuple

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

## Writer and Writable

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

## Locking

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

## Loop Utilities

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

## Variant

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

## Buffered Writing

```mojo
# Write multiple arguments to a writer with buffering
fn write_buffered[W: Writer, *Ts: Writable, buffer_size: Int = 4096, use_heap: Bool = False](mut writer: W, args: VariadicPack[_, Writable, *Ts], *, sep: StaticString = "", end: StaticString = "")

# Write a list to a writer with buffering
fn write_buffered[W: Writer, T: WritableCollectionElement, buffer_size: Int = 4096](mut writer: W, values: List[T, *_], *, sep: StaticString = "")
```