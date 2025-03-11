# TITLE: Python 3.13.0
VERSION: 3.13.0
RELEASED: 2024-10-07
COMPATIBILITY: macOS 10.13+, Windows, Linux
DOCUMENTATION_SOURCE: https://www.python.org/downloads/release/python-3130/

## Conceptual Overview

- Python 3.13.0 introduces major performance improvements through an experimental free-threaded mode without the GIL and a preliminary JIT compiler
- Enhanced developer experience with a new interactive interpreter featuring multi-line editing and colored output
- Strengthened typing system with type parameter defaults, type narrowing via TypeIs, and read-only TypeDict items
- Removed 19 deprecated "dead batteries" modules from the standard library (PEP 594)
- Added official support for mobile platforms (iOS and Android at Tier 3) and WASI at Tier 2

## Technical Reference

### Core Language

#### Interactive Interpreter [`STABLE`]

**Available Since:** `v3.13.0`
**Status:** Stable

**Context:**
- Purpose: Provides a greatly improved REPL experience
- Features: Multi-line editing, direct command support, color highlighting, help browsing
- Based on code from the PyPy project

**Usage Example:**
```python
# Simply run Python in interactive mode, no special commands needed
$ python
>>> # Multi-line editing is now supported
>>> # Colored output is enabled by default
```

**Environment Control:**
- Set `PYTHON_BASIC_REPL` to disable the new interpreter
- Control colors using `PYTHON_COLORS` or standard `NO_COLOR` environment variables
- Change history file location with `PYTHON_HISTORY` environment variable

#### Free-Threaded CPython [`EXPERIMENTAL`]

**Available Since:** `v3.13.0`
**Status:** Experimental

**Signature:**
```python
# Run the free-threaded Python binary:
$ python3.13t  # or python3.13t.exe on Windows

# Control GIL with environment variable:
$ PYTHON_GIL=0 python3.13t  # ensure GIL is disabled

# Or command-line option:
$ python3.13t -X gil=0
```

**Context:**
- Purpose: Enables true parallel execution by disabling the Global Interpreter Lock (GIL)
- Patterns: Allows full utilization of multi-core CPUs for threaded code
- Limitations: Experimental feature with potential bugs and performance impact for single-threaded code
- Performance: Programs designed with threading will see improved performance on multi-core systems

**Security Considerations:**
- C extensions need to be compiled specifically for free-threaded mode
- Extensions can indicate support via `Py_mod_gil` slot

**Migration Difficulty:** Complex
- Requires separate binary (python3.13t) from standard Python
- C extensions need updates to support free-threaded mode
- pip 24.1+ required for installing extensions in free-threaded mode

#### Just-In-Time (JIT) Compiler [`EXPERIMENTAL`]

**Available Since:** `v3.13.0`
**Status:** Experimental

**Signature:**
```bash
# Build with JIT support:
$ ./configure --enable-experimental-jit
# On Windows:
$ PCbuild/build.bat --experimental-jit

# Control at runtime:
$ PYTHON_JIT=0  # disable JIT
$ PYTHON_JIT=1  # enable JIT
```

**Context:**
- Purpose: Improves performance by compiling hot code paths to machine code
- Architecture:
  - Translates hot Tier 1 bytecode to Tier 2 IR (micro-ops)
  - Optimizes the Tier 2 IR
  - Translates optimized IR to machine code using copy-and-patch technique
- Limitations:
  - Currently disabled by default
  - Requires LLVM as a build-time dependency
  - Performance improvements are modest in this first release

#### locals() Semantics [`STABLE`]

**Available Since:** `v3.13.0`
**Status:** Stable

**Signature:**
```python
# PEP 667 defines semantics for mutating the return value of locals()
locals_dict = locals()
locals_dict['new_var'] = 42  # This now has well-defined behavior
```

**Context:**
- Purpose: Standardizes behavior for changing the returned mapping from `locals()`
- Changes: In optimized scopes (functions, generators, comprehensions, etc.), `locals()` now returns independent snapshots rather than a shared dict
- Impact: Enables debuggers to more reliably update local variables, even during concurrent execution

**Edge Cases:**
- Code execution functions targeting `locals()` (e.g., `exec()` and `eval()`) now operate on independent snapshots in optimized scopes
- `FrameType.f_locals` now returns a write-through proxy to frame's local and nonlocal variables

**Migration:** Medium
- Code that relied on undefined mutation behavior may need updates
- Explicit namespace references should be passed to code execution functions

