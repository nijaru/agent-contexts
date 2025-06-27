# EmberJson Technical Documentation

## Metadata Section
```
TITLE: EmberJson
VERSION: Latest
DOCUMENTATION_SOURCE: https://github.com/bgreni/EmberJson, https://builds.modular.com/packages/emberjson
MODEL: Claude-3.7-Sonnet
```

## Conceptual Overview

- EmberJson is a lightweight, user-friendly JSON parsing library implemented in pure Mojo
- Provides intuitive APIs for parsing JSON strings and converting Mojo objects to JSON format
- Features high performance with customizable parsing options for speed/accuracy tradeoffs
- Supports all standard JSON data types (objects, arrays, strings, numbers, booleans, null)
- Implements Unicode support with escaped character handling

## Technical Reference

### Core Components

#### Parse Function [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
fn parse(json_str: String) -> JSON
fn parse[options: ParseOptions](json_str: String) -> JSON
```

**Dependencies/Imports:**
```mojo
from emberjson import parse
```

**Usage Example:**
```mojo
from emberjson import parse

// Basic parsing
var json = parse('{"key": 123}')

// With custom parse options
from emberjson import parse, ParseOptions
var json = parse[ParseOptions(fast_float_parsing=True)]('{"key": 123.456}')
```

**Context:**
- Purpose: Main entry point for converting JSON strings into Mojo objects
- Patterns: Accepts raw JSON strings and returns a structured JSON object 
- Alternatives: None in standard Mojo currently
- Behavior: Throws an error on invalid JSON input

#### ParseOptions Struct [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
struct ParseOptions:
    var fast_float_parsing: Bool  # Use faster but potentially less accurate float parsing
    var ignore_unicode: Bool      # Skip unicode handling for performance
```

**Dependencies/Imports:**
```mojo
from emberjson import ParseOptions
```

**Usage Example:**
```mojo
from emberjson import parse, ParseOptions

// Parse with fast float parsing (may reduce accuracy)
var options = ParseOptions(fast_float_parsing=True)
var json = parse[options]('{"value": 123.456}')

// Parse ignoring unicode handling for better performance
var json = parse[ParseOptions(ignore_unicode=True)]('["simple string"]')
```

**Context:**
- Purpose: Configure the JSON parser's behavior to optimize for performance or accuracy
- Fast float parsing can significantly improve performance when parsing large numeric datasets
- Ignoring Unicode can boost performance when handling ASCII-only content

#### to_string Function [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
fn to_string(json: JSON) -> String
fn to_string[pretty: Bool = False](json: JSON) -> String
```

**Dependencies/Imports:**
```mojo
from emberjson import to_string
```

**Usage Example:**
```mojo
from emberjson import parse, to_string

var json = parse('{"key": 123}')

// Basic serialization
print(to_string(json))  // Prints: {"key":123}

// Pretty-printed serialization
print(to_string[pretty=True](json))
// Prints:
// {
//   "key": 123
// }
```

**Context:**
- Purpose: Converts JSON objects back to string representation
- Patterns: Outputs compact JSON by default, with optional pretty-printing
- Related: JSON object supports Stringable, Representable, and Writable traits

### JSON Value Types

#### JSON [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
struct JSON:
    fn is_object(self) -> Bool
    fn is_array(self) -> Bool
    fn object(self) -> Object  # Returns Object if valid, otherwise raises error
    fn array(self) -> Array    # Returns Array if valid, otherwise raises error
    
    // Subscript operator for dictionary-style access
    fn __getitem__(self, key: String) -> Value
    // Subscript operator for array-style access
    fn __getitem__(self, index: Int) -> Value
```

**Dependencies/Imports:**
```mojo
from emberjson import JSON
```

**Usage Example:**
```mojo
from emberjson import parse

var json = parse('{"name": "Mojo", "values": [1, 2, 3]}')

// Check type
if json.is_object():
    print("JSON is an object")

// Access object elements (dictionary style)
var name = json["name"].string()  // "Mojo"

// Access nested arrays
var values = json["values"]
var first_value = values[0].int()  // 1
```

