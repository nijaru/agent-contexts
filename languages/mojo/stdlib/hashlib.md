# hashlib

Provides hash functions and hashable interfaces.

## Types and Traits

```mojo
trait Hashable:
    # Get the hash value for this object
    fn __hash__(self) -> UInt
```

## Functions

```mojo
# Hash a hashable type
fn hash[T: Hashable](hashable: T) -> UInt

# Hash a byte array
fn hash(bytes: UnsafePointer[UInt8], n: Int) -> UInt
```