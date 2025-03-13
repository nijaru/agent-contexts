# Mojo Value Ownership and Lifecycle

## Metadata Section
```
TITLE: Mojo Value Ownership and Lifecycle System
VERSION: Mojo Documentation as of March 2025
COMPATIBILITY: Mojo 0.5.0+
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/manual/values/
MODEL: Claude-3.7-Sonnet-Thinking
```

## Conceptual Overview

- Mojo implements a unique memory management system based on value ownership that provides memory safety without garbage collection
- Every value has exactly one owner at any given time, with clear rules for transferring ownership between variables
- Values are destroyed deterministically as soon as they're no longer used (ASAP destruction)
- Mojo provides argument conventions (`read`, `mut`, `owned`, `ref`) that control how values are passed to functions
- The lifecycle system enables developers to control how values are created, copied, moved, and destroyed

## Technical Reference

### Memory Management Foundation [`STABLE`]

**Package:** `mojo.memory`
**Available Since:** `v0.1.0`
**Status:** Stable

**Context:**
- Purpose: Mojo's memory management system divides memory into stack (for automatic local data) and heap (for dynamic data)
- Patterns: Stack memory is managed automatically by the compiler, heap memory is managed by type authors implementing lifecycle methods
- Alternatives: Garbage collection (Python, Java), manual management (C, C++), reference counting (Swift, Rust)
- Behavior: Deterministic memory management with strict ownership rules and ASAP destruction

Mojo's memory management strategy is built around value ownership, providing memory safety guarantees while maintaining deterministic behavior. Unlike garbage-collected languages that may wait to clean up memory, Mojo destroys values as soon as they're no longer needed in the program flow.

Each variable in Mojo owns its value, and ownership can be transferred between variables using explicit syntax. This ensures that at any given time, every value has exactly one owner, preventing common memory errors like use-after-free and double-free.

**Edge Cases and Anti-patterns:**
- Common Mistakes: Attempting to use a variable after transferring its ownership
- Edge Cases: Partially initialized structs cannot be used until all fields are initialized
- Gotchas: ASAP destruction means values are destroyed immediately after their last use, not at the end of scope

### Value Semantics [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Context:**
- Purpose: Provides predictable behavior for how values are shared and modified
- Patterns: Each variable maintains exclusive ownership of its value
- Related: Value ownership, argument conventions, lifetime tracking

Mojo's value semantics ensure that when you share a value-semantic type, you're creating a copy of the value, not sharing a reference. This means modifications to one variable don't affect other variables holding what appears to be the "same" value.

**Usage Example:**
```mojo
x = 1
y = x  # creates a copy
y += 1

print(x)  # Prints 1
print(y)  # Prints 2
```

When passing arguments to functions, `def` and `fn` functions behave differently:

- In `def` functions, arguments are mutable by default (but operate on a copy of the value)
- In `fn` functions, arguments are immutable by default (to avoid unnecessary copies)

**Edge Cases and Anti-patterns:**
- Gotchas: A Python programmer might expect reference semantics for objects, while Mojo uses value semantics by default
- Anti-patterns: Assuming that a function can modify the caller's value without an explicit `mut` argument

```mojo
# ANTI-PATTERN (Python programmer expectation):
def update_list(list):
    list.append(3)  # In Python, this would modify the original list

# CORRECT in Mojo:
def update_list(mut list: List[Int]):
    list.append(3)  # 'mut' explicitly indicates the function will modify the original value
```

### Argument Conventions [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
# Function with various argument conventions
fn example(
    read immutable_arg: Type,          # Immutable reference (default)
    mut mutable_arg: Type,             # Mutable reference
    owned transfer_arg: Type,          # Ownership transfer
    ref [origin] parametric_arg: Type  # Parametric mutability
):
    # Function body
```

**Context:**
- Purpose: Control how values are passed between functions while maintaining memory safety
- Patterns: Explicit declaration of mutability and ownership
- Behavior: Ensures predictable behavior for function arguments
- Related: Value ownership, value semantics, lifetimes

Mojo argument conventions explicitly declare how a function accesses its parameters, enabling memory optimizations while maintaining value semantics.

#### `read` Arguments (Default)

By default, all arguments use the `read` convention, which provides immutable access to the original value.

```mojo
fn print_value(value: Int):  # 'read' is implicit
    print(value)
    # value += 1  # Error: cannot modify a 'read' argument in 'fn'
```

Important differences between `fn` and `def` functions:
- In `fn` functions, `read` arguments are always immutable references
- In `def` functions, `read` arguments may be copies if the function attempts to mutate them

#### `mut` Arguments

The `mut` convention provides mutable access to the original value.

```mojo
fn increment(mut value: Int):
    value += 1  # Modifies the original value

