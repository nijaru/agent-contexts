# TITLE: Mojo Traits System and Parametric Polymorphism
VERSION: Mojo SDK v0.6.0 (March 2025)
COMPATIBILITY: Mojo SDK v0.6.0+
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/manual/traits/ and https://docs.modular.com/mojo/manual/parameters/
MODEL: Claude-3.7-Sonnet-Thinking

## Conceptual Overview

- Mojo's traits provide a powerful contract system for types, enabling polymorphism with static type checking
- Traits define requirements that conforming types must implement, similar to interfaces in other languages
- Parameters provide zero-cost compile-time metaprogramming, enabling generic programming
- The combination of traits and parameters enables expressive, statically-checked generic code
- Traits can express relationships between types through inheritance and associated aliases

## Traits System

### Traits [`STABLE`]

**Package:** `mojo.manual.traits`
**Available Since:** `v0.4.0`
**Status:** Stable

**Signature:**
```mojo
trait TraitName:
    # Method signatures that conforming types must implement
    fn required_method(self, arg: Type) -> ReturnType:
        ...
    
    # Static methods can also be required
    @staticmethod
    fn static_method() -> ReturnType:
        ...
```

**Usage Example:**
```mojo
trait Quackable:
    fn quack(self):
        ...

@value
struct Duck(Quackable):
    fn quack(self):
        print("Quack")

@value
struct StealthCow(Quackable):
    fn quack(self):
        print("Moo!")

fn make_it_quack[T: Quackable](maybe_a_duck: T):
    maybe_a_duck.quack()

make_it_quack(Duck())      # Prints: Quack
make_it_quack(StealthCow()) # Prints: Moo!
```

**Context:**
- Purpose: Traits define a set of requirements that types must implement, creating a contract for polymorphic code
- Patterns: Traits can include method signatures, static methods, and associated aliases
- Alternatives: Similar to Java interfaces, C++ concepts, Swift protocols, and Rust traits
- Related: Parameters system for generics enables parametric polymorphism
- Behavior: Traits are checked at compile-time, ensuring type safety without runtime overhead

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting to implement all required methods of a trait
- Edge Cases: Implicit trait conformance exists but explicit conformance is recommended for clarity and future features
- Gotchas: Traits can't be added to existing types from other modules or the standard library

### Trait Inheritance [`STABLE`]

**Signature:**
```mojo
trait ParentTrait:
    fn parent_method(self):
        ...

trait ChildTrait(ParentTrait):
    fn child_method(self):
        ...
```

**Usage Example:**
```mojo
trait Animal:
    fn make_sound(self):
        ...

trait Bird(Animal):
    fn fly(self):
        ...

# Multiple inheritance
trait Named:
    fn get_name(self) -> String:
        ...

trait NamedAnimal(Animal, Named):
    pass
```

**Context:**
- Purpose: Trait inheritance allows composition of behavior requirements
- Patterns: Child traits inherit all requirements from parent traits
- Behavior: A type conforming to a child trait must implement all methods from both child and parent traits

### Associated Aliases for Generics [`STABLE`]

**Signature:**
```mojo
trait TraitWithAlias:
    alias TypeAlias: Trait
    
    fn method(self, arg: Self.TypeAlias):
        ...
```

**Usage Example:**
```mojo
trait Stacklike:
    alias EltType: CollectionElement
    
    def push(mut self, owned item: Self.EltType):
        pass
    
    def pop(mut self) -> Self.EltType:
        pass

struct MyStack[T: CollectionElement](Stacklike):
    """A simple Stack built using a List."""
    alias EltType = T
    alias list_type = List[Self.EltType]
    
    var list: Self.list_type
    
    fn __init__(out self):
        self.list = Self.list_type()
    
    def push(mut self, owned item: Self.EltType):
        self.list.append(item)
    
    def pop(mut self) -> Self.EltType:
        return self.list.pop()
```

**Context:**
- Purpose: Associated aliases allow traits to define required type relationships
- Patterns: Useful for creating generic containers that work with various element types
- Behavior: Implementing structs must provide concrete values for all associated aliases

### Implicit Trait Conformance [`STABLE`]

**Usage Example:**
```mojo
trait Quackable:
    fn quack(self):
        ...

# Explicitly conforming type
@value
struct Duck(Quackable):
    fn quack(self):
        print("Quack")

# Implicitly conforming type - doesn't declare the trait
struct RubberDucky:
    fn quack(self):
        print("Squeak!")

fn make_it_quack[T: Quackable](maybe_a_duck: T):
    maybe_a_duck.quack()

# Both work with the generic function
make_it_quack(Duck())       # Prints: Quack
make_it_quack(RubberDucky()) # Prints: Squeak!
```

**Context:**
- Purpose: Allows types to work with trait-constrained code without explicit declaration
- Patterns: Useful for working with types from libraries or standard library
- Limitations: Explicit conformance is recommended for documentation and future feature support

### Traits with Lifecycle Methods [`STABLE`]

