# math

Provides mathematical constants, functions, and utilities.

## Constants

```mojo
alias pi = 3.1415926535897932384626433832795028841971693993751058209749445923
alias e = 2.7182818284590452353602874713526624977572470936999595749669676277
alias tau = 2 * pi
```

## Traits

```mojo
trait Floorable:
    fn __floor__(self) -> Self

trait Ceilable:
    fn __ceil__(self) -> Self

trait CeilDivable:
    fn __ceildiv__(self, denominator: Self) -> Self

trait Truncable:
    fn __trunc__(self) -> Self
```

## Functions

```mojo
# Basic rounding operations
fn floor[T: Floorable](value: T) -> T
fn ceil[T: Ceilable](value: T) -> T
fn ceildiv[T: CeilDivable](numerator: T, denominator: T) -> T
fn trunc[T: Truncable](value: T) -> T

# Root functions
fn sqrt(x: Int) -> Int
fn sqrt[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn isqrt(x: SIMD) -> __type_of(x)
fn cbrt(x: SIMD) -> __type_of(x)

# Reciprocal
fn recip(x: SIMD) -> __type_of(x)

# Exponential functions
fn exp2[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn exp[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn expm1(x: SIMD) -> __type_of(x)

# Logarithmic functions
fn log(x: SIMD) -> __type_of(x)
fn log2(x: SIMD) -> __type_of(x)
fn log10(x: SIMD) -> __type_of(x)
fn log1p(x: SIMD) -> __type_of(x)
fn logb(x: SIMD) -> __type_of(x)

# Trigonometric functions
fn sin[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn cos[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn tan(x: SIMD) -> __type_of(x)
fn asin(x: SIMD) -> __type_of(x)
fn acos(x: SIMD) -> __type_of(x)
fn atan(x: SIMD) -> __type_of(x)
fn atan2[type: DType, simd_width: Int](y: SIMD[type, simd_width], x: SIMD[type, simd_width]) -> SIMD[type, simd_width]

# Hyperbolic functions
fn sinh(x: SIMD) -> __type_of(x)
fn cosh(x: SIMD) -> __type_of(x)
fn tanh[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn asinh(x: SIMD) -> __type_of(x)
fn acosh(x: SIMD) -> __type_of(x)
fn atanh(x: SIMD) -> __type_of(x)

# Error functions
fn erf[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn erfc(x: SIMD) -> __type_of(x)

# Gamma functions
fn gamma(x: SIMD) -> __type_of(x)
fn lgamma(x: SIMD) -> __type_of(x)

# Bessel functions
fn j0(x: SIMD) -> __type_of(x)
fn j1(x: SIMD) -> __type_of(x)
fn y0(x: SIMD) -> __type_of(x)
fn y1(x: SIMD) -> __type_of(x)

# Utility functions
fn copysign[type: DType, simd_width: Int](magnitude: SIMD[type, simd_width], sign: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn isclose[type: DType, simd_width: Int](a: SIMD[type, simd_width], b: SIMD[type, simd_width], *, atol: Float64 = 1e-08, rtol: Float64 = 1e-05, equal_nan: Bool = False) -> SIMD[DType.bool, simd_width]
fn clamp(val: Int, lower_bound: Int, upper_bound: Int) -> Int
fn clamp(val: SIMD, lower_bound: SIMD, upper_bound: SIMD) -> SIMD

# Integer functions
fn gcd(m: Int, n: Int) -> Int
fn gcd(s: Span[Int]) -> Int
fn gcd(*values: Int) -> Int
fn lcm(m: Int, n: Int) -> Int
fn lcm(s: Span[Int]) -> Int
fn lcm(*values: Int) -> Int
fn factorial(n: Int) -> Int

# Vector and numeric functions
fn iota[type: DType, simd_width: Int](offset: Scalar[type] = 0) -> SIMD[type, simd_width]
fn fma(a: Int, b: Int, c: Int) -> Int
fn fma[type: DType, simd_width: Int](a: SIMD[type, simd_width], b: SIMD[type, simd_width], c: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn frexp[type: DType, simd_width: Int](x: SIMD[type, simd_width]) -> StaticTuple[SIMD[type, simd_width], 2]
fn ldexp[type: DType, simd_width: Int](x: SIMD[type, simd_width], exp: SIMD[DType.int32, simd_width]) -> SIMD[type, simd_width]
fn modf(x: SIMD) -> Tuple[__type_of(x), __type_of(x)]

# Alignment functions
fn align_down(value: Int, alignment: Int) -> Int
fn align_up(value: Int, alignment: Int) -> Int

# Other functions
fn hypot[type: DType, simd_width: Int](arg0: SIMD[type, simd_width], arg1: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn remainder[type: DType, simd_width: Int](x: SIMD[type, simd_width], y: SIMD[type, simd_width]) -> SIMD[type, simd_width]
fn scalb[type: DType, simd_width: Int](arg0: SIMD[type, simd_width], arg1: SIMD[type, simd_width]) -> SIMD[type, simd_width]

# Polynomial evaluation
fn polynomial_evaluate[dtype: DType, simd_width: Int, coefficients: List[SIMD[dtype, simd_width], *_]](x: SIMD[dtype, simd_width]) -> SIMD[dtype, simd_width]
```