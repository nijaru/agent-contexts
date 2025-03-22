# Mojo `Dict` Collection

## Metadata

```
TITLE: Mojo Dict Collection
VERSION: Current
DOCUMENTATION_SOURCE: Mojo stdlib source code
MODEL: Claude-3.7-Sonnet
```

## Conceptual Overview

- Key-value mapping container with O(1) amortized average-time complexity for insert, lookup, and removal
- Keys must implement `KeyElement` trait (Movable, Hashable, EqualityComparable)
- Values must implement `CollectionElement` trait
- Insertion order is preserved when iterating (like Python's `dict`)
- Performance is optimized for small dictionaries, but can scale to large collections
- Implements a hash table with open addressing and linear probing similar to Python's `dict`

## Core Features

### Dict[K, V] `STABLE`

**Package:** `collections`

**Signature:**
```mojo
struct Dict[K: KeyElement, V: CollectionElement](Sized, CollectionElement, CollectionElementNew, Boolable)
```

**Dependencies/Imports:**
```mojo
from collections import Dict
```

**Usage Example:**
```mojo
from collections import Dict

var d = Dict[String, Int]()
d["hello"] = 1
d["world"] = 2

print(len(d))  # prints 2
print(d["hello"])  # prints 1

for key in d:
    print(key)  # prints keys in insertion order

# Check if key exists
if "hello" in d:
    print("Key exists!")

# Access with default value if key doesn't exist
var value = d.get("missing", 42)  # returns 42

# Remove a key
var removed = d.pop("world")  # returns 2
print(len(d))  # prints 1
```

**Context:**
- Purpose: Provides an efficient, type-safe dictionary implementation for key-value storage
- Patterns: Hash-based implementation with open addressing
- Limitations:
  - Keys must implement `KeyElement` trait
  - Values must implement `CollectionElement` trait
- Behavior:
  - Thread-safety: Not thread-safe by default
  - Deterministic iteration in insertion order
  - Maximum load factor of 2/3, after which the dictionary resizes
- Performance:
  - O(1) average case for lookup, insert, and delete operations
  - O(n) worst case when many hash collisions occur

**Edge Cases and Anti-patterns:**
- Common Mistakes: Not checking if key exists before accessing with `__getitem__`
- Anti-patterns:
```mojo
# ANTI-PATTERN (can raise):
var value = d["missing_key"]  # Raises if key doesn't exist

# CORRECT:
# Use get with default
var value = d.get("missing_key", default_value)

# Or check first
if "missing_key" in d:
    var value = d["missing_key"]
```
- Edge Cases:
  - Hash collisions can degrade performance to O(n) in worst case
  - Removing many entries without adding new ones doesn't automatically shrink the dictionary

## APIs

### Constructors

#### `__init__` `STABLE`

**Signature:**
```mojo
fn __init__(out self)
```

Creates an empty dictionary with default capacity.

**Usage Example:**
```mojo
var d = Dict[String, Int]()
```

#### `__init__` (with capacity) `STABLE`

**Signature:**
```mojo
fn __init__(out self, *, power_of_two_initial_capacity: Int)
```

Creates an empty dictionary with a specific initial capacity.

**Usage Example:**
```mojo
# Create dictionary with initial capacity of 1024
var d = Dict[String, Int](power_of_two_initial_capacity=1024)
```

**Context:**
- Purpose: Pre-allocate memory for a dictionary when you know approximately how many elements it will hold
- Constraints: `power_of_two_initial_capacity` must be ≥ 8 and a power of two

#### Static Constructor Methods

#### `fromkeys` `STABLE`

**Signature:**
```mojo
@staticmethod
fn fromkeys(keys: List[K, *_], value: V) -> Self
```

Creates a new dictionary with keys from list and values set to the given value.

**Usage Example:**
```mojo
var keys = List[String]()
keys.append("a")
keys.append("b")
keys.append("c")

var d = Dict[String, Int].fromkeys(keys, 1)
# d now contains {"a": 1, "b": 1, "c": 1}
```

#### `fromkeys` (with optional value) `STABLE`

**Signature:**
```mojo
@staticmethod
fn fromkeys(keys: List[K, *_], value: Optional[V] = None) -> Dict[K, Optional[V]]
```

Creates a new dictionary with keys from list and values set to the given optional value (default None).

### Operators

#### `__getitem__` `STABLE`

**Signature:**
```mojo
fn __getitem__(self, key: K) raises -> ref V
```

Retrieves a reference to a value from the dictionary by key.

**Usage Example:**
```mojo
var value = d["key"]  # Raises if key doesn't exist
```

**Edge Cases:**
- Raises `KeyError` if the key is not in the dictionary

#### `__setitem__` `STABLE`

**Signature:**
```mojo
fn __setitem__(mut self, owned key: K, owned value: V)
```

Sets a value in the dictionary by key.

**Usage Example:**
```mojo
d["key"] = 42  # Add or update a value
```

**Context:**
- Overwrites existing value if key already exists
- Adds new entry if key doesn't exist
- May trigger dictionary resize if load factor exceeds 2/3

#### `__contains__` `STABLE`

**Signature:**
```mojo
fn __contains__(self, key: K) -> Bool
```

Checks if a key exists in the dictionary.

**Usage Example:**
```mojo
if "key" in d:
    # Key exists
```

#### `__iter__` `STABLE`

**Signature:**
```mojo
fn __iter__(ref self) -> _DictKeyIter[K, V, __origin_of(self)]
```

Returns an iterator over the dictionary's keys in insertion order.

**Usage Example:**
```mojo
for key in d:
    print(key)
```

#### `__reversed__` `STABLE`

**Signature:**
```mojo
fn __reversed__(ref self) -> _DictKeyIter[K, V, __origin_of(self), False]
```

Returns a reversed iterator over the dictionary's keys.

**Usage Example:**
```mojo
for key in __reversed__(d):
    print(key)  # Keys in reverse insertion order
```

#### `__or__` `STABLE`

**Signature:**
```mojo
fn __or__(self, other: Self) -> Self
```

Merges two dictionaries and returns the result as a new dictionary.

**Usage Example:**
```mojo
var d1 = Dict[String, Int]()
d1["a"] = 1
var d2 = Dict[String, Int]()
d2["b"] = 2

var combined = d1 | d2  # {"a": 1, "b": 2}
```

**Context:**
- When both dictionaries have the same key, the value from the right-hand dictionary (`other`) is used

#### `__ior__` `STABLE`

**Signature:**
```mojo
fn __ior__(mut self, other: Self)
```

Updates the dictionary with key/value pairs from another dictionary.

**Usage Example:**
```mojo
var d1 = Dict[String, Int]()
d1["a"] = 1
var d2 = Dict[String, Int]()
d2["b"] = 2

d1 |= d2  # d1 now contains {"a": 1, "b": 2}
```

#### `__len__` `STABLE`

**Signature:**
```mojo
fn __len__(self) -> Int
```

Returns the number of key-value pairs in the dictionary.

**Usage Example:**
```mojo
var count = len(d)
```

#### `__bool__` `STABLE`

**Signature:**
```mojo
fn __bool__(self) -> Bool
```

Returns `True` if the dictionary is not empty, `False` otherwise.

**Usage Example:**
```mojo
if d:
    print("Dictionary is not empty")
```

### Methods

#### `find` `STABLE`

**Signature:**
```mojo
fn find(self, key: K) -> Optional[V]
```

Finds a value in the dictionary by key.

**Usage Example:**
```mojo
var maybe_value = d.find("key")
if maybe_value:
    var value = maybe_value.value()
```

#### `get_ptr` `STABLE`

**Signature:**
```mojo
fn get_ptr(ref self, key: K) -> Optional[Pointer[V, __origin_of(self._entries[0].value().value)]]
```

Gets a pointer to a value in the dictionary by key.

**Usage Example:**
```mojo
var ptr = d.get_ptr("key")
if ptr:
    var value = ptr.value()[]
```

#### `get` `STABLE`

**Signature:**
```mojo
fn get(self, key: K) -> Optional[V]
```

Gets a value from the dictionary by key as an Optional.

**Usage Example:**
```mojo
var maybe_value = d.get("key")
if maybe_value:
    var value = maybe_value.value()
```

#### `get` (with default) `STABLE`

**Signature:**
```mojo
fn get(self, key: K, default: V) -> V
```

Gets a value from the dictionary by key, or returns the default if the key doesn't exist.

**Usage Example:**
```mojo
var value = d.get("key", 42)  # Returns 42 if key doesn't exist
```

#### `pop` `STABLE`

**Signature:**
```mojo
fn pop(mut self, key: K) raises -> V
```

Removes and returns a value from the dictionary by key.

**Usage Example:**
```mojo
try:
    var value = d.pop("key")
except:
    print("Key not found")
```

**Edge Cases:**
- Raises `KeyError` if the key is not in the dictionary

#### `pop` (with default) `STABLE`

**Signature:**
```mojo
fn pop(mut self, key: K, owned default: V) -> V
```

Removes and returns a value from the dictionary by key, or returns the default if the key doesn't exist.

**Usage Example:**
```mojo
var value = d.pop("key", 42)  # Returns 42 if key doesn't exist
```

#### `popitem` `STABLE`

**Signature:**
```mojo
fn popitem(mut self) raises -> DictEntry[K, V]
```

Removes and returns the last inserted key-value pair from the dictionary.

**Usage Example:**
```mojo
try:
    var entry = d.popitem()
    print(entry.key, entry.value)
except:
    print("Dictionary is empty")
```

**Edge Cases:**
- Raises `KeyError` if the dictionary is empty
- Useful for destructively iterating through the dictionary

#### `keys` `STABLE`

**Signature:**
```mojo
fn keys(ref self) -> _DictKeyIter[K, V, __origin_of(self)]
```

Returns an iterator over the dictionary's keys.

**Usage Example:**
```mojo
for key in d.keys():
    print(key)
```

#### `values` `STABLE`

**Signature:**
```mojo
fn values(ref self) -> _DictValueIter[K, V, __origin_of(self)]
```

Returns an iterator over the dictionary's values.

**Usage Example:**
```mojo
for value in d.values():
    print(value[])
```

#### `items` `STABLE`

**Signature:**
```mojo
fn items(ref self) -> _DictEntryIter[K, V, __origin_of(self)]
```

Returns an iterator over the dictionary's key-value pairs.

**Usage Example:**
```mojo
for entry in d.items():
    print(entry[].key, entry[].value)
```

#### `update` `STABLE`

**Signature:**
```mojo
fn update(mut self, other: Self)
```

Updates the dictionary with key-value pairs from another dictionary.

**Usage Example:**
```mojo
var d1 = Dict[String, Int]()
d1["a"] = 1
var d2 = Dict[String, Int]()
d2["b"] = 2

d1.update(d2)  # d1 now contains {"a": 1, "b": 2}
```

**Context:**
- Equivalent to using the `|=` operator
- Overwrites values for existing keys

#### `clear` `STABLE`

**Signature:**
```mojo
fn clear(mut self)
```

Removes all key-value pairs from the dictionary.

**Usage Example:**
```mojo
d.clear()  # Dictionary is now empty
```

#### `setdefault` `STABLE`

**Signature:**
```mojo
fn setdefault(mut self, key: K, owned default: V) raises -> ref V
```

Gets a value from the dictionary by key, or sets it to a default if it doesn't exist.

**Usage Example:**
```mojo
var value = d.setdefault("key", 42)  # Sets "key" to 42 if it doesn't exist
```

**Context:**
- Returns a reference to the existing value if the key exists
- Otherwise, inserts the default value and returns a reference to it

## Support Types

### DictEntry `STABLE`

**Signature:**
```mojo
@value
struct DictEntry[K: KeyElement, V: CollectionElement](CollectionElement, CollectionElementNew)
```

Stores a key-value pair entry inside a dictionary.

**Fields:**
- `hash`: UInt64 - Cached hash value of the key
- `key`: K - The key
- `value`: V - The associated value

**Usage Context:**
- Returned by the `popitem()` method
- Used when iterating over dictionary items

### KeyElement `STABLE`

**Signature:**
```mojo
trait KeyElement(CollectionElement, Hashable, EqualityComparable)
```

A trait composition for types which implement all requirements of dictionary keys.

**Context:**
- Dict keys must minimally be Movable, Hashable, and EqualityComparable
- Currently also requires CollectionElement and Copyable traits until references are fully implemented

## Implementation Details

The Dict implementation uses a hash table with open addressing and linear probing:

- Elements are stored in a dense array with insertion order preserved
- A separate index structure maps hash slots to entry indices
- Resizing occurs when the load factor exceeds 2/3
- Compaction happens when many entries are removed to maintain performance
- The initial capacity starts at 8 and grows by doubling
- The hash function and probe sequence are similar to Python's dict implementation

## Performance Characteristics

- Average case time complexity:
  - Lookup: O(1)
  - Insert: O(1) amortized
  - Delete: O(1) amortized
- Worst case time complexity (when many hash collisions occur):
  - All operations: O(n)
- Space complexity:
  - O(n) where n is the number of entries
  - Approximately 3/2 * n space is used due to load factor constraints

## Advanced Usage Patterns

### Type Constraints and Custom Types

When using custom types as dictionary keys, they must implement the required traits:

```mojo
struct MyKey(KeyElement):
    var id: Int

    fn __init__(inout self, id: Int):
        self.id = id

    fn __hash__(self) -> UInt64:
        return UInt64(self.id)

    fn __eq__(self, other: Self) -> Bool:
        return self.id == other.id

var d = Dict[MyKey, String]()
d[MyKey(1)] = "one"
```

### Memory Pre-allocation

For performance-critical code where you know the approximate size in advance:

```mojo
# Pre-allocate a dictionary that can hold ~682 entries without resizing
var d = Dict[String, Int](power_of_two_initial_capacity=1024)
```

### Dictionary Composition

Merging dictionaries to create a new one:

```mojo
var config = defaults | user_settings | command_line_options
```

## Practical Examples

### Counting Occurrences

```mojo
fn count_frequencies(words: List[String]) -> Dict[String, Int]:
    var frequencies = Dict[String, Int]()
    for i in range(len(words)):
        var word = words[i]
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies
```

### Using as a Cache

```mojo
var cache = Dict[String, ComputedResult]()

fn get_result(key: String) -> ComputedResult:
    if key in cache:
        return cache[key]
    var result = compute_expensive_result(key)
    cache[key] = result
    return result
```

### Building a Lookup Table

```mojo
var lookup = Dict[Int, String]()
lookup[1] = "one"
lookup[2] = "two"
lookup[3] = "three"

fn number_to_word(n: Int) -> String:
    return lookup.get(n, "unknown")
```