### Typing System Enhancements

#### Type Parameter Defaults [`STABLE`]

**Package:** `typing`
**Available Since:** `v3.13.0`
**Status:** Stable
**PEP:** [696](https://peps.python.org/pep-0696/)

**Signature:**
```python
from typing import TypeVar, Generic, ParamSpec

# TypeVar with default
T = TypeVar("T", default=int)

# ParamSpec with default
P = ParamSpec("P", default=...)

# In type parameter syntax (PEP 695)
class Box[T=int]:
    value: T
```

**Usage Example:**
```python
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T", default=int)

@dataclass
class Box(Generic[T]):
    value: T | None = None

# These are equivalent
box1 = Box()  # Box[int]
box2 = Box[int]()  # Box[int]

# This is different
box3 = Box(value="hello")  # Box[str]
```

**Context:**
- Purpose: Allows specifying default types for generic type parameters
- Benefits: Improves type inference and usability for optional type parameters
- Common patterns:
  - Simplifies commonly used generics like `Generator[YieldT, SendT=None, ReturnT=None]`
  - Makes generic libraries more ergonomic for non-typing users

#### TypeIs Type Narrowing [`STABLE`]

**Package:** `typing`
**Available Since:** `v3.13.0`
**Status:** Stable
**PEP:** [742](https://peps.python.org/pep-0742/)

**Signature:**
```python
from typing import TypeIs

def is_int_list(obj: object) -> TypeIs[list[int]]:
    return isinstance(obj, list) and all(isinstance(x, int) for x in obj)
```

**Usage Example:**
```python
from typing import TypeIs, Any

def is_str(val: Any) -> TypeIs[str]:
    return isinstance(val, str)

def process(val: list[Any] | str):
    if is_str(val):
        # Type checker knows val is str here
        print(val.upper())
    else:
        # Type checker knows val is list[Any] here
        print(len(val))
```

**Context:**
- Purpose: Provides more intuitive type narrowing behavior
- Alternatives: `TypeGuard` - TypeIs is often a more natural choice
- Use cases: Type-checking functions that validate input types

#### ReadOnly TypeDict Items [`STABLE`]

**Package:** `typing`
**Available Since:** `v3.13.0`
**Status:** Stable
**PEP:** [705](https://peps.python.org/pep-0705/)

**Signature:**
```python
from typing import TypedDict, ReadOnly

class User(TypedDict):
    id: ReadOnly[int]  # Read-only field
    name: str  # Regular field
```

**Usage Example:**
```python
from typing import TypedDict, ReadOnly

class Config(TypedDict):
    version: ReadOnly[str]  # Cannot be modified
    debug: bool  # Can be modified

def update_config(config: Config) -> None:
    # Type checker will flag this as an error
    config["version"] = "2.0"  # Error: Cannot modify read-only item

    # This is allowed
    config["debug"] = True
```

**Context:**
- Purpose: Marks specific items in a TypedDict as read-only
- Benefits: Provides more precise modeling of immutable fields in dictionary-like structures
- Limitations: Runtime enforcement is not provided - this is for static type checking only

### Standard Library

#### dbm.sqlite3 [`STABLE`]

**Package:** `dbm.sqlite3`
**Available Since:** `v3.13.0`
**Status:** Stable

**Signature:**
```python
import dbm.sqlite3

db = dbm.sqlite3.open(filename, flag='c', mode=0o666, buffer_size=0)
```

**Usage Example:**
```python
import dbm

# Now uses sqlite3 by default
with dbm.open('cache', 'c') as db:
    db['key'] = 'value'
    value = db['key']
```

**Context:**
- Purpose: Provides a modern, robust SQLite backend for the dbm interface
- Benefits: More reliable storage, better performance for many operations
- Impact: Now the default dbm backend when creating new files

#### copy.replace() [`STABLE`]

**Package:** `copy`
**Available Since:** `v3.13.0`
**Status:** Stable

**Signature:**
```python
def replace(obj, /, **changes):
    """Return a new copy of obj with specified attribute changes."""
```

**Usage Example:**
```python
import copy
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = copy.replace(p1, y=3)  # Point(x=1, y=3)
```

**Context:**
- Purpose: Creates modified copies of objects, especially useful for immutable objects
- Supported built-in types:
  - `collections.namedtuple()`
  - `dataclasses.dataclass`
  - `datetime.datetime`, `datetime.date`, `datetime.time`
  - `inspect.Signature`, `inspect.Parameter`
  - `types.SimpleNamespace`
  - code objects
- Custom support: Classes can implement the `__replace__()` method

#### base64.z85encode/z85decode [`STABLE`]

**Package:** `base64`
**Available Since:** `v3.13.0`
**Status:** Stable

**Signature:**
```python
def z85encode(b: bytes, /) -> bytes: ...
def z85decode(b: bytes, /) -> bytes: ...
```

**Usage Example:**
```python
import base64

data = b"Hello, world!"
encoded = base64.z85encode(data)
decoded = base64.z85decode(encoded)
assert data == decoded
```

**Context:**
- Purpose: Provides encoding/decoding for Z85 data format (ZeroMQ Base-85)
- Characteristics: Produces 5 ASCII characters for every 4 bytes of binary data
- Use case: More compact and readable than base64 for some applications

### Removed and Deprecated Features

#### PEP 594 Module Removals [`REMOVED`]

**Status:** Removed in 3.13.0
**PEP:** [594](https://peps.python.org/pep-0594/)

**Context:**
- Purpose: Remove obsolete or unmaintained modules from the standard library
- Removed modules:
  - `aifc`: Audio Interchange File Format support
  - `audioop`: Audio processing operations
  - `cgi`, `cgitb`: CGI support modules
  - `chunk`: Read IFF chunked data
  - `crypt`: Function to check Unix passwords
  - `imghdr`: Determine image types
  - `mailcap`: Mailcap file handling
  - `msilib`: Windows Installer creation
  - `nis`: Interface to Sun's NIS
  - `nntplib`: NNTP protocol client
  - `ossaudiodev`: Access to OSS audio devices
  - `pipes`: Unix shell pipeline templates
  - `sndhdr`: Determine sound file types
  - `spwd`: Access to the Unix shadow password database
  - `sunau`: Sun AU file format
  - `telnetlib`: Telnet client
  - `uu`: UUencode/UUdecode
  - `xdrlib`: XDR data encoding
  - `lib2to3`: 2to3 code translation tool

**Migration Difficulty:** Medium
- Use third-party alternatives where needed
- Many removed modules have better alternatives in PyPI packages

#### Other Removals [`REMOVED`]

**Status:** Removed in 3.13.0

**Context:**
- `tkinter.tix` module (deprecated since Python 3.6)
- `locale.resetlocale()` function
- `typing.io` and `typing.re` namespaces
- Chained `classmethod` descriptors

### Platform Support Changes

#### iOS Support [`EXPERIMENTAL`]

**Status:** Tier 3
**PEP:** [730](https://peps.python.org/pep-0730/)

**Context:**
- Support targets:
  - `arm64-apple-ios`: iPhone and iPad devices (2013+)
  - `arm64-apple-ios-simulator`: iOS simulator on Apple silicon
- `x86_64-apple-ios-simulator`: Best-effort support

#### Android Support [`EXPERIMENTAL`]

**Status:** Tier 3
**PEP:** [738](https://peps.python.org/pep-0738/)

**Context:**
- Support targets:
  - `aarch64-linux-android`: 64-bit ARM
  - `x86_64-linux-android`: 64-bit x86
- 32-bit targets have best-effort support:
  - `arm-linux-androideabi`
  - `i686-linux-android`

#### WASI Support [`STABLE`]

**Status:** Tier 2

**Context:**
- WebAssembly System Interface (`wasm32-wasi`) is now a Tier 2 supported platform
- `wasm32-emscripten` is no longer officially supported

## Security Enhancements

- `ssl.create_default_context()` now sets `ssl.VERIFY_X509_PARTIAL_CHAIN` and `ssl.VERIFY_X509_STRICT` as default flags
- A modified version of mimalloc is now included and enabled by default on supported platforms, improving memory allocation security

## Other Notable Changes

- Docstrings now have leading whitespace stripped, reducing memory use and .pyc file size
- Added `PythonFinalizationError` exception, raised when operations are blocked during interpreter shutdown
- macOS minimum supported version changed from 10.9 to 10.13 (High Sierra)
- Python release cadence updated: Python 3.13+ will have two years of full support followed by three years of security fixes

## Implementation Details

- Classes now have a `__static_attributes__` attribute containing attribute names assigned through `self.X`
- Classes now have a `__firstlineno__` attribute recording the first line number of the class definition
- Added support for Linux timer notification file descriptors in the `os` module
- The `random` module now has a command-line interface
