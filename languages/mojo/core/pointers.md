# TITLE: Mojo Pointers
VERSION: 0.5.0
RELEASED: 2023-12-01
COMPATIBILITY: Mojo 0.5.0+
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/manual/pointers/
MODEL: Claude-3.7-Sonnet

## Conceptual Overview

- **Safe Memory Management System**: Mojo offers a comprehensive pointer system with both safe and unsafe options, allowing fine-grained control over memory without sacrificing safety when using the appropriate pointer type
- **Multiple Pointer Types for Different Use Cases**: From safe non-owning pointers (`Pointer`) to smart pointers (`OwnedPointer`, `ArcPointer`) to raw memory access (`UnsafePointer`)
- **Ownership Semantics**: Clear distinction between owning and non-owning pointers to prevent memory leaks and use-after-free errors
- **Reference Counting Support**: Shared ownership via reference-counted smart pointers for complex data structures
- **Foreign Function Interface**: Seamless interoperability with C/C++ and Python through unsafe pointers

## Core Features

### `Pointer[T]` [`STABLE`]

**Package:** `mojo.stdlib.memory.pointer`  
**Available Since:** `v0.3.0`  
**Status:** Stable  

**Signature:**
```mojo
struct Pointer[T: AnyType]:
    var address: UInt
    
    @staticmethod
    fn address_of(borrowed value: T) -> Self
    
    fn __getitem__(self) -> T
    fn __setitem__(inout self, value: T)
    
    fn load(self) -> T
    fn store(inout self, value: T)
```

**Dependencies/Imports:**
```mojo
from memory.pointer import Pointer
```

**Usage Example:**
```mojo
from memory.pointer import Pointer

fn pointer_example():
    var x: Int = 42
    let ptr = Pointer.address_of(x)
    
    # Read the value through the pointer
    let value = ptr[]  # or ptr.__getitem__()
    print(value)  # Outputs: 42
    
    # Update the value through the pointer
    ptr[] = 100  # or ptr.__setitem__(100)
    print(x)  # Outputs: 100
```

**Context:**
- Purpose: Safe pointer for non-owning references to initialized values
- Patterns: Useful for passing references to existing values
- Alternatives: Using references directly when possible
- Limitations: Cannot point to uninitialized memory or null
- Related: `OwnedPointer[T]`, `ArcPointer[T]`, `UnsafePointer[T]`
- Behavior: Tracks origin/lifetime of referenced value to prevent dangling pointers
- Performance: Zero overhead compared to raw pointers in release mode

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using pointers after the referenced variable goes out of scope
- Anti-patterns:
```mojo
# ANTI-PATTERN (dangling pointer):
fn get_dangling_pointer() -> Pointer[Int]:
    var local_var = 42
    return Pointer.address_of(local_var)  # WRONG: local_var is destroyed after function returns

# CORRECT:
fn use_pointer(borrowed value: Int):
    let ptr = Pointer.address_of(value)
    # Use ptr while value is in scope
```

### `OwnedPointer[T]` [`STABLE`]

**Package:** `mojo.stdlib.memory.owned_pointer`  
**Available Since:** `v0.3.0`  
**Status:** Stable  

**Signature:**
```mojo
struct OwnedPointer[T: AnyType]:
    var _ptr: UnsafePointer[T]
    
    fn __init__(inout self, value: T)
    fn __init__(inout self, value: owned T)
    fn __init__(inout self, other: owned Self)  # Transfer ownership

    fn __getitem__(self) -> T
    fn __setitem__(inout self, value: T)
    
    fn load(self) -> T
    fn store(inout self, value: T)
```

**Dependencies/Imports:**
```mojo
from memory.owned_pointer import OwnedPointer
```

**Usage Example:**
```mojo
from memory.owned_pointer import OwnedPointer

fn owned_pointer_example():
    # Create an owned pointer with a new value
    var ptr = OwnedPointer(100)
    
    # Read the value
    let value = ptr[]
    print(value)  # Outputs: 100
    
    # Update the value
    ptr[] = 200
    print(ptr[])  # Outputs: 200
    
    # Transfer ownership (moves the pointer)
    var new_ptr = OwnedPointer(ptr^)
    # ptr is now invalid, new_ptr owns the value
```

