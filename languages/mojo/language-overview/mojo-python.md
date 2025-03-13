# TITLE: Mojo Python Integration
VERSION: March 2025
COMPATIBILITY: Requires compatible Python runtime and Magic/conda environment
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/manual/python/
MODEL: Claude-3.7-Sonnet-Thinking

## Conceptual Overview

- Mojo integrates with Python, allowing you to import Python modules, call Python functions, and interact with Python objects directly from Mojo code
- Python code runs in a standard CPython interpreter, maintaining compatibility with existing Python code and ecosystem
- Mojo provides automatic type conversion between Mojo primitive types and Python objects
- Python integration helps bridge the gap while Mojo's ecosystem is still developing, giving access to Python's extensive library ecosystem

## Core Features

### Python Environment Integration [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
from python import Python

// Configure Python environment
Python.add_to_path(String) -> None
```

**Dependencies/Imports:**
```mojo
from python import Python
```

**Usage Example:**
```mojo
from python import Python

def main():
    # Add current directory to Python path
    Python.add_to_path(".")
    
    # Import your Python module
    my_module = Python.import_module("mymodule")
```

**Context:**
- Purpose: Configures the Python runtime environment for Mojo integration
- Patterns: Configure paths before importing modules
- Alternatives: Using Magic or conda for environment management
- Related: `import_module()`, Python environment management

**Edge Cases and Anti-patterns:**
- Common Mistakes: Not setting up a proper Python environment with required dependencies
- Edge Cases: Path resolution follows Python's module lookup rules

### Module Import [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
Python.import_module(String) -> PythonObject
```

**Dependencies/Imports:**
```mojo
from python import Python
```

**Usage Example:**
```mojo
from python import Python

def main():
    # Import NumPy module
    np = Python.import_module("numpy")
    
    # Use NumPy functionality
    array = np.array([1, 2, 3])
    print(array)
```

**Context:**
- Purpose: Imports Python modules for use in Mojo code
- Patterns: Import modules and access their attributes via the returned object
- Limitations: Can only import whole modules, not individual members
- Behavior: Raises exceptions if module isn't found; multiple imports of the same module won't re-run initialization

**Edge Cases and Anti-patterns:**
- Common Mistakes: Not handling potential exceptions from import failures
- Edge Cases: Must be called inside a function (not at top level)
- Gotchas: Must use the module reference to access members, can't directly import classes or functions

### Python Evaluation [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
Python.evaluate(String, file: Bool = False, name: String = "") -> PythonObject
```

**Dependencies/Imports:**
```mojo
from python import Python
```

**Usage Example:**
```mojo
from python import Python

def main():
    # Evaluate Python expression
    py_set = Python.evaluate('{2, 3, 2, 7, 11, 3}')
    
    # Create in-memory Python module
    py_module = """
def type_printer(value):
    print(type(value))
"""
    py_utils = Python.evaluate(py_module, file=True, name="py_utils")
    
    # Use the dynamically created function
    py_utils.type_printer(4)
```

**Context:**
- Purpose: Executes Python code and returns the result
- Patterns: Useful for creating Python objects without direct Mojo equivalents
- Related: `PythonObject` wrapper for interoperability

**Edge Cases and Anti-patterns:**
- Common Mistakes: Not handling potential exceptions from evaluation errors
- Edge Cases: When `file=True`, code is executed as a module

## APIs

### Python Object Wrapper [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
struct PythonObject:
    // Dunder methods for Python interoperability
    fn __getattr__(self, name: String) -> PythonObject
    fn __getitem__(self, key: AnyType) -> PythonObject
    fn __setitem__(self, inout self, key: AnyType, value: AnyType)
    
    // Trait implementations
    fn __str__(self) -> String  // Stringable
    fn __bool__(self) -> Bool   // Boolable
    fn __int__(self) -> Int     // Intable
    fn __float__(self) -> Float64  // Floatable
```

**Dependencies/Imports:**
```mojo
from python import PythonObject
```

**Usage Example:**
```mojo
from python import PythonObject

def main():
    // Create a Python list
    var py_list: PythonObject = ["cat", 2, 3.14159, 4]
    
    // Access and modify items
    n = py_list[2]
    print("n =", n)
    py_list.append(5)
    py_list[0] = "aardvark"
    print(py_list)
    
    // Convert to Mojo native types
    var s = String(py_list[0])
    var i = Int(py_list[1])
    var f = Float64(py_list[2])
}
```

**Context:**
- Purpose: Provides a wrapper around Python objects for seamless interoperability
- Patterns: Use dot notation for attributes/methods and bracket notation for item access
- Behavior: Automatically converts between Mojo and Python types when possible

**Edge Cases and Anti-patterns:**
- Common Mistakes: Not explicitly converting to Mojo native types when needed
- Gotchas: Some operations may require explicit conversion between Python and Mojo types

### Python Collections [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
Python.dict() -> PythonObject  // Creates empty Python dictionary
Python.list() -> PythonObject  // Creates empty Python list
```

**Dependencies/Imports:**
```mojo
from python import Python
```

**Usage Example:**
```mojo
from python import Python