**Context:**
- Purpose: Top-level JSON document representation
- Contains either an Object or Array as its root element
- Provides type checking and convenient access methods

#### Value [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
struct Value:
    // Type checking methods
    fn is_string(self) -> Bool
    fn is_int(self) -> Bool
    fn is_float(self) -> Bool
    fn is_bool(self) -> Bool
    fn is_object(self) -> Bool
    fn is_array(self) -> Bool
    fn is_null(self) -> Bool
    
    // Value extraction methods
    fn string(self) -> String
    fn int(self) -> Int
    fn float(self) -> Float64
    fn bool(self) -> Bool
    fn object(self) -> Object
    fn array(self) -> Array
    
    // Implicitly create Value from various types
    fn __init__(inout self, val: String)
    fn __init__(inout self, val: Int)
    fn __init__(inout self, val: Float64)
    fn __init__(inout self, val: Bool)
    fn __init__(inout self, val: NoneType)  // For null values
    
    // Equality checking
    fn __eq__(self, other: Value) -> Bool
```

**Dependencies/Imports:**
```mojo
from emberjson import Value
```

**Usage Example:**
```mojo
from emberjson import parse, Value, Null

var json = parse('{"name": "Mojo", "count": 42, "enabled": true, "factor": 3.14, "data": null}')

// Check types and extract values
if json["name"].is_string():
    print(json["name"].string())  // "Mojo"

var count = json["count"].int()      // 42
var enabled = json["enabled"].bool() // true
var factor = json["factor"].float()  // 3.14

// Check for null
if json["data"].is_null():
    print("Data is null")

// Compare with null
if json["data"] == Null():
    print("Data is null (alternate check)")

// Create Value instances
var string_val: Value = "example"
var int_val: Value = 123
var null_val: Value = None
```

**Context:**
- Purpose: Represents any valid JSON value type
- Wraps Int, Float64, String, Bool, Object, Array, and Null types
- Provides type checking and type-safe value extraction
- Supports implicit construction from basic types

#### Object [`STABLE`]

**Package:** `emberjson`
**Status:** Stable  

**Signature:**
```mojo
struct Object:
    // Dictionary-style access
    fn __getitem__(self, key: String) -> Value
    fn __setitem__(inout self, key: String, val: Value)
    
    // Convert to standard Mojo Dict
    fn to_dict(owned self) -> Dict[String, Value]
    
    // Create empty object
    fn __init__(inout self)
    
    // Check if key exists
    fn contains(self, key: String) -> Bool
```

**Dependencies/Imports:**
```mojo
from emberjson import Object
```

**Usage Example:**
```mojo
from emberjson import parse, Object, Value

var json = parse('{"name": "Mojo", "version": 1}')
var obj = json.object()

// Access values
var name = obj["name"].string()

// Check if key exists
if obj.contains("version"):
    print("Version:", obj["version"].int())

// Create and populate a new object
var new_obj = Object()
new_obj["name"] = "EmberJson"
new_obj["type"] = "library"

// Convert to Dict
var dict = obj.to_dict()
```

**Context:**
- Purpose: Represents a JSON object (key-value pairs)
- Patterns: Provides dictionary-like access to properties
- Behavior: Keys must be strings, values can be any JSON value type

#### Array [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
struct Array:
    // Array-style access
    fn __getitem__(self, index: Int) -> Value
    fn __setitem__(inout self, index: Int, val: Value)
    
    // Size information
    fn size(self) -> Int
    
    // Convert to standard Mojo List
    fn to_list(owned self) -> List[Value]
    
    // Create empty array
    fn __init__(inout self)
    
    // Create array with values
    fn __init__(inout self, *values: Value)
```

**Dependencies/Imports:**
```mojo
from emberjson import Array
```