**Signature:**
```mojo
trait DefaultConstructible:
    fn __init__(out self):
        ...

trait MassProducible(DefaultConstructible, Movable):
    pass

fn factory[T: MassProducible]() -> T:
    return T()
```

**Usage Example:**
```mojo
struct Thing(MassProducible):
    var id: Int
    
    fn __init__(out self):
        self.id = 0
    
    fn __moveinit__(out self, owned existing: Self):
        self.id = existing.id

var thing = factory[Thing]()
```

**Context:**
- Purpose: Ensures that types provide necessary lifecycle methods
- Patterns: Combine multiple traits to define complete type requirements
- Behavior: Factory functions can create instances of types that conform to lifecycle traits

## Built-in Traits

### Movable [`STABLE`]

**Package:** `mojo.stdlib.builtin.value`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
trait Movable:
    fn __moveinit__(out self, owned existing: Self):
        ...
```

**Context:**
- Purpose: Defines a contract for types that can be moved
- Patterns: Used to enforce safe transfer of resources between variables
- Related: Used by containers and algorithms that need to move values

### Copyable [`STABLE`]

**Package:** `mojo.stdlib.builtin.value`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
trait Copyable:
    fn __copyinit__(out self, existing: Self):
        ...
```

**Context:**
- Purpose: Defines a contract for types that can be copied
- Patterns: Used to enforce safe duplication of values
- Related: Used by containers and algorithms that need to copy values

### CollectionElement [`STABLE`]

**Package:** `mojo.stdlib.builtin.value`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
trait CollectionElement(Movable, Copyable):
    pass
```

**Usage Example:**
```mojo
struct Item(CollectionElement):
    var data: Int
    
    fn __init__(out self, data: Int):
        self.data = data
    
    fn __copyinit__(out self, existing: Self):
        self.data = existing.data
    
    fn __moveinit__(out self, owned existing: Self):
        self.data = existing.data
```

**Context:**
- Purpose: Defines the minimum requirements for types that can be stored in collections
- Patterns: A type must be both movable and copyable to be used in standard containers
- Related: Used by standard library containers like `List`

### Sized [`STABLE`]

**Package:** `mojo.stdlib.builtin.len`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
trait Sized:
    fn __len__(self) -> Int:
        ...
```

**Usage Example:**
```mojo
struct MyList(Sized):
    var size: Int
    
    fn __init__(out self):
        self.size = 0
    
    fn __len__(self) -> Int:
        return self.size

print(len(MyList()))  # Prints: 0
```

**Context:**
- Purpose: Defines types that have a measurable length
- Patterns: Used with the built-in `len()` function
- Related: Used by collection types and algorithms that need to know the size of containers

### Other Built-in Traits

The Mojo standard library includes many other traits:

- `Stringable` - Types convertible to a String (implements `__str__()`)
- `Representable` - Types with a canonical string representation (implements `__repr__()`)
- `Writable` - Types that can be written to a stream
- `Comparable` - Types that support comparison operators
- `Hashable` - Types that can be used as dictionary keys
- `Intable` - Types convertible to Int
- `AnyType` - Base trait that all types conform to
- And many more specialized traits for specific use cases

## Parametric Polymorphism

### Parameterized Functions [`STABLE`]

**Package:** `mojo.manual.parameters`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
fn function_name[param1: Type, param2: Type](arg1: Type, arg2: Type) -> ReturnType:
    # Function body
```

**Usage Example:**
```mojo
fn repeat[count: Int](msg: String):
    @parameter
    for i in range(count):
        print(msg)

repeat[3]("Hello")  # Prints "Hello" three times
```

**Context:**
- Purpose: Enables compile-time metaprogramming with zero runtime cost
- Patterns: Parameters are resolved at compile-time, generating specialized code
- Behavior: Creates a concrete version of the function for each unique parameter combination

### Generic Functions with Traits [`STABLE`]

**Signature:**
```mojo
fn generic_function[T: TraitConstraint](arg: T) -> ReturnType:
    # Function body using trait methods
```

**Usage Example:**
```mojo
fn stringify[T: Stringable](value: T) -> String:
    return String(value)

print(stringify(42))       # Prints: 42
print(stringify("hello"))  # Prints: hello
print(stringify(True))     # Prints: True
```

**Context:**
- Purpose: Combines traits and parameters to enable generic programming
- Patterns: Use trait constraints to ensure the generic type has required capabilities
- Behavior: Creates specialized implementations at compile time based on the actual types used

### Parameterized Structs for Generic Types [`STABLE`]

**Signature:**
```mojo
struct StructName[Param1: Type, Param2: Type]:
    var field1: Type
    var field2: Param1
    
    fn method(self, arg: Param2) -> ReturnType:
        # Method body
