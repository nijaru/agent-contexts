# memory

Provides several pointer types and utility functions for memory management.

## Types

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

## Functions

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