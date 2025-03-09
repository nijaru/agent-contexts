# Interval & IntervalTree

Interval and IntervalTree types for efficient range queries.

## Types

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