def main():
    // Create a Python dictionary
    py_dict = Python.dict()
    py_dict["item_name"] = "whizbang"
    py_dict["price"] = 11.75
    py_dict["inventory"] = 100
    print(py_dict)
    
    // Create a Python list
    py_list = Python.list()
    py_list.append("first")
    py_list.append(42)
    print(py_list)
}
```

**Context:**
- Purpose: Creates Python collection objects that support heterogeneous types
- Patterns: Useful when Mojo's native collections lack needed features
- Alternatives: Mojo's homogeneous `Dict` and `List` types

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using Python collections where Mojo native collections would be more efficient
- Gotchas: Performance impact from Python/Mojo boundary crossing

## Type Conversion

### Mojo to Python Type Conversion [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Context:**
- Mojo primitive types automatically convert to Python equivalents
- Supported conversions:
  - Mojo `Int` → Python `int`
  - Mojo `Float64` → Python `float`
  - Mojo `Bool` → Python `bool`
  - Mojo `String` → Python `str`
  - Mojo tuples → Python `tuple`
  - Mojo `ListLiteral` → Python `list`

**Usage Example:**
```mojo
from python import Python

def main():
    py_module = """
def type_printer(value):
    print(type(value))
"""
    py_utils = Python.evaluate(py_module, file=True, name="py_utils")
    
    // Mojo values automatically convert to Python types
    py_utils.type_printer(4)           // <class 'int'>
    py_utils.type_printer(3.14)        // <class 'float'>
    py_utils.type_printer(("Mojo", True))  // <class 'tuple'>
```

### Python to Mojo Type Conversion [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Context:**
- Python objects can be explicitly converted to Mojo types using constructors
- `PythonObject` implements conversion traits:
  - `Stringable` - Convert to Mojo `String`
  - `Boolable` - Convert to Mojo `Bool`
  - `Intable` - Convert to Mojo `Int`
  - `Floatable` - Convert to Mojo `Float64`
  - `Writable` - Support for Mojo `print()` function

**Usage Example:**
```mojo
from python import Python, PythonObject

def main():
    var py_string: PythonObject = "hello"
    var py_int: PythonObject = 42
    var py_float: PythonObject = 3.14
    var py_bool: PythonObject = True
    
    // Convert to Mojo native types
    var s = String(py_string)
    var i = Int(py_int)
    var f = Float64(py_float)
    var b = Bool(py_bool)
}
```

### Python Type Comparison and Testing [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
Python.type(PythonObject) -> PythonObject
```

**Dependencies/Imports:**
```mojo
from python import Python
```

**Usage Example:**
```mojo
from python import Python, PythonObject

def main():
    var value: PythonObject = 3.7
    
    // Check value in boolean context
    if value > 3:
        print("Value is greater than 3")
    
    // Compare Python object identities
    value2 = value
    if value2 is value:
        print("Same object")
    
    // Check Python type
    py_float_type = Python.evaluate("float")
    if Python.type(value) is py_float_type:
        print("Value is a Python float")
}
```

**Context:**
- Purpose: Inspects and compares Python objects and their types
- Patterns: Uses Python's type system for type checking
- Behavior: Supports value comparisons, identity comparisons with `is`, and type checking

## Advanced Usage

### Working with Local Python Modules [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Signature:**
```mojo
Python.add_to_path(String) -> None
```

**Dependencies/Imports:**
```mojo
from python import Python
```

**Usage Example:**
```mojo
from python import Python

def main():
    // Add local directory to Python's path
    Python.add_to_path(".")
    
    // Import local module
    my_module = Python.import_module("mymodule")
    
    // Use functions from the local module
    result = my_module.some_function(42)
    print(result)
}
```

**Context:**
- Purpose: Enables using local Python code in Mojo applications
- Patterns: First add path, then import module
- Related: Python module importing system

### Python UI Integration Pattern [`STABLE`]

**Package:** `python`
**Available Since:** Early Mojo releases
**Status:** Stable

**Context:**
- Purpose: Pattern for integrating with Python UI frameworks
- Limitations: Python can't directly call back into Mojo code
- Alternatives: Drive event loop from Mojo and poll for events

**Usage Example:**
```mojo
from python import Python

def main():
    Python.add_to_path(".")
    app = Python.import_module("my_ui_app").App()
    app.create("800x600")
    
    // Polling loop pattern for UI frameworks
    while True:
        app.update()  // Update UI
        
        // Check flags set by Python callbacks
        if app.button_clicked:
            handle_button_click()
            app.button_clicked = False
}

fn handle_button_click():
    print("Button was clicked!")
```

**Edge Cases and Anti-patterns:**
- Common Mistakes: Trying to pass Mojo callbacks to Python modules
- Gotchas: Event-driven frameworks require this polling approach from Mojo

## Limitations and Future Directions

- Can't currently call Mojo from Python (one-way integration)
- Not all Python features are yet implemented in Mojo
- Event-driven patterns require polling workarounds
- Python integration provides temporary bridge while Mojo ecosystem develops

## Further Documentation

- [Mojo Python Integration](https://docs.modular.com/mojo/manual/python/)
- [Python Types in Mojo](https://docs.modular.com/mojo/manual/python/types/)
- [PythonObject API Reference](https://docs.modular.com/mojo/stdlib/python/python_object/PythonObject)
- [Python Module API Reference](https://docs.modular.com/mojo/stdlib/python/python/Python)