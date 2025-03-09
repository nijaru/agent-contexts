# InlineArray

A fixed-size array with compile-time size checking.

## Types

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