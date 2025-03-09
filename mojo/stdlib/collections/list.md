# List

A dynamically-allocated list implementation.

## Types

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