**Usage Example:**
```mojo
from emberjson import parse, Array, Value

var json = parse('[1, 2, 3, "four", true]')
var arr = json.array()

// Access by index
var first = arr[0].int()  // 1
var fourth = arr[3].string()  // "four"

// Get size
print("Array size:", arr.size())  // 5

// Create a new array
var new_arr = Array(123, "string", False)

// Convert to List
var list = arr.to_list()
```

**Context:**
- Purpose: Represents a JSON array (ordered collection of values)
- Patterns: Provides indexed access to elements
- Behavior: Elements can be any valid JSON value type

#### Null [`STABLE`]

**Package:** `emberjson`
**Status:** Stable

**Signature:**
```mojo
struct Null:
    fn __init__(inout self)
    fn __eq__(self, other: Value) -> Bool
```

**Dependencies/Imports:**
```mojo
from emberjson import Null
```

**Usage Example:**
```mojo
from emberjson import parse, Null

var json = parse('{"data": null}')

// Check for null using is_null()
if json["data"].is_null():
    print("Data is null")

// Check for null using equality
if json["data"] == Null():
    print("Data is null (alternate check)")

// None in Mojo converts implicitly to Null
assert(json["data"] == Value(None))
```

**Context:**
- Purpose: Represents the JSON null value
- Patterns: Use for explicit null checks
- Behavior: None values in Mojo convert implicitly to Null

## Installation and Setup

### Prerequisites

- Mojo programming language (latest version)

### Installation

To use EmberJson in your Mojo project:

1. Add the mojo-community channel to your mojoproject.toml:
```toml
[project]
channels = [
    "conda-forge", 
    "https://conda.modular.com/max", 
    "https://repo.prefix.dev/mojo-community"
]
```

2. Add EmberJson to your dependencies:
```toml
[dependencies]
emberjson = "latest"
```

3. Run the Mojo installation command:
```
magic install
```

## Usage Examples

### Basic Parsing and Access

```mojo
from emberjson import parse

// Parse a JSON string
var json = parse('{"name": "EmberJson", "version": 1, "features": ["parsing", "serialization"]}')

// Access object properties
print(json["name"].string())  // "EmberJson"
print(json["version"].int())  // 1

// Access array elements
var features = json["features"]
print(features[0].string())  // "parsing"
print(features[1].string())  // "serialization"
```

### JSON Creation and Serialization

```mojo
from emberjson import Object, Array, Value, to_string

// Create a JSON object
var obj = Object()
obj["name"] = "EmberJson"
obj["type"] = "library"

// Create a JSON array
var arr = Array(1, 2, 3, "four")

// Add array to object
obj["values"] = Value(arr)

// Serialize to string
print(to_string(obj))  // {"name":"EmberJson","type":"library","values":[1,2,3,"four"]}

// Pretty-print
print(to_string[pretty=True](obj))
// {
//   "name": "EmberJson",
//   "type": "library",
//   "values": [
//     1,
//     2,
//     3,
//     "four"
//   ]
// }
```

### Performance Optimization

```mojo
from emberjson import parse, ParseOptions

// Fast parsing with potentially reduced float accuracy
var options = ParseOptions(fast_float_parsing=True)
var json = parse[options]('{"data": [1.2345, 2.3456, 3.4567]}')

// Skip Unicode handling for ASCII-only content
var ascii_json = parse[ParseOptions(ignore_unicode=True)]('{"status": "ok"}')
```

## Known Limitations

- No streaming parser for large files
- Limited error reporting on parse failures
- Parsed objects are currently not modifiable after creation
- No schema validation capabilities
- Limited serialization options compared to more mature JSON libraries

## Performance Considerations

- Use `fast_float_parsing=True` for numeric-heavy JSON when exact precision isn't critical
- Enable `ignore_unicode=True` when dealing with ASCII-only content
- For large JSON objects, consider working with the parsed structure rather than repeatedly serializing/deserializing
- Converting to standard Mojo types (via `to_dict()` and `to_list()`) are consuming operations, so only use when necessary
