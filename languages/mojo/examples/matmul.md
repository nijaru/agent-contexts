# Mojo Matrix Multiplication Optimization

## Metadata
**TITLE:** Mojo Matrix Multiplication Optimization Techniques  
**VERSION:** N/A  
**COMPATIBILITY:** Requires Mojo compiler and runtime  
**DOCUMENTATION_SOURCE:** matmul.mojo  
**MODEL:** Claude-3.7-Sonnet-Thinking  

## Conceptual Overview

- Demonstrates progressive optimization techniques for matrix multiplication in Mojo
- Showcases systems-level optimizations including vectorization, parallelization, tiling, and memory access patterns
- Provides benchmarking infrastructure to compare performance against Python and NumPy implementations
- Illustrates how to leverage Mojo's systems programming features for high-performance computing
- Achieves significant performance improvements through systematic application of optimization techniques

## Core Features

### Matrix Structure [`STABLE`]

**Signature:**
```mojo
struct Matrix[rows: Int, cols: Int]:
    var data: UnsafePointer[Scalar[type]]

    fn __init__(out self)
    fn __init__(out self, data: UnsafePointer[Scalar[type]])
    @staticmethod
    fn rand() -> Self
    fn __getitem__(self, y: Int, x: Int) -> Scalar[type]
    fn __setitem__(mut self, y: Int, x: Int, val: Scalar[type])
    fn load[nelts: Int = 1](self, y: Int, x: Int) -> SIMD[type, nelts]
    fn store[nelts: Int = 1](self, y: Int, x: Int, val: SIMD[type, nelts])
```

**Dependencies/Imports:**
```mojo
from memory import UnsafePointer, memset_zero, stack_allocation
from random import rand
```

**Usage Example:**
```mojo
// Create a zero-initialized matrix
var C = Matrix[512, 4096]()

// Create a matrix with random values
var A = Matrix[512, 512].rand()

// Access elements
var value = A[0, 0]
A[1, 1] = 3.14

// Load/store SIMD values
var simd_val = A.load[4](row, col)
A.store[4](row, col, simd_val)
```

**Context:**
- Purpose: Provides a 2D matrix abstraction with SIMD-friendly access patterns
- Patterns: Uses row-major layout with direct memory access for performance
- Limitations: Fixed size determined at compile time through template parameters
- Behavior: Uses unsafe memory pointers for maximum performance

**Edge Cases and Anti-patterns:**
```mojo
// ANTI-PATTERN (memory leak):
var M = Matrix[100, 100].rand()
// No M.data.free() at end of scope

// CORRECT:
var M = Matrix[100, 100].rand()
// Use matrix
M.data.free()  // Explicitly free memory
```

## Matrix Multiplication Implementations

### Naive Implementation [`STABLE`]

**Signature:**
```mojo
fn matmul_naive(mut C: Matrix, A: Matrix, B: Matrix)
```

**Usage Example:**
```mojo
var A = Matrix[M, K].rand()
var B = Matrix[K, N].rand()
var C = Matrix[M, N]()
matmul_naive(C, A, B)
```

**Context:**
- Purpose: Baseline implementation using triple-nested loops
- Performance: Slowest implementation, used as baseline for comparison
- Behavior: Single-threaded, scalar computation

**Implementation:**
```mojo
fn matmul_naive(mut C: Matrix, A: Matrix, B: Matrix):
    for m in range(C.rows):
        for k in range(A.cols):
            for n in range(C.cols):
                C[m, n] += A[m, k] * B[k, n]
```

### Vectorized Implementation [`STABLE`]

**Signature:**
```mojo
fn matmul_vectorized(mut C: Matrix, A: Matrix, B: Matrix)
```

**Dependencies/Imports:**
```mojo
from algorithm import vectorize
```

**Usage Example:**
```mojo
matmul_vectorized(C, A, B)
```

**Context:**
- Purpose: SIMD-accelerated matrix multiplication
- Performance: Significant speedup over naive implementation through SIMD
- Behavior: Vectorized computation using SIMD instructions

**Implementation:**
```mojo
fn matmul_vectorized(mut C: Matrix, A: Matrix, B: Matrix):
    for m in range(C.rows):
        for k in range(A.cols):
            @parameter
            fn dot[nelts: Int](n: Int):
                C.store[nelts](
                    m, n, C.load[nelts](m, n) + A[m, k] * B.load[nelts](k, n)
                )
            vectorize[dot, nelts, size = C.cols]()
```