**Context:**
- Purpose: Smart pointer with exclusive ownership of its pointee
- Patterns: RAII-style memory management with automatic cleanup
- Alternatives: `ArcPointer` when shared ownership is needed
- Limitations: Cannot be copied, only moved, and isn't nullable
- Related: `ArcPointer[T]`, `Pointer[T]`
- Behavior: Automatically allocates and deallocates memory for the pointee
- Performance: Minimal overhead compared to manual memory management

**Edge Cases and Anti-patterns:**
- Common Mistakes: Attempting to copy an owned pointer (not allowed)
- Anti-patterns:
```mojo
# ANTI-PATTERN (copying an owned pointer):
fn wrong_copy():
    var ptr1 = OwnedPointer(42)
    var ptr2 = ptr1  # WRONG: Compile error, OwnedPointer not copyable

# CORRECT (transfer ownership):
fn correct_transfer():
    var ptr1 = OwnedPointer(42)
    var ptr2 = OwnedPointer(ptr1^)  # Move ownership using ^
    # ptr1 is now invalid, ptr2 owns the value
```

### `ArcPointer[T]` [`STABLE`]

**Package:** `mojo.stdlib.memory.arc`  
**Available Since:** `v0.3.0`  
**Status:** Stable  

**Signature:**
```mojo
struct ArcPointer[T: AnyType]:
    var _ptr: UnsafePointer[T]
    var _refcount: UnsafePointer[Atomic[UInt64]]
    
    fn __init__(inout self, value: T)
    fn __init__(inout self, value: owned T)
    fn __copyinit__(inout self, other: Self)  # Share ownership

    fn __getitem__(self) -> T
    fn __setitem__(inout self, value: T)
    
    fn load(self) -> T
    fn store(inout self, value: T)
```

**Dependencies/Imports:**
```mojo
from memory.arc import ArcPointer
```

**Usage Example:**
```mojo
from memory.arc import ArcPointer
from collections import Dict

fn arc_pointer_example():
    # Create shared dictionary
    var dict = Dict[String, Int]()
    dict["one"] = 1
    dict["two"] = 2
    
    # Create ArcPointer with dictionary
    var ptr1 = ArcPointer(dict^)
    
    # Create a second pointer sharing ownership
    var ptr2 = ptr1  # Increments reference count
    
    # Both pointers can access and modify the dictionary
    ptr1[]["three"] = 3
    print(ptr2[]["three"])  # Outputs: 3
    
    # When both pointers go out of scope, the dictionary is freed
```

**Context:**
- Purpose: Reference-counted smart pointer for shared ownership
- Patterns: Use for data that needs to be shared among multiple owners
- Alternatives: `OwnedPointer` when exclusive ownership is sufficient
- Limitations: Thread-safety for reference counting only, not for data access
- Related: `OwnedPointer[T]`, `Pointer[T]`
- Behavior: Automatically manages memory using reference counting
- Performance: Small overhead for reference count operations

**Edge Cases and Anti-patterns:**
- Common Mistakes: Creating reference cycles that prevent memory from being freed
- Anti-patterns:
```mojo
# ANTI-PATTERN (potential reference cycle):
struct Node:
    var value: Int
    var next: ArcPointer[Node]
    
    fn __init__(inout self, value: Int):
        self.value = value
        # self.next will be initialized separately

# Creating a cycle that can't be freed automatically:
fn create_cycle():
    var node1 = Node(1)
    var node2 = Node(2)
    
    var ptr1 = ArcPointer(node1^)
    var ptr2 = ArcPointer(node2^)
    
    # Create a cycle
    ptr1[].next = ptr2
    ptr2[].next = ptr1  # Creates reference cycle
```

### `UnsafePointer[T]` [`STABLE`]

**Package:** `mojo.stdlib.memory.unsafe_pointer`  
**Available Since:** `v0.3.0`  
**Status:** Stable  

