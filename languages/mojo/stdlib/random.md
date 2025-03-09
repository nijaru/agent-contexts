# random

Provides random number generation.

## Functions

```mojo
# Seed the random number generator
fn seed()  # Seed with current time
fn seed(a: Int)  # Seed with a specific value

# Generate random floating point numbers
fn random_float64(min: Float64 = 0, max: Float64 = 1) -> Float64
fn randn_float64(mean: Float64 = 0.0, variance: Float64 = 1.0) -> Float64

# Generate random integers
fn random_si64(min: Int64, max: Int64) -> Int64
fn random_ui64(min: UInt64, max: UInt64) -> UInt64

# Fill memory with random values
fn randint[type: DType](ptr: UnsafePointer[Scalar[type]], size: Int, low: Int, high: Int)
fn rand[type: DType](ptr: UnsafePointer[Scalar[type], mut=True, **_], size: Int, /, *, min: Float64 = 0.0, max: Float64 = 1.0, int_scale: Optional[Int] = None)
fn randn[type: DType](ptr: UnsafePointer[Scalar[type]], size: Int, mean: Float64 = 0.0, variance: Float64 = 1.0)

# Shuffle a list in place
fn shuffle[T: CollectionElement](mut list: List[T])
```