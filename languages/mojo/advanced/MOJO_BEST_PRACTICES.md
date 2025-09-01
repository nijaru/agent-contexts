# Mojo Best Practices for OmenDB
*Critical patterns for high-performance vector database and ML applications*

## Critical Type Conversions (Most Common Errors)

### ❌ WRONG - Python-style (causes compilation errors)
```mojo
var my_int = int(some_value)        # ERROR: use of unknown declaration 'int'
var my_str = str(some_value)        # ERROR: use of unknown declaration 'str'
var my_float = float(some_value)    # ERROR: use of unknown declaration 'float'
```

### ✅ CORRECT - Mojo-style
```mojo
var my_int = Int(some_value)        # Capital I
var my_str = String(some_value)     # String not str
var my_float = Float32(some_value)  # Explicit precision
```

## Memory Management Best Practices

### Single Storage Principle
**CRITICAL**: Never store the same data multiple times
```mojo
# ❌ WRONG - Double storage
struct BadBuffer:
    var data: UnsafePointer[Float32]          # Original vectors
    var quantized: UnsafePointer[UInt8]       # Quantized vectors
    # Storing BOTH wastes memory!

# ✅ CORRECT - Single storage
struct GoodBuffer:
    var data: UnsafePointer[Float32]          # Only if NOT quantized
    var quantized: UnsafePointer[UInt8]       # Only if quantized
    var use_quantization: Bool                # Flag to know which
```

### Move Semantics Over Copy
```mojo
# ❌ WRONG - Copying data
fn flush_buffer(self, buffer: VectorBuffer):
    for i in range(buffer.size):
        var vector = buffer.get_vector(i)     # COPY
        self.index.add(vector)                # Another COPY
        
# ✅ CORRECT - Moving data
fn flush_buffer(mut self, owned buffer: VectorBuffer):
    # Move entire buffer to index
    self.index.consume_buffer(buffer^)        # MOVE ownership
    # Buffer is now empty, no duplication
```

### Lazy Allocation Pattern
```mojo
# ❌ WRONG - Pre-allocate everything
fn __init__(out self):
    self.nodes = UnsafePointer[Node].alloc(1_000_000)  # 1M nodes upfront!
    self.edges = UnsafePointer[Edge].alloc(32_000_000) # 32M edges!

# ✅ CORRECT - Start small, grow as needed
fn __init__(out self):
    self.capacity = 100                      # Start small
    self.nodes = UnsafePointer[Node].alloc(self.capacity)
    
fn add_node(mut self):
    if self.size >= self.capacity:
        self._grow()                          # Double when needed
```

## State-of-the-Art Memory Targets

### Industry Standards (FAISS, ScaNN, Qdrant)
- **Float32 vectors**: 512 bytes/vector (128D × 4 bytes)
- **8-bit quantized**: 136 bytes/vector (128D × 1 byte + metadata)
- **Binary quantized**: 20 bytes/vector (128D / 8 bits + metadata)

### OmenDB Achieved (Aug 26, 2025)
- **With quantization**: 208 bytes/vector ✅
- **Without quantization**: 800 bytes/vector

### Current Problem (Aug 29, 2025)
- **With quantization**: 2,800+ bytes/vector ❌ (13x regression!)

## Common Mojo Performance Patterns

### SIMD Operations
```mojo
# Hardware-adaptive SIMD width
alias simd_width = simdwidthof[DType.float32]()

fn dot_product(a: UnsafePointer[Float32], b: UnsafePointer[Float32], dim: Int) -> Float32:
    var sum = SIMD[DType.float32, simd_width](0)
    
    # Process SIMD-width chunks
    for i in range(0, dim, simd_width):
        var va = a.load[width=simd_width](i)
        var vb = b.load[width=simd_width](i)
        sum = va.fma(vb, sum)
    
    return sum.reduce_add()
```

