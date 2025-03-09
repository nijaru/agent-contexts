# Set

A set data type that stores unique items.

## Types

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