**Signature:**
```mojo
struct UnsafePointer[T: AnyType]:
    var address: UInt
    
    fn __init__(inout self)  # Null pointer
    fn __init__(inout self, address: UInt)
    
    @staticmethod
    fn address_of(borrowed value: T) -> Self
    @staticmethod
    fn alloc(count: Int = 1) -> Self
    
    fn __getitem__(self) -> T
    fn __getitem__(self, offset: Int) -> T
    fn __setitem__(inout self, value: T)
    fn __setitem__(inout self, offset: Int, value: T)
    
    fn init_pointee_copy(self, value: T)
    fn init_pointee_move(self, value: owned T)
    fn destroy_pointee(self)
    fn take_pointee(self) -> T
    fn move_pointee_into(self, dst: Self)
    
    fn free(self)
    fn bitcast[U: AnyType](self) -> UnsafePointer[U]
    fn offset(self, count: Int) -> Self
    fn is_null(self) -> Bool
    
    # SIMD operations
    fn strided_load[width: Int](self, stride: Int) -> SIMD[T, width]
    fn strided_store[width: Int](self, value: SIMD[T, width], stride: Int)
    fn gather[width: Int](self, offsets: SIMD[Int, width]) -> SIMD[T, width]
    fn scatter[width: Int](self, values: SIMD[T, width], offsets: SIMD[Int, width])
```

**Dependencies/Imports:**
```mojo
from memory.unsafe_pointer import UnsafePointer
```

**Usage Example:**
```mojo
from memory.unsafe_pointer import UnsafePointer

fn unsafe_pointer_example():
    # Allocate memory for 5 integers
    var ptr = UnsafePointer[Int].alloc(5)
    
    # Initialize memory values
    for i in range(5):
        ptr.offset(i).init_pointee_copy(i * 10)
    
    # Read values using array-like syntax
    for i in range(5):
        print(ptr[i], end=" ")  # Outputs: 0 10 20 30 40
    print()
    
    # Modify values
    ptr[2] = 25
    
    # Free memory when done
    ptr.free()
```

**Context:**
- Purpose: Low-level pointer for direct memory manipulation and allocation
- Patterns: For implementing collections, memory pools, or FFI
- Alternatives: Use safe pointer types when possible
- Limitations: No memory safety guarantees or lifetime tracking
- Related: `Pointer[T]`, `OwnedPointer[T]`, `ArcPointer[T]`
- Behavior: Nullable, can access uninitialized memory, supports pointer arithmetic
- Performance: Zero overhead, equivalent to C/C++ raw pointers

**Edge Cases and Anti-patterns:**
- Common Mistakes: Memory leaks, use-after-free, double-free
- Anti-patterns:
```mojo
# ANTI-PATTERN (memory leak):
fn memory_leak():
    let ptr = UnsafePointer[Int].alloc(10)
    # WRONG: Missing ptr.free()

# ANTI-PATTERN (use after free):
fn use_after_free():
    let ptr = UnsafePointer[Int].alloc(1)
    ptr.init_pointee_copy(42)
    ptr.free()
    let value = ptr[]  # WRONG: Accessing freed memory

# ANTI-PATTERN (uninitialized access):
fn uninitialized_access():
    let ptr = UnsafePointer[Int].alloc(1)
    let value = ptr[]  # WRONG: Accessing uninitialized memory
```

**Security Considerations:**
- [SECURITY-SENSITIVE] Can circumvent Mojo's memory safety guarantees
- Can lead to memory corruption, buffer overflows, and security vulnerabilities
- Always validate array bounds before accessing elements
- Never use with untrusted input without proper validation

## Advanced Usage

### Memory Management Patterns [`STABLE`]

**Available Since:** `v0.3.0`  
**Status:** Stable  