### Zero-Copy FFI
```mojo
# ❌ WRONG - Copying from Python
fn add_vector(py_array: PythonObject):
    var vector = List[Float32]()
    for i in range(len(py_array)):
        vector.append(Float32(py_array[i]))  # COPY each element!

# ✅ CORRECT - Direct pointer access
fn add_vector(data_ptr: UnsafePointer[Float32], size: Int):
    # Use pointer directly, no copy
    self.buffer.add_view(data_ptr, size)
```

## Critical Architecture Decisions

### 1. Buffer → Index Flow (NO DUPLICATION)
```mojo
struct VectorStore:
    var buffer: VectorBuffer         # Temporary holding
    var index: DiskANNIndex          # Permanent storage
    
    fn flush(mut self):
        # MOVE vectors from buffer to index
        self.index.consume(self.buffer^)
        self.buffer = VectorBuffer()  # New empty buffer
```

### 2. Quantization Storage (EITHER/OR)
```mojo
struct CSRGraph:
    # Store EITHER full precision OR quantized, never both
    var vectors: UnsafePointer[Float32]      # Only if NOT quantized
    var quantized: UnsafePointer[UInt8]      # Only if quantized
    var use_quantization: Bool
    
    fn memory_bytes(self) -> Int:
        if self.use_quantization:
            return self.num_nodes * (self.dimension + 8)  # 136 bytes/vector
        else:
            return self.num_nodes * self.dimension * 4     # 512 bytes/vector
```

### 3. Proper Pre-allocation Sizes
```mojo
# Based on empirical analysis of production workloads
alias DEFAULT_BUFFER_SIZE = 100        # Flush frequently
alias INITIAL_INDEX_CAPACITY = 100     # Start small
alias GROWTH_FACTOR = 1.5               # Grow moderately
alias MAX_DEGREE = 16                   # Edges per node (not 32 or 64!)
```

## Memory Debugging Checklist

When memory usage exceeds targets:

1. **Check for double storage**
   - Are vectors stored in both buffer AND index?
   - Are we keeping both quantized AND original?

2. **Check pre-allocations**
   - Search for `.alloc(` with large numbers
   - Look for `* 1000` or `* 10000` multiplications
   - Verify DEFAULT constants aren't too large

3. **Check for copies vs moves**
   - Look for `vector.append` in loops
   - Check if `owned` keyword is used for transfers
   - Verify `^` operator for moves

4. **Measure actual allocations**
   ```python
   import psutil
   process = psutil.Process()
   before = process.memory_info().rss
   # Operation
   after = process.memory_info().rss
   print(f"Allocated: {(after-before)/1024/1024:.1f} MB")
   ```

## Quick Reference: Python ↔ Mojo

| Python | Mojo | Notes |
|--------|------|-------|
| `int()` | `Int()` | Capital I |
| `str()` | `String()` | Full name |
| `float()` | `Float32()` or `Float64()` | Explicit precision |
| `list.append()` | `list.append()` | Same, but check for copies |
| `del obj` | `obj^` to move, `__del__` for cleanup | RAII pattern |
| `@property` | `fn get_x(self)` | No properties yet |
| `**kwargs` | Not supported | Use explicit parameters |

## Common Compilation Errors → Solutions

- `use of unknown declaration 'int'` → Use `Int()`
- `use of unknown declaration 'str'` → Use `String()`  
- `cannot convert Float64 to Float32` → Use `Float32(value)`
- `could not deduce parameter` → Add type annotations
- `no attribute 'get'` → Use index access `[0]` for tuples
- `unable to locate module` → Use relative imports within packages

## Performance Verification

Always verify optimizations with actual measurements:

```python
# Test memory efficiency
vectors_added = 1000
memory_used_mb = (after - before) / (1024 * 1024)
bytes_per_vector = (memory_used_mb * 1024 * 1024) / vectors_added

# Success criteria
assert bytes_per_vector <= 200  # Quantized target
assert bytes_per_vector <= 600  # Non-quantized target
```

---
*Remember: State-of-the-art means matching FAISS/ScaNN efficiency while maintaining Mojo's safety and performance guarantees.*