### Parallelized Implementation [`STABLE`]

**Signature:**
```mojo
fn matmul_parallelized(mut C: Matrix, A: Matrix, B: Matrix)
```

**Dependencies/Imports:**
```mojo
from algorithm import parallelize, vectorize
```

**Context:**
- Purpose: Multi-threaded, SIMD-accelerated matrix multiplication
- Performance: Further speedup through parallelism across matrix rows
- Behavior: Multi-threaded, vectorized computation

**Implementation:**
```mojo
fn matmul_parallelized(mut C: Matrix, A: Matrix, B: Matrix):
    var num_workers = C.rows

    @parameter
    fn calc_row(m: Int):
        for k in range(A.cols):
            @parameter
            fn dot[nelts: Int](n: Int):
                C.store[nelts](
                    m, n, C.load[nelts](m, n) + A[m, k] * B.load[nelts](k, n)
                )
            vectorize[dot, nelts, size = C.cols]()

    parallelize[calc_row](C.rows, num_workers)
```

### Tiled Implementation [`STABLE`]

**Signature:**
```mojo
fn matmul_tiled(mut C: Matrix, A: Matrix, B: Matrix)
```

**Dependencies/Imports:**
```mojo
from algorithm import Static2DTileUnitFunc as Tile2DFunc
from algorithm import parallelize, vectorize
```

**Context:**
- Purpose: Cache-optimized, parallelized, vectorized matrix multiplication
- Performance: Improved memory locality through tiling
- Behavior: Processes matrices in tiles to improve cache utilization

**Implementation:**
```mojo
fn tile[tiled_fn: Tile2DFunc, tile_x: Int, tile_y: Int](end_x: Int, end_y: Int):
    for y in range(0, end_y, tile_y):
        for x in range(0, end_x, tile_x):
            tiled_fn[tile_x, tile_y](x, y)

fn matmul_tiled(mut C: Matrix, A: Matrix, B: Matrix):
    var num_workers = C.rows

    @parameter
    fn calc_row(m: Int):
        @parameter
        fn calc_tile[tile_x: Int, tile_y: Int](x: Int, y: Int):
            for k in range(y, y + tile_y):
                @parameter
                fn dot[nelts: Int](n: Int):
                    C.store(
                        m,
                        n + x,
                        C.load[nelts](m, n + x)
                        + A[m, k] * B.load[nelts](k, n + x),
                    )
                vectorize[dot, nelts, size=tile_x]()
        tile[calc_tile, tile_n, tile_k](C.cols, B.rows)

    parallelize[calc_row](C.rows, num_workers)
```

### Unrolled Implementation [`STABLE`]

**Signature:**
```mojo
fn matmul_unrolled[mode: Int](mut C: Matrix, A: Matrix, B: Matrix)
```

**Dependencies/Imports:**
```mojo
from algorithm import Static2DTileUnitFunc as Tile2DFunc
from algorithm import parallelize, vectorize
from sys import info
```

**Usage Example:**
```mojo
// Use physical cores count
matmul_unrolled[1](C, A, B)

// Use logical cores count
matmul_unrolled[2](C, A, B)
```

**Context:**
- Purpose: Loop-unrolled, tiled, parallelized, vectorized matrix multiplication
- Performance: Further speedup through loop unrolling
- Mode selection affects thread count:
  - 0: Uses rows as thread count
  - 1: Uses physical core count
  - 2: Uses logical core count
  - 3: Uses performance core count

### Reordered Implementation [`STABLE`]

**Signature:**
```mojo
fn matmul_reordered(mut C: Matrix, A: Matrix, B: Matrix)
```

**Dependencies/Imports:**
```mojo
from algorithm import Static2DTileUnitFunc as Tile2DFunc
from algorithm import parallelize, vectorize
from memory import stack_allocation, memset_zero
```

**Context:**
- Purpose: Most optimized matrix multiplication implementation
- Performance: Highest performance through multiple optimizations
- Key techniques:
  - Per-tile accumulators allocated on stack
  - Loop reordering for optimal memory access
  - Partial unrolling of reduction dimension
  - Parallel tiling across output matrix

**Edge Cases:**
- Matrix dimensions must be multiples of tile sizes:
  - M must be a multiple of tile_m (32)
  - N must be a multiple of tile_n (32)
  - K must be a multiple of tile_k

