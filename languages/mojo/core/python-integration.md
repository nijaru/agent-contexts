TITLE: Mojo Python Integration
VERSION: 0.6.0
RELEASED: 2024-03-01
COMPATIBILITY: Python 3.8+, macOS, Linux
DOCUMENTATION_SOURCE: https://docs.modular.com/mojo/manual/python/
MODEL: Claude-3.7-Sonnet-Thinking

# Mojo Python Integration

## Conceptual Overview

- Mojo provides seamless interoperability with Python libraries and code
- The `python` module enables importing and using Python modules directly in Mojo
- Python objects are wrapped as `PythonObject` instances which can be used naturally with Mojo syntax
- Mojo's performance optimization capabilities can be applied to Python code
- Python types can be converted to and from native Mojo types

## Python Integration

### Python Module [`STABLE`]

**Package:** `python`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
module Python:
    @staticmethod
    fn import_module(name: String) -> PythonObject: ...
    
    @staticmethod
    fn evaluate(code: String) -> PythonObject: ...
    
    @staticmethod
    fn object_from_address(addr: Int) -> PythonObject: ...
```

**Dependencies/Imports:**
```mojo
from python import Python, PythonObject
```

**Usage Example:**
```mojo
from python import Python, PythonObject

def use_numpy():
    # Import a Python module
    np = Python.import_module("numpy")
    
    # Create a numpy array
    arr = np.array([1, 2, 3, 4])
    mean = arr.mean()
    print("Mean:", mean)
    
    # Iterate over Python collections
    for value in arr:
        print(value)
```

**Context:**
- Purpose: Bridge between Mojo and Python ecosystems
- Patterns: Import Python modules, call Python functions, use Python objects
- Limitations: Performance overhead when crossing the Mojo-Python boundary
- Performance: Python integration incurs some overhead, so batch operations when possible

**Edge Cases and Anti-patterns:**
```mojo
# ANTI-PATTERN (crossing boundary repeatedly):
from python import Python
np = Python.import_module("numpy")
arr = np.array([1, 2, 3, 4])
total = 0
for i in range(len(arr)):
    total += Int(arr[i])  # Crossing boundary for each element

# BETTER:
total_py = arr.sum()
total = Int(total_py)  # Cross boundary only once
```

### PythonObject [`STABLE`]

**Package:** `python`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
struct PythonObject:
    # Attributes access
    fn __getattr__(self, name: String) -> PythonObject: ...
    fn __setattr__(self, mut self, name: String, value: PythonObject): ...
    
    # Method invocation
    fn __call__(self, *args: PythonObject, **kwargs: PythonObject) -> PythonObject: ...
    
    # Indexing
    fn __getitem__(self, idx: PythonObject) -> PythonObject: ...
    fn __setitem__(self, mut self, idx: PythonObject, value: PythonObject): ...
    
    # Iteration
    fn __iter__(self) -> PythonObject: ...
    fn __next__(self, it: PythonObject) raises -> PythonObject: ...
```

**Usage Example:**
```mojo
from python import Python, PythonObject

def work_with_python_types():
    # Create Python dictionaries
    dict_module = Python.import_module("builtins")
    py_dict = dict_module.dict()
    
    # Set values
    py_dict["key1"] = "value1"
    py_dict["key2"] = 42
    
    # Access values
    print(py_dict["key1"])  # Prints: value1
    
    # Iterate over a Python object
    for key in py_dict:
        print("Key:", key, "Value:", py_dict[key])
```

**Context:**
- Purpose: Wrapper for Python objects in Mojo
- Patterns: Access attributes, call methods, use indexing, iterate over collections
- Behavior: Follows Python's reference semantics, not Mojo's value semantics
- Related: Used with `Python.import_module()` to interact with Python libraries

### Type Conversion [`STABLE`]

**Package:** `python`
**Available Since:** `v0.1.0`
**Status:** Stable

**Signature:**
```mojo
# Python to Mojo conversion constructors
Int(py_int: PythonObject) -> Int
Float64(py_float: PythonObject) -> Float64
Bool(py_bool: PythonObject) -> Bool
String(py_str: PythonObject) -> String

# Mojo to Python conversion
PythonObject(value: Int) -> PythonObject
PythonObject(value: Float64) -> PythonObject
PythonObject(value: Bool) -> PythonObject
PythonObject(value: String) -> PythonObject
```

