# Dict

A dictionary implementation that maps keys to values.

## Types

```mojo
struct Dict[K: KeyElement, V: CollectionElement](Sized, CollectionElement, CollectionElementNew, Boolable):
    # A dictionary mapping keys to values

    # Constructors
    fn __init__(out self)  # Empty dictionary
    fn __init__(out self, *, power_of_two_initial_capacity: Int)  # Pre-reserved capacity
    fn copy(self) -> Self

    # Static methods
    fn fromkeys(keys: List[K, *_], value: V) -> Self
    fn fromkeys(keys: List[K, *_], value: Optional[V] = None) -> Dict[K, Optional[V]]

    # Operators
    fn __getitem__(self, key: K) raises -> ref V
    fn __setitem__(mut self, owned key: K, owned value: V)
    fn __contains__(self, key: K) -> Bool
    fn __iter__(ref self) -> _  # Return iterator over keys
    fn __reversed__(ref self) -> _  # Return reversed iterator over keys
    fn __or__(self, other: Self) -> Self  # Merge dictionaries
    fn __ior__(mut self, other: Self)  # Update with other dictionary
    fn __len__(self) -> Int
    fn __bool__(self) -> Bool

    # Methods
    fn find(self, key: K) -> Optional[V]  # Find value by key
    fn get_ptr(ref self, key: K) -> Optional[Pointer[V, _]]
    fn get(self, key: K) -> Optional[V]
    fn get(self, key: K, default: V) -> V
    fn pop(mut self, key: K, owned default: V) -> V
    fn pop(mut self, key: K) raises -> V
    fn popitem(mut self) raises -> DictEntry[K, V]
    fn keys(ref self) -> _  # Return iterator over keys
    fn values(ref self) -> _  # Return iterator over values
    fn items(ref self) -> _  # Return iterator over items
    fn update(mut self, other: Self)
    fn clear(mut self)
    fn setdefault(mut self, key: K, owned default: V) raises -> ref V
```