**Implementation Highlights:**
```mojo
fn matmul_reordered(mut C: Matrix, A: Matrix, B: Matrix):
    alias tile_m = 32
    alias tile_n = 32
    alias tile_k = max(4, K // 256)

    constrained[M % tile_m == 0, "M must be a multiple of tile_m"]()
    constrained[N % tile_n == 0, "N must be a multiple of tile_n"]()
    constrained[K % tile_k == 0, "K must be a multiple of tile_k"]()

    @parameter
    fn calc_tile[tile_m: Int, tile_n: Int](mo: Int, no: Int):
        // Allocate the tile of accumulators on the stack
        var accumulator = Matrix[tile_m, tile_n](
            stack_allocation[tile_m * tile_n, type]()
        )
        memset_zero(accumulator.data, tile_m * tile_n)
        
        // Process tiles with optimized memory access patterns
        // ...
```

## Utilities

### SIMD Width Helper [`STABLE`]

**Signature:**
```mojo
fn get_simd_width() -> Int
```

**Dependencies/Imports:**
```mojo
from sys import info, simdwidthof
```

**Context:**
- Purpose: Determines optimal SIMD width based on hardware
- Implementation: Uses 4x SIMD width on Apple Silicon, 2x on other architectures
- Usage: Called at compile time to set optimal vectorization width

### Tiling Helper Functions [`STABLE`]

**Signatures:**
```mojo
fn tile[tiled_fn: Tile2DFunc, tile_x: Int, tile_y: Int](end_x: Int, end_y: Int)
fn tile_parallel[tiled_fn: Tile2DFunc, tile_m: Int, tile_n: Int](end_m: Int, end_n: Int)
```

**Context:**
- Purpose: Abstractions for 2D tiling patterns
- tile: Serial tiling across a 2D space
- tile_parallel: Parallel tiling with work distribution

## Testing and Benchmarking

### Benchmarking Function [`STABLE`]

**Signature:**
```mojo
fn bench[func: fn (mut Matrix, Matrix, Matrix) -> None, name: StringLiteral](base_gflops: Float64, np_gflops: Float64) raises
```

**Context:**
- Purpose: Benchmark matrix multiplication implementations
- Measures: GFLOPS (billions of floating-point operations per second)
- Comparisons: Relative speedup vs Python and NumPy implementations

### Testing Functions [`STABLE`]

**Signatures:**
```mojo
fn test_matrix_equal[func: fn (mut Matrix, Matrix, Matrix) -> None](C: Matrix, A: Matrix, B: Matrix) raises -> Bool
fn test_all()
```

**Context:**
- Purpose: Validate correctness of optimized implementations
- test_matrix_equal: Compares output of implementation against reference
- test_all: Tests all implementations against naive baseline

## Configuration Constants

The module defines several important constants:

- `M = 512`: Rows of A and C matrices
- `N = 4096`: Columns of B and C matrices
- `K = 512`: Columns of A and rows of B matrices
- `type = DType.float32`: Data type for matrix elements
- `nelts`: Dynamic SIMD width based on hardware
- `tile_n = 64`: Tile size for N dimension
- `tile_k = 4`: Tile size for K dimension

## Performance Characteristics

The code includes benchmarking that shows impressive performance improvements:

1. Naive implementation: Baseline performance
2. Vectorized: Significant speedup through SIMD operations
3. Parallelized: Further improvement through multi-threading
4. Tiled: Better cache utilization
5. Unrolled: Improved instruction-level parallelism
6. Reordered: Highest performance through optimized memory access patterns

When benchmarked, the most optimized implementation (Reordered) can achieve:
- Hundreds of GFLOPS on modern hardware
- 100-1000x speedup over pure Python implementation
- Significant speedup even over NumPy (which uses optimized C/Fortran)

## Example Output

The program produces benchmark results in this format:

```
Problem Size (M N K): 512 4096 512
CPU Results

Python:              0.123 GFLOPS
Numpy:              45.678 GFLOPS
Naive:               0.456 GFLOPS     3.71x Python    0.01x Numpy
Vectorized:         12.345 GFLOPS   100.37x Python    0.27x Numpy
Parallelized:       78.901 GFLOPS   641.47x Python    1.73x Numpy
Tiled:             123.456 GFLOPS  1003.71x Python    2.70x Numpy
Unrolled:          234.567 GFLOPS  1907.05x Python    5.14x Numpy
Reordered:         345.678 GFLOPS  2810.39x Python    7.57x Numpy
```

This demonstrates how systems programming techniques in Mojo can achieve dramatic performance improvements, surpassing even highly optimized libraries like NumPy.