var x = 5
increment(x)
print(x)  # Prints 6
```

Mojo enforces argument exclusivity for mutable references, meaning a value cannot be passed as both `mut` and `read` simultaneously.

#### `owned` Arguments

The `owned` convention transfers ownership of a value to the function.

```mojo
fn consume(owned value: String):
    print(value)
    # 'value' is destroyed at the end of the function

var message = String("Hello")
consume(message)  # Makes a copy by default
print(message)    # Still valid, prints "Hello"

consume(message^) # Transfers ownership with the ^ sigil
# print(message)  # Error: 'message' is no longer initialized
```

The `^` transfer sigil explicitly ends the lifetime of a variable and transfers its value.

#### `ref` Arguments

The `ref` convention provides parametric mutability, allowing a function to accept either mutable or immutable references.

```mojo
fn process[is_mutable: Bool, origin: Origin[is_mutable]](
    ref [origin] value: String
):
    @parameter
    if is_mutable:
        value += "!"  # Only allowed if the reference is mutable
    else:
        print(value)  # Read-only access
```

### Value Lifecycle [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Context:**
- Purpose: Defines how values are created, copied, moved, and destroyed
- Patterns: Each lifecycle event is handled by a specific method
- Related: Value ownership, argument conventions, initialization rules

The lifecycle of a Mojo value is controlled by special methods that define how it behaves during creation, copying, moving, and destruction.

#### Constructors

The `__init__` method initializes a value, typically by setting all fields.

```mojo
struct Person:
    var name: String
    var age: Int

    fn __init__(out self, name: String, age: Int):
        self.name = name
        self.age = age
```

Constructors can be overloaded to support different initialization patterns:

```mojo
fn __init__(out self):  # Default constructor
    self.name = ""
    self.age = 0

fn __init__(out self, name: String):  # Partial constructor
    self = Self()  # Call default constructor
    self.name = name
```

#### Copy Constructor

The `__copyinit__` method defines how a value is copied.

```mojo
fn __copyinit__(out self, existing: Self):
    self.name = existing.name  # Creates a copy of the string
    self.age = existing.age
```

Mojo expects copy constructors to perform deep copies, creating entirely new instances of all component values.

#### Move Constructor

The `__moveinit__` method defines how a value is moved (ownership transfer).

```mojo
fn __moveinit__(out self, owned existing: Self):
    self.name = existing.name^  # Transfer ownership of the string
    self.age = existing.age
```

Move constructors are typically more efficient than copies for types with heap-allocated resources.

#### Destructor

The `__del__` method defines how a value is destroyed.

```mojo
fn __del__(owned self):
    # Release any resources owned by this value
    # E.g., deallocate memory, close file handles, etc.
```

Mojo automatically calls destructors as soon as a value is no longer used (ASAP destruction).

**Usage Example:**
```mojo
struct HeapArray:
    var data: UnsafePointer[Int]
    var size: Int

    fn __init__(out self, size: Int, val: Int):
        self.size = size
        self.data = UnsafePointer[Int].alloc(self.size)
        for i in range(self.size):
            (self.data + i).init_pointee_copy(val)

    fn __copyinit__(out self, existing: Self):
        # Deep copy
        self.size = existing.size
        self.data = UnsafePointer[Int].alloc(self.size)
        for i in range(self.size):
            (self.data + i).init_pointee_copy(existing.data[i])

    fn __moveinit__(out self, owned existing: Self):
        # Shallow copy (ownership transfer)
        self.size = existing.size
        self.data = existing.data
        # existing is invalidated, no destructor call

    fn __del__(owned self):
        # Clean up allocated memory
        for i in range(self.size):
            (self.data + i).destroy_pointee()
        self.data.free()
```

### Lifetime Tracking [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Context:**
- Purpose: Ensures references remain valid and prevents memory safety issues
- Patterns: The compiler tracks the lifetime of each value and prevents invalid accesses
- Behavior: Fields can be tracked independently within composite types

Mojo's lifetime checker is a compiler pass that analyzes dataflow through your program, identifying when variables are valid and inserting destructor calls when a variable's lifetime ends.

**Edge Cases and Anti-patterns:**
- Common Mistakes: Attempting to use a reference after its source has been destroyed
- Gotchas: Field lifetimes are tracked independently, so a struct can be partially initialized

```mojo
struct Person:
    var name: String
    var age: Int

