# Counter

A counter is a collection that counts how many times each unique element appears in a collection.

## Types

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