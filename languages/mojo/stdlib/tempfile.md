# tempfile

Provides temporary file and directory handling.

## Functions

```mojo
# Get temporary directory
fn gettempdir() -> Optional[String]

# Create a temporary directory
fn mkdtemp(suffix: String = "", prefix: String = "tmp", dir: Optional[String] = None) raises -> String
```

## Types

```mojo
struct TemporaryDirectory:
    var name: String  # The path to the temporary directory

    # Constructor
    fn __init__(mut self, suffix: String = "", prefix: String = "tmp",
                dir: Optional[String] = None, ignore_cleanup_errors: Bool = False) raises

    # Context manager methods
    fn __enter__(self) -> String
    fn __exit__(self) raises
    fn __exit__(self, err: Error) -> Bool

struct NamedTemporaryFile:
    var name: String  # The path to the temporary file

    # Constructor
    fn __init__(mut self, mode: String = "w", name: Optional[String] = None,
                suffix: String = "", prefix: String = "tmp",
                dir: Optional[String] = None, delete: Bool = True) raises

    # File operations
    fn close(mut self) raises
    fn read(self, size: Int64 = -1) raises -> String
    fn read_bytes(self, size: Int64 = -1) raises -> List[UInt8]
    fn seek(self, offset: UInt64, whence: UInt8 = os.SEEK_SET) raises -> UInt64
    fn write[*Ts: Writable](mut self, *args: *Ts)
    fn write_bytes(mut self, bytes: Span[Byte, _])

    # Context manager
    fn __enter__(owned self) -> Self
```