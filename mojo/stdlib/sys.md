# sys

Provides system information, intrinsics, and utilities for interacting with the operating system.

## Types

```mojo
# FFI types
alias c_char = Int8
alias c_uchar = UInt8
alias c_int = Int32
alias c_uint = UInt32
alias c_short = Int16
alias c_ushort = UInt16
alias c_long = Scalar[_c_long_dtype()]
alias c_long_long = Scalar[_c_long_long_dtype()]
alias c_size_t = UInt
alias c_ssize_t = Int
alias c_float = Float32
alias c_double = Float64
alias OpaquePointer = UnsafePointer[NoneType]

# Dynamic library loading
struct RTLD:
    alias LAZY = 1
    alias NOW = 2
    alias LOCAL = 4
    alias GLOBAL = 256 if os_is_linux() else 8

@value
@register_passable("trivial")
struct DLHandle(CollectionElement, CollectionElementNew, Boolable):
    # Methods
    fn __init__(out self, path: String, flags: Int = DEFAULT_RTLD)
    fn check_symbol(self, name: String) -> Bool
    fn close(mut self)
    fn get_function[result_type: AnyTrivialRegType](self, name: String) -> result_type
    fn get_symbol[result_type: AnyType](self, name: StringLiteral) -> UnsafePointer[result_type]
    fn call[name: StringLiteral, return_type: AnyTrivialRegType = NoneType, *T: AnyType](self, *args: *T) -> return_type

# Prefetch options
@register_passable("trivial")
struct PrefetchLocality:
    var value: Int32
    alias NONE = PrefetchLocality(0)
    alias LOW = PrefetchLocality(1)
    alias MEDIUM = PrefetchLocality(2)
    alias HIGH = PrefetchLocality(3)

@register_passable("trivial")
struct PrefetchRW:
    var value: Int32
    alias READ = PrefetchRW(0)
    alias WRITE = PrefetchRW(1)

@register_passable("trivial")
struct PrefetchCache:
    var value: Int32
    alias INSTRUCTION = PrefetchCache(0)
    alias DATA = PrefetchCache(1)

@register_passable("trivial")
struct PrefetchOptions:
    var rw: PrefetchRW
    var locality: PrefetchLocality
    var cache: PrefetchCache
    # Methods
    fn for_read(self) -> Self
    fn for_write(self) -> Self
    fn no_locality(self) -> Self
    fn low_locality(self) -> Self
    fn medium_locality(self) -> Self
    fn high_locality(self) -> Self
    fn to_data_cache(self) -> Self
    fn to_instruction_cache(self) -> Self
```

## Variables and Constants

```mojo
alias DEFAULT_RTLD = RTLD.NOW | RTLD.GLOBAL
alias is_compile_time = __mlir_op.`kgen.is_compile_time`
alias OptimizationLevel = _OptimizationLevel()
alias DebugLevel = _DebugLevel()
alias stdout: FileDescriptor = 1
alias stderr: FileDescriptor = 2
alias argv = () -> VariadicList[StringSlice[StaticConstantOrigin]]  # Command line arguments
```

## Functions

```mojo
# FFI utilities
fn external_call[callee: StringLiteral, return_type: AnyTrivialRegType, *types: AnyType](*args: *types) -> return_type

# System information
fn is_x86() -> Bool
fn has_sse4() -> Bool
fn has_avx() -> Bool
fn has_avx2() -> Bool
fn has_avx512f() -> Bool
fn has_fma() -> Bool
fn has_vnni() -> Bool
fn has_neon() -> Bool
fn has_neon_int8_dotprod() -> Bool
fn has_neon_int8_matmul() -> Bool
fn is_apple_m1() -> Bool
fn is_apple_m2() -> Bool
fn is_apple_m3() -> Bool
fn is_apple_silicon() -> Bool
fn is_neoverse_n1() -> Bool
fn has_intel_amx() -> Bool
fn os_is_macos() -> Bool
fn os_is_linux() -> Bool
fn os_is_windows() -> Bool
fn is_nvidia_gpu() -> Bool
fn is_amd_gpu() -> Bool
fn is_gpu() -> Bool
fn is_little_endian[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn is_big_endian[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn is_32bit[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn is_64bit[target: __mlir_type.`!kgen.target` = _current_target()]() -> Bool
fn simdbitwidth[target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn simdbytewidth[target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn sizeof[type: AnyType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn alignof[type: AnyType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn bitwidthof[type: AnyTrivialRegType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn simdwidthof[type: AnyTrivialRegType, target: __mlir_type.`!kgen.target` = _current_target()]() -> Int
fn num_physical_cores() -> Int
fn num_logical_cores() -> Int
fn num_performance_cores() -> Int
fn has_accelerator() -> Bool
fn has_amd_gpu_accelerator() -> Bool
fn has_nvidia_gpu_accelerator() -> Bool

# SIMD and memory operations
fn gather[type: DType, size: Int](owned base: SIMD[DType.index, size], mask: SIMD[DType.bool, size], passthrough: SIMD[type, size], alignment: Int = 0) -> SIMD[type, size]
fn scatter[type: DType, size: Int](value: SIMD[type, size], owned base: SIMD[DType.index, size], mask: SIMD[DType.bool, size], alignment: Int = 0)
fn prefetch[type: DType](addr: UnsafePointer[Scalar[type], **_])
fn masked_load[type: DType](addr: UnsafePointer[Scalar[type], **_], mask: SIMD[DType.bool, size], passthrough: SIMD[type, size], alignment: Int = 1) -> SIMD[type, size]
fn masked_store[size: Int](value: SIMD, addr: UnsafePointer[Scalar[value.type], **_], mask: SIMD[DType.bool, size], alignment: Int = 1)
fn compressed_store[type: DType, size: Int](value: SIMD[type, size], addr: UnsafePointer[Scalar[type], **_], mask: SIMD[DType.bool, size])
fn strided_load[type: DType](addr: UnsafePointer[Scalar[type], **_], stride: Int, mask: SIMD[DType.bool, simd_width] = True) -> SIMD[type, simd_width]
fn strided_store[type: DType](value: SIMD[type, simd_width], addr: UnsafePointer[Scalar[type], **_], stride: Int, mask: SIMD[DType.bool, simd_width] = True)

# Debug and optimization
fn breakpointhook()
fn expect[T: AnyTrivialRegType](val: T) -> T
fn likely(val: Bool) -> Bool
fn unlikely(val: Bool) -> Bool
fn assume(val: Bool)

# Parameter environment
fn is_defined[name: StringLiteral]() -> Bool
fn env_get_bool[name: StringLiteral]() -> Bool
fn env_get_bool[name: StringLiteral, default: Bool]() -> Bool
fn env_get_int[name: StringLiteral]() -> Int
fn env_get_int[name: StringLiteral, default: Int]() -> Int
fn env_get_string[name: StringLiteral]() -> StringLiteral
fn env_get_string[name: StringLiteral, default: StringLiteral]() -> StringLiteral
fn env_get_dtype[name: StringLiteral, default: DType]() -> DType

# Process control
fn exit()
fn exit[intable: Intable](code: intable)
```