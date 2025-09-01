# Mojo Patterns & Workarounds
*Critical knowledge for high-performance Mojo applications*

## Memory Overhead Issues

### Stdlib Collections (CRITICAL)
```mojo
# ❌ NEVER USE in hot paths - massive overhead
Dict[String, Int]  # 8KB per entry (100x expected)
List[String]       # 5KB per item (100x expected)
String             # Unknown but significant overhead

# ✅ SOLUTIONS IMPLEMENTED
SparseMap          # Custom hash map (180x improvement)
Fixed arrays       # Instead of List[String]
Batch operations   # Amortize FFI overhead
```

### Memory Patterns That Work
```mojo
# Arena allocation for batch operations
var arena = Arena(1024 * 1024)  # 1MB blocks
var batch_data = arena.alloc[Float32](count * 128)

# Fixed-size string pools
struct StringPool:
    var data: UnsafePointer[UInt8]
    var offsets: List[Int]
    
# Product Quantization (16x compression)
struct PQ32:
    var codes: UnsafePointer[UInt8]
    var codebook: Tensor[Float32]
```

## FFI Optimization

### Python FFI Overhead
```mojo
# ❌ BAD: Individual FFI calls (8KB overhead each)
for i in range(count):
    add_vector(keys[i], vectors[i])  # 8,356 bytes/vector

# ✅ GOOD: Batch FFI calls  
add_batch(keys, vectors)  # 1,475 bytes/vector

# ✅ BETTER: LibC FFI (50x faster than Python)
sys.ffi.external_call["mmap", UnsafePointer[Int8]](...)
```

### String Marshaling
```mojo
# ❌ Problem: String serialization used pointer addresses
write_string(str):
    file.write(Int(str._as_ptr()))  # Writing address!

# ✅ Solution: Serialize actual data
write_string(str):
    file.write(len(str))
    for c in str:
        file.write(ord(c))
```

## Import System Rules

### Relative Imports Required
```mojo
# ❌ WRONG - "unable to locate module"
from core.vector import Vector

# ✅ CORRECT - Relative imports
from .core.vector import Vector      # From root
from ..core.vector import Vector     # From subdir
from .vector import Vector           # Same directory
```

### Module Structure Requirements
- Every directory needs `__init__.mojo` with re-exports
- No module-level variables (Mojo limitation)
- Keep globals in native.mojo (monolith by necessity)

## Crash Workarounds

### Dict Iteration Bug
```mojo
# ❌ CRASHES with bus error
for item in dict.items():
    process(item)

# ✅ WORKAROUND: Manual key iteration
for key in known_keys:
    if key in dict:
        process(dict[key])
```

### Optional Handling
```mojo
# ❌ CRASHES on None
var value = optional.value()

# ✅ SAFE pattern
fn safe_unwrap[T](opt: Optional[T], context: String) -> Result[T, Error]:
    if opt:
        return Ok(opt.value())
    return Error("None value: " + context)
```

### Memory Allocation Limits
```mojo
# ❌ CRASHES at 26-27K with List[List[Int]]
var adjacency: List[List[Int]]  # Hard limit ~26K nodes

# ✅ SOLUTION: Memory-mapped or flat arrays
var edges: UnsafePointer[UInt32]  # Can scale to millions
var offsets: List[Int]            # CSR format
```

## Performance Patterns

### SIMD Operations (When Working)
```mojo
fn distance_simd[width: Int](a: SIMD[DType.float32, width], 
                             b: SIMD[DType.float32, width]) -> Float32:
    var diff = a - b
    return sqrt(diff.reduce_add())
```

### Batch Processing
```mojo
# Process in chunks to amortize overhead
alias BATCH_SIZE = 1000

fn process_batch(items: List[T]) -> None:
    for i in range(0, len(items), BATCH_SIZE):
        var end = min(i + BATCH_SIZE, len(items))
        _process_chunk(items[i:end])
```

### Buffer Management
```mojo
# Double buffering for concurrent read/write
struct DoubleBuffer:
    var active: Buffer
    var inactive: Buffer
    
    fn swap(inout self) -> None:
        self.active, self.inactive = self.inactive, self.active
```

## Compiler Limitations

### No Generics (Limited)
```mojo
# Can't do full generic programming
# Must create type-specific implementations
struct IntDict:  # Separate implementation
struct FloatDict:  # Separate implementation
```

### No Async/Await
```mojo
# Use double buffering instead
# Or manual state machines for async patterns
```

### No Thread Safety Primitives
```mojo
# No Arc, Mutex, atomics
# Solution: Single-threaded engine
# Concurrency at server layer (Rust)
```

## Debugging Techniques

### Memory Debugging
```bash
# Enable sanitizers
MOJO_ASAN=1 mojo run program.mojo
MOJO_MEMCHECK=1 mojo run program.mojo

# Debug build
mojo build --debug program.mojo
```

### Common Segfault Causes
1. Buffer overflow - check bounds
2. Use after free - track lifetimes
3. Null pointer - validate before use
4. Graph reallocation - copy old data correctly
5. String handling - use proper length

## Proven Optimizations

### What Worked
1. **SparseMap**: 180x improvement over Dict[String, Int]
2. **Batch operations**: 18x improvement in throughput
3. **Product Quantization**: 16x memory compression
4. **LibC mmap**: 50x faster than Python FFI
5. **CSR Graph**: 79% edge memory reduction

### What Didn't Work
1. Memory pooling - Mojo thread safety issues
2. Full SIMD - Compiler bugs
3. Module splitting - Import system limitations
4. Generic collections - Limited generic support

## Critical Files & Lines

### Performance Hot Paths
- `native.mojo:1850-2000` - VectorStore core
- `native.mojo:500-700` - Buffer management
- `diskann.mojo:200-300` - Search inner loop
- `csr_graph.mojo:150-250` - Edge operations

### Memory Management
- `vector_buffer.mojo:25` - id_to_index Dict
- `memory_mapped.mojo:100-200` - LibC mmap
- `scalar.mojo` - Quantization implementation

## Testing Patterns

### Scale Testing Required
```python
# Always test at scale, not toy examples
def test_at_scale():
    vectors = generate_vectors(100_000, 128)  # Not 100!
    # Small tests hide issues that appear at scale
```

### Performance Measurement
```python
# Run 3x, report median
times = []
for _ in range(3):
    start = time.perf_counter()
    operation()
    times.append(time.perf_counter() - start)
    
result = statistics.median(times)
```

---
*This document captures hard-won Mojo knowledge. Update when new patterns discovered.*