```

**Usage Example:**
```mojo
struct GenericArray[ElementType: CollectionElement]:
    var data: UnsafePointer[ElementType]
    var size: Int
    
    fn __init__(out self, *elements: ElementType):
        self.size = len(elements)
        self.data = UnsafePointer[ElementType].alloc(self.size)
        for i in range(self.size):
            (self.data + i).init_pointee_move(elements[i])
    
    fn __getitem__(self, i: Int) raises -> ref [self] ElementType:
        if (i < self.size):
            return self.data[i]
        else:
            raise Error("Out of bounds")

var array = GenericArray[Int](1, 2, 3, 4)
```

**Context:**
- Purpose: Allows creation of generic containers and algorithms
- Patterns: Type parameters specify the data types that the struct can work with
- Related: Used with traits to define type constraints

### Conditional Conformance [`STABLE`]

**Signature:**
```mojo
struct Generic[T: Trait1]:
    fn conditional_method[U: Trait2, //](self: Generic[U]) -> ReturnType:
        # Method implementation
```

**Usage Example:**
```mojo
@value
struct Container[ElementType: CollectionElement]:
    var element: ElementType
    
    def __str__[StrElementType: WritableCollectionElement, //](
            self: Container[StrElementType]) -> String:
        return String(self.element)

def use_container():
    float_container = Container(5)
    string_container = Container("Hello")
    print(float_container.__str__())  # Prints: 5
    print(string_container.__str__())  # Prints: Hello
```

**Context:**
- Purpose: Allows methods to be conditionally available based on more specific trait requirements
- Patterns: Define methods that only work with types meeting additional constraints
- Limitations: Currently, the specializations are not automatically recognized by trait conformance checking

### Parameter Inference [`STABLE`]

**Usage Example:**
```mojo
@value
struct One[Type: WritableCollectionElement]:
    var value: Type
    
    fn __init__(out self, value: Type):
        self.value = value

struct Two[Type: WritableCollectionElement]:
    var val1: Type
    var val2: Type
    
    fn __init__(out self, one: One[Type], another: One[Type]):
        self.val1 = one.value
        self.val2 = another.value
        print(String(self.val1), String(self.val2))

# Type parameter is inferred
var s1 = One(123)
var s2 = One("Hello")

# Type parameter is inferred from arguments
var s3 = Two(One("infer"), One("me"))  # Prints: infer me
```

**Context:**
- Purpose: Simplifies usage of parameterized types and functions
- Patterns: Type parameters can be inferred from arguments
- Behavior: The compiler deduces the concrete type at compile time

## Case Study: Implementing Generic Containers

### SIMD Type Example [`STABLE`]

**Signature:**
```mojo
struct SIMD[type: DType, size: Int]:
    var value: ...
    
    fn __init__(out self, *elems: SIMD[type, 1]):
        ...
    
    @staticmethod
    fn splat(x: SIMD[type, 1]) -> SIMD[type, size]:
        ...
    
    fn cast[target: DType](self) -> SIMD[target, size]:
        ...
```

**Usage Example:**
```mojo
var vector = SIMD[DType.int16, 4](1, 2, 3, 4)
vector = vector * vector
for i in range(4):
    print(vector[i], end=" ")  # Prints: 1 4 9 16
```

**Context:**
- Purpose: Demonstrates how parametric types enable hardware-specific optimizations
- Patterns: Type parameters allow for different data types and vector sizes
- Performance: Creates optimized machine code for specific hardware SIMD registers

## Migration

When migrating to Mojo from other languages, follow these guidelines:

### From Python:
```python
# BEFORE (Python):
class Duck:
    def quack(self):
        print("Quack.")

class StealthCow:
    def quack(self):
        print("Moo!")

def make_it_quack_python(maybe_a_duck):
    try:
        maybe_a_duck.quack()
    except:
        print("Not a duck.")
```

```mojo
# AFTER (Mojo with traits):
trait Quackable:
    fn quack(self):
        ...

@value
struct Duck(Quackable):
    fn quack(self):
        print("Quack")

@value
struct StealthCow(Quackable):
    fn quack(self):
        print("Moo!")

fn make_it_quack[T: Quackable](maybe_a_duck: T):
    maybe_a_duck.quack()
```

### From C++:
```cpp
// BEFORE (C++ templates and concepts):
template <typename T>
concept Stringable = requires(T a) {
    { a.to_string() } -> std::convertible_to<std::string>;
};

template <Stringable T>
std::string stringify(T value) {
    return value.to_string();
}
```

```mojo
# AFTER (Mojo traits and parameters):
trait Stringable:
    fn to_string(self) -> String:
        ...

fn stringify[T: Stringable](value: T) -> String:
    return value.to_string()
```

## Further Documentation

- [Mojo Traits Documentation](https://docs.modular.com/mojo/manual/traits/)
- [Mojo Parameters Documentation](https://docs.modular.com/mojo/manual/parameters/)
- [Mojo Lifecycle Documentation](https://docs.modular.com/mojo/manual/lifecycle/)
- [Mojo Standard Library](https://docs.modular.com/mojo/stdlib/)
- [Mojo on GitHub](https://github.com/modular-lang/mojo)