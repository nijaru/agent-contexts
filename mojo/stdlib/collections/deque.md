# Deque

A double-ended queue implementation with O(1) append and pop from both ends.

## Types

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