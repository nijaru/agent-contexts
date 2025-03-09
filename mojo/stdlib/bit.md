# bit

Provides bit manipulation utilities.

## Functions

```mojo
# Counting zeros
fn count_leading_zeros(val: Int) -> Int
fn count_leading_zeros[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn count_trailing_zeros(val: Int) -> Int
fn count_trailing_zeros[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Bit reversing and swapping
fn bit_reverse(val: Int) -> Int
fn bit_reverse[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn byte_swap(val: Int) -> Int
fn byte_swap[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Bit counting and operations
fn pop_count(val: Int) -> Int
fn pop_count[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn bit_not[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn bit_width(val: Int) -> Int
fn bit_width[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Power of 2 functions
fn log2_floor(val: Int) -> Int
fn is_power_of_two(val: Int) -> Bool
fn is_power_of_two[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[DType.bool, width]
fn next_power_of_two(val: Int) -> Int
fn next_power_of_two[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]
fn prev_power_of_two(val: Int) -> Int
fn prev_power_of_two[type: DType, width: Int](val: SIMD[type, width]) -> SIMD[type, width]

# Bit rotation
fn rotate_bits_left[shift: Int](x: Int) -> Int
fn rotate_bits_left[type: DType, width: Int, shift: Int](x: SIMD[type, width]) -> SIMD[type, width]
fn rotate_bits_right[shift: Int](x: Int) -> Int
fn rotate_bits_right[type: DType, width: Int, shift: Int](x: SIMD[type, width]) -> SIMD[type, width]
```