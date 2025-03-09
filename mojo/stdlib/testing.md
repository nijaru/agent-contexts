# testing

Provides test assertion utilities.

## Functions

```mojo
# Boolean assertions
fn assert_true[T: Boolable](val: T, msg: String = "condition was unexpectedly False", *, location: Optional[_SourceLocation] = None) raises
fn assert_false[T: Boolable](val: T, msg: String = "condition was unexpectedly True", *, location: Optional[_SourceLocation] = None) raises

# Equality assertions
fn assert_equal[T: Testable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_equal(lhs: String, rhs: String, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_equal[type: DType, size: Int](lhs: SIMD[type, size], rhs: SIMD[type, size], msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_equal[T: TestableCollectionElement](lhs: List[T], rhs: List[T], msg: String = "", *, location: Optional[_SourceLocation] = None) raises

# Non-equality assertions
fn assert_not_equal[T: Testable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_not_equal(lhs: String, rhs: String, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_not_equal[type: DType, size: Int](lhs: SIMD[type, size], rhs: SIMD[type, size], msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_not_equal[T: TestableCollectionElement](lhs: List[T], rhs: List[T], msg: String = "", *, location: Optional[_SourceLocation] = None) raises

# Approximate equality for floating point
fn assert_almost_equal[type: DType, size: Int](lhs: SIMD[type, size], rhs: SIMD[type, size], msg: String = "", *, atol: Float64 = 1e-08, rtol: Float64 = 1e-05, equal_nan: Bool = False, location: Optional[_SourceLocation] = None) raises

# Identity assertions
fn assert_is[T: StringableIdentifiable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises
fn assert_is_not[T: StringableIdentifiable](lhs: T, rhs: T, msg: String = "", *, location: Optional[_SourceLocation] = None) raises

# Exception testing
struct assert_raises:
    var message_contains: Optional[String]  # Optional text the error must contain

    fn __init__(out self, *, location: Optional[_SourceLocation] = None)
    fn __init__(mut self, *, contains: String, location: Optional[_SourceLocation] = None)
    fn __enter__(self)
    fn __exit__(self) raises
    fn __exit__(self, error: Error) raises -> Bool
```

## Traits

```mojo
trait Testable(EqualityComparable, Stringable):
    # Trait for types that can be tested with equality assertions

trait TestableCollectionElement(EqualityComparableCollectionElement, RepresentableCollectionElement):
    # Trait for collection elements that can be tested
```