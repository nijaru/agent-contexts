# Collections Traits

Core traits for collection types.

## Traits

```mojo
trait KeyElement(CollectionElement, Hashable, EqualityComparable):
    # Trait for types that can be used as dictionary keys

trait IntervalElement(CollectionElement, Writable, Intable, Comparable, _CopyableGreaterThanComparable):
    # Trait for interval bounds
    fn __sub__(self, rhs: Self) -> Self

trait IntervalPayload(CollectionElement, Stringable, Comparable):
    # Trait for data associated with intervals
```