# pathlib

Provides filesystem path manipulation.

## Constants

```mojo
alias DIR_SEPARATOR = "\\" if os_is_windows() else "/"
```

## Functions

```mojo
fn cwd() raises -> Path  # Get current working directory
```

## Types

```mojo
@value
struct Path(Stringable, Boolable, Writable, CollectionElement, CollectionElementNew, PathLike, KeyElement):
    var path: String  # The underlying path string

    # Constructors
    fn __init__(out self) raises  # Current directory
    fn __init__(out self, path: StringSlice)
    fn __init__(out self, owned path: String)

    # Path operations
    fn copy(self) -> Self
    fn __truediv__(self, suffix: Self) -> Self  # Path joining with /
    fn __truediv__(self, suffix: StringSlice) -> Self
    fn __itruediv__(mut self, suffix: StringSlice)
    fn joinpath(self, *pathsegments: String) -> Path

    # String conversion
    fn __str__(self) -> String
    fn __repr__(self) -> String
    fn __fspath__(self) -> String  # For os.PathLike compatibility
    fn __bool__(self) -> Bool  # True if path is not empty

    # Comparison
    fn __eq__(self, other: Self) -> Bool
    fn __eq__(self, other: StringSlice) -> Bool
    fn __ne__(self, other: Self) -> Bool

    # Hashing
    fn __hash__(self) -> UInt

    # File system operations
    fn stat(self) raises -> stat_result  # Get file stats
    fn lstat(self) raises -> stat_result  # Get symlink stats
    fn exists(self) -> Bool  # Check if path exists
    fn expanduser(self) raises -> Path  # Expand ~ to home directory
    fn is_dir(self) -> Bool  # Check if path is a directory
    fn is_file(self) -> Bool  # Check if path is a file
    fn read_text(self) raises -> String  # Read file as text
    fn read_bytes(self) raises -> List[UInt8]  # Read file as bytes
    fn write_text[stringable: Stringable](self, value: stringable) raises  # Write text to file
    fn listdir(self) raises -> List[Path]  # List directory contents

    # Path information
    fn suffix(self) -> String  # Get file extension

    # Static methods
    @staticmethod
    fn home() raises -> Path  # Get user's home directory
```