# Optional

Types that model values which may or may not be present.

## Types

```mojo
struct Optional[T: CollectionElement](CollectionElement, CollectionElementNew, Boolable):
    # A type modeling a value which may or may not be present

    # Constructors
    fn __init__(out self)  # Empty optional
    fn __init__(out self, owned value: T)  # With value
    fn __init__(out self, value: NoneType)  # Empty optional
    fn copy(self) -> Self

    # Operators
    fn __is__(self, other: NoneType) -> Bool
    fn __isnot__(self, other: NoneType) -> Bool
    fn __eq__(self, rhs: NoneType) -> Bool
    fn __eq__(self, rhs: Optional[T]) -> Bool
    fn __ne__(self, rhs: NoneType) -> Bool
    fn __ne__(self, rhs: Optional[T]) -> Bool
    fn __bool__(self) -> Bool
    fn __invert__(self) -> Bool

    # Methods
    fn value(ref self) -> ref [self._value] T  # Get value or abort
    fn unsafe_value(ref self) -> ref [self._value] T  # Get value without check
    fn take(mut self) -> T  # Move value out
    fn unsafe_take(mut self) -> T  # Move value out without check
    fn or_else(self, default: T) -> T  # Get value or default
    fn copied(self) -> Optional[T]  # Convert Optional[Pointer[T]] to Optional[T]

struct OptionalReg[T: AnyTrivialRegType](Boolable):
    # A register-passable optional type

    # Constructors
    fn __init__(out self)
    fn __init__(out self, value: T)
    fn __init__(out self, value: NoneType)

    # Operators
    fn __is__(self, other: NoneType) -> Bool
    fn __isnot__(self, other: NoneType) -> Bool
    fn __bool__(self) -> Bool

    # Methods
    fn value(self) -> T
    fn or_else(owned self, owned default: T) -> T
```