**Usage Example:**
```mojo
from memory.unsafe_pointer import UnsafePointer

struct Buffer:
    var data: UnsafePointer[UInt8]
    var size: Int
    
    fn __init__(inout self, size: Int):
        self.size = size
        self.data = UnsafePointer[UInt8].alloc(size)
        # Initialize memory to zero
        for i in range(size):
            self.data[i] = 0
        
    fn __del__(owned self):
        self.data.free()
        
    fn __copyinit__(inout self, other: Self):
        self.size = other.size
        self.data = UnsafePointer[UInt8].alloc(self.size)
        # Deep copy the data
        for i in range(self.size):
            self.data[i] = other.data[i]
            
    fn get(self, index: Int) -> UInt8:
        if index >= 0 and index < self.size:
            return self.data[index]
        return 0
        
    fn set(inout self, index: Int, value: UInt8):
        if index >= 0 and index < self.size:
            self.data[index] = value

fn buffer_example():
    var buf = Buffer(10)
    buf.set(0, 42)
    buf.set(1, 43)
    print(buf.get(0), buf.get(1))  # Outputs: 42 43
    
    # Copy the buffer
    var buf2 = buf
    buf2.set(0, 100)
    
    # Original buffer remains unchanged
    print(buf.get(0))  # Outputs: 42
    print(buf2.get(0))  # Outputs: 100
```

**Context:**
- Purpose: RAII-style memory management with automatic cleanup
- Patterns: Encapsulating unsafe pointers in safe abstractions
- Alternatives: Using standard library collections when possible
- Related: `UnsafePointer[T]`
- Behavior: Deterministic resource management with constructors and destructors
- Performance: Minimal overhead compared to manual memory management

### SIMD Vector Operations [`STABLE`]

**Available Since:** `v0.3.0`  
**Status:** Stable  

**Usage Example:**
```mojo
from memory.unsafe_pointer import UnsafePointer

fn simd_operations():
    # Allocate memory for 16 UInt8 values
    var ptr = UnsafePointer[UInt8].alloc(16)
    
    # Initialize with sequential values
    for i in range(16):
        ptr[i] = i
    
    # Load 8 values with stride of 2 (every other value)
    let stride = 2
    let simd_width = 8
    let values = ptr.strided_load[width=simd_width](stride)
    
    # Print the loaded values: 0, 2, 4, 6, 8, 10, 12, 14
    for i in range(simd_width):
        print(values[i], end=" ")
    print()
    
    # Gather values from specific offsets
    var offsets = SIMD[Int, 4](0, 5, 10, 15)
    let gathered = ptr.gather[width=4](offsets)
    
    # Print gathered values: 0, 5, 10, 15
    for i in range(4):
        print(gathered[i], end=" ")
    print()
    
    # Free the memory
    ptr.free()
```

**Context:**
- Purpose: Efficient vectorized memory operations for SIMD processing
- Patterns: For processing image data, scientific computing, or performance-critical code
- Related: `UnsafePointer[T].strided_load`, `UnsafePointer[T].gather`, `UnsafePointer[T].scatter`
- Performance: Highly optimized for SIMD hardware acceleration

## Platform-Specific

### FFI with C/C++ [`STABLE`]

**Available Since:** `v0.3.0`  
**Status:** Stable  

**Usage Example:**
```mojo
from sys.ffi import external_call
from memory.unsafe_pointer import UnsafePointer

struct CString:
    var ptr: UnsafePointer[UInt8]
    
    fn __init__(inout self, string: String):
        # Allocate memory for string + null terminator
        let size = len(string) + 1
        self.ptr = UnsafePointer[UInt8].alloc(size)
        
        # Copy string data
        for i in range(len(string)):
            self.ptr[i] = ord(string[i])
        
        # Add null terminator
        self.ptr[len(string)] = 0
        
    fn __del__(owned self):
        self.ptr.free()
    
    fn c_ptr(self) -> UnsafePointer[UInt8]:
        return self.ptr

fn call_c_strlen():
    var cstr = CString("Hello, World!")
    
    # Call C's strlen function
    let length = external_call[
        "strlen",  # C function name
        Int,       # Return type
        UnsafePointer[UInt8]  # Parameter type
    ](cstr.c_ptr())
    
    print("String length:", length)  # Outputs: String length: 13
```

**Context:**
- Purpose: Interoperability with C/C++ libraries and system calls
- Patterns: Converting between Mojo and C data structures
- Limitations: No automatic type checking across language boundaries
- Related: `UnsafePointer[T]`, `external_call()`
- Behavior: Follows C calling conventions and memory layout
- Performance: Zero overhead compared to native C calls

