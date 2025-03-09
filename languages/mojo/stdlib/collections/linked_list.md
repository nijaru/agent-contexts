# LinkedList

A doubly-linked list implementation.

## Types

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