fn example():
    var p = Person("Alice", 30)
    consume(p.name^)  # Transfer ownership of just the name field
    # use(p)  # Error: p.name is uninitialized

    p.name = String("Bob")  # Reinitialize the field
    use(p)  # OK: p is fully initialized again
```

### Origin Values [`STABLE`]

**Package:** `mojo.core.memory`
**Available Since:** `v0.1.0`
**Status:** Stable

**Context:**
- Purpose: Track variable lifetimes and reference validity
- Patterns: Origin values represent the "source" of a reference, including its mutability
- Related: Lifetime tracking, reference safety

Origin values are special compiler-managed values that track the lifetime and mutability of references. They are used by Mojo's lifetime checker to ensure references remain valid.

```mojo
struct Span[
    is_mutable: Bool,
    T: CollectionElement,
    origin: Origin[is_mutable]
]:
    var _data: UnsafePointer[T]
    var _len: Int

    fn __init__(out self, ref [origin] list: List[T, *_]):
        # Create a span that refers to the list data
        self._data = list.data
        self._len = len(list)
```

Origins can be:
- Derived from existing values using `__origin_of(value)`
- Inferred from function arguments
- Specified as static for program-lifetime values
- Combined to represent multiple source origins

### ASAP Destruction [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Context:**
- Purpose: Free resources as soon as they're no longer needed
- Patterns: Values are destroyed immediately after their last use
- Alternatives: Scope-based destruction (C++), garbage collection (Python, Java)
- Behavior: Deterministic, predictable cleanup

Mojo uses an "as soon as possible" (ASAP) destruction policy that destroys values immediately after their last use, rather than waiting until the end of a scope.

```mojo
fn example():
    var a = MyType()
    var b = MyType()
    print(a.field)
    # a is destroyed here since it's no longer needed

    print(b.field)
    # b is destroyed here
```

This approach provides deterministic resource management and optimized memory usage.

**Edge Cases and Anti-patterns:**
- Gotchas: Values may be destroyed before the end of a scope, unlike C++ RAII
- Edge Cases: Within an expression like `a + b + c`, intermediate values are destroyed as soon as they're no longer needed

For special cases where the compiler cannot correctly determine the last use, you can use:

```mojo
# Keep a value alive longer than the compiler would:
_ = value  # 'value' is kept alive until this point

# Or use a with statement:
with open_file() as file:
    # 'file' is guaranteed to stay alive for the entire with block
    process_file(file)
```

### Value Decorator [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
@value
struct SimpleType:
    var field1: Int
    var field2: String
    # No need to implement __init__, __copyinit__, __moveinit__
```

**Context:**
- Purpose: Automatically generate lifecycle methods for simple value types
- Patterns: Eliminates boilerplate constructor code for common cases
- Related: Value lifecycle, constructors

The `@value` decorator automatically synthesizes the `__init__`, `__copyinit__`, and `__moveinit__` methods for simple structs, eliminating the need for boilerplate code.

**Usage Example:**
```mojo
@value
struct Point:
    var x: Int
    var y: Int

    # These methods are automatically generated:
    # fn __init__(out self, x: Int, y: Int)
    # fn __copyinit__(out self, existing: Self)
    # fn __moveinit__(out self, owned existing: Self)

    # You can still define custom methods:
    fn distance_from_origin(self) -> Float64:
        return (self.x * self.x + self.y * self.y).sqrt()
```

### Register-Passable Types [`STABLE`]

**Package:** `mojo.core`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
@register_passable("trivial")
struct Int:
    var value: __mlir_type.index

    fn __init__(value: __mlir_type.index) -> Int:
        return Self {value: value}
```

**Context:**
- Purpose: Optimize small value types to be passed in CPU registers
- Patterns: Types marked as "trivial" have no user-defined lifecycle methods
- Performance: Significantly faster than passing through memory

The `@register_passable` decorator marks types that should be passed in CPU registers rather than through memory. This is a significant performance enhancement for small "trivial" types like integers and floats.

```mojo
@register_passable("trivial")
struct Complex:
    var real: Float64
    var imag: Float64

    fn __init__(real: Float64, imag: Float64 = 0) -> Self:
        return Self{real: real, imag: imag}
```

## Further Documentation

- [Mojo Value Ownership Reference](https://docs.modular.com/mojo/manual/values/ownership/)
- [Value Semantics Guide](https://docs.modular.com/mojo/manual/values/value-semantics/)
- [Lifetimes and References](https://docs.modular.com/mojo/manual/values/lifetimes/)
- [Value Lifecycle: Creation and Copying](https://docs.modular.com/mojo/manual/lifecycle/life/)
- [Value Lifecycle: Destruction](https://docs.modular.com/mojo/manual/lifecycle/death/)