**Edge Cases and Anti-patterns:**
- Common Mistakes: Not handling ownership of memory allocated by foreign code
- Anti-patterns:
```mojo
# ANTI-PATTERN (memory management mismatch):
fn memory_mismatch():
    # Call C function that returns allocated memory
    let c_ptr = external_call["c_malloc", UnsafePointer[UInt8], Int](100)
    
    # WRONG: Using Mojo's free on memory allocated by C
    c_ptr.free()
    
    # CORRECT: Use corresponding C function
    external_call["c_free", None, UnsafePointer[UInt8]](c_ptr)
```

**Security Considerations:**
- [SECURITY-SENSITIVE] No bounds checking on C-allocated buffers
- Validate all data returned from C functions before use
- Be careful with C functions that may modify memory unexpectedly

### Integration with Python [`STABLE`]

**Available Since:** `v0.3.0`  
**Status:** Stable  

**Usage Example:**
```mojo
from python import Python
from memory.unsafe_pointer import UnsafePointer

fn numpy_integration():
    # Import NumPy
    let np = Python.import_module("numpy")
    
    # Create a NumPy array
    let array = np.array([1, 2, 3, 4, 5], dtype=np.int32)
    
    # Get pointer to NumPy data
    let ptr = array.ctypes.data.unsafe_get_as_pointer[DType.int32]()
    
    # Modify the array through the pointer
    ptr[2] = 30
    
    # Print the array to see the modification
    print(array)  # Outputs: [1 2 30 4 5]
```

**Context:**
- Purpose: Interacting with Python libraries and data
- Patterns: Efficiently processing Python data in Mojo without copying
- Related: `PythonObject.unsafe_get_as_pointer()`, `UnsafePointer[T]`
- Performance: Minimal overhead when accessing Python data

## Migration

### From Manual Memory Management to Safe Pointers [`EXPERIMENTAL`]

**Migration Example:**
```mojo
# BEFORE: Manual memory management with UnsafePointer
fn old_style():
    let ptr = UnsafePointer[Int].alloc(1)
    ptr.init_pointee_copy(42)
    # Use ptr...
    print(ptr[])
    ptr.free()

# AFTER: Using OwnedPointer
fn new_style():
    var ptr = OwnedPointer(42)
    # Use ptr...
    print(ptr[])
    # No need to free memory - handled automatically
```

**Migration Difficulty:** Easy - direct replacement with higher-level abstraction

### From C-style Arrays to Safe Collections [`STABLE`]

**Migration Example:**
```mojo
# BEFORE: C-style array using UnsafePointer
fn old_array_style():
    let size = 10
    let ptr = UnsafePointer[Int].alloc(size)
    
    # Initialize array
    for i in range(size):
        ptr[i] = i * 10
    
    # Use array...
    for i in range(size):
        print(ptr[i], end=" ")
    print()
    
    # Free memory
    ptr.free()

# AFTER: Using Mojo List
fn new_list_style():
    var list = List[Int]()
    
    # Initialize list
    for i in range(10):
        list.append(i * 10)
    
    # Use list...
    for i in range(len(list)):
        print(list[i], end=" ")
    print()
    
    # No need to free memory - handled automatically
```

**Migration Difficulty:** Medium - requires restructuring code to use collection APIs

## Further Documentation

- [Mojo Pointers Documentation](https://docs.modular.com/mojo/manual/pointers/) - Complete overview of pointer types in Mojo
- [Unsafe Pointers Guide](https://docs.modular.com/mojo/manual/pointers/unsafe-pointers) - Detailed information on using UnsafePointer
- [Mojo Standard Library Reference](https://docs.modular.com/mojo/stdlib/) - Complete API documentation for all pointer types
- [Memory Safety in Mojo](https://docs.modular.com/mojo/programming-manual.html#memory-safety) - Overview of Mojo's memory safety features
- [Foreign Function Interface Guide](https://docs.modular.com/mojo/manual/interop/) - Information on interoperating with C/C++ and Python