**Usage Example:**
```mojo
from python import Python, PythonObject

def convert_types():
    # Python to Mojo conversion
    np = Python.import_module("numpy")
    py_value = np.int64(42)
    mojo_int = Int(py_value)
    print("Mojo Int:", mojo_int)
    
    # Mojo to Python conversion
    mojo_string = String("Hello from Mojo")
    py_string = PythonObject(mojo_string)
    
    builtins = Python.import_module("builtins")
    builtins.print("Python sees:", py_string)
```

**Context:**
- Purpose: Convert between Mojo and Python data types
- Patterns: Use constructors to convert Python objects to Mojo types
- Limitations: Not all Python types have direct Mojo equivalents
- Performance: Type conversion adds overhead, so minimize conversions in tight loops

### Working with NumPy [`STABLE`]

**Package:** `python.numpy`
**Available Since:** `v0.2.0`
**Status:** Stable

**Dependencies/Imports:**
```mojo
from python import Python, PythonObject
```

**Usage Example:**
```mojo
from python import Python, PythonObject

def numpy_integration():
    # Import numpy
    np = Python.import_module("numpy")
    
    # Create arrays
    arr1 = np.array([[1, 2, 3], [4, 5, 6]])
    arr2 = np.array([[7, 8, 9], [10, 11, 12]])
    
    # Perform operations
    result = np.dot(arr1, arr2.T)
    print(result)
    
    # Access shape information
    shape = result.shape
    dims = Int(shape[0]), Int(shape[1])
    print("Result dimensions:", dims)
    
    # Convert to Mojo types if needed
    for i in range(Int(shape[0])):
        for j in range(Int(shape[1])):
            element = Int(result[i, j])
            print(element, end=" ")
        print()
```

**Context:**
- Purpose: Leverage NumPy's numerical computation capabilities in Mojo
- Patterns: Create arrays, perform operations, access results
- Performance: Use NumPy's vectorized operations for better performance
- Alternatives: For performance-critical sections, consider using Mojo's SIMD types directly

## Python/Mojo Interoperability Best Practices

### Minimizing Boundary Crossings [`STABLE`]

**Usage Example:**
```mojo
from python import Python, PythonObject

def efficient_python_interop():
    np = Python.import_module("numpy")
    
    # GOOD: Perform calculations in Python
    data = np.random.rand(1000, 1000)
    result = np.mean(data, axis=0)  # Let NumPy do the calculation
    
    # Only convert what you need to Mojo
    first_mean = Float64(result[0])
    
    # BAD: Cross the boundary in a loop
    # for i in range(1000):
    #     for j in range(1000):
    #         sum += Float64(data[i, j])  # Crossing boundary repeatedly
```

**Context:**
- Purpose: Optimize performance when working with Python code
- Patterns: Perform computation-heavy operations in the Python domain before crossing to Mojo
- Performance: Each boundary crossing has overhead, so batch operations when possible

### Exception Handling with Python [`STABLE`]

**Usage Example:**
```mojo
from python import Python, PythonObject

def handle_python_exceptions():
    # Import Python modules
    np = Python.import_module("numpy")
    
    try:
        # Intentionally cause an error in Python
        result = np.array([1, 2, 3]) / 0
    except:
        print("Caught Python exception")
    
    # Alternatively, check for error conditions
    file_module = Python.import_module("builtins").open
    try:
        f = file_module("nonexistent_file.txt", "r")
    except:
        print("File not found")
```

**Context:**
- Purpose: Properly handle errors from Python code
- Patterns: Use Mojo's `try`-`except` blocks to catch Python exceptions
- Behavior: Python exceptions are converted to Mojo exceptions when they cross the boundary

### Memory Management Considerations [`STABLE`]

**Context:**
- Python objects follow Python's reference counting garbage collection
- Mojo objects held by Python are properly reference counted
- When holding large Python objects in Mojo, explicitly release references when done
- Be careful with circular references between Mojo and Python objects

### Python Module Loading [`STABLE`]

**Usage Example:**
```mojo
from python import Python, PythonObject

fn ensure_module_installed() raises -> PythonObject:
    try:
        return Python.import_module("pandas")
    except:
        # Attempt to install the module
        pip = Python.import_module("pip.main")
        pip.main(["install", "pandas"])
        # Try importing again
        return Python.import_module("pandas")
```

**Context:**
- Purpose: Handle Python dependency management in Mojo code
- Patterns: Check if modules are available and install if needed
- Limitations: Requires appropriate permissions for installation