# os

Provides operating system interfaces, including environment variables, file operations, and atomic operations.

## Constants and Types

```mojo
# File-related constants
alias sep = "\\" if os_is_windows() else "/"
alias SEEK_SET: UInt8 = 0
alias SEEK_CUR: UInt8 = 1
alias SEEK_END: UInt8 = 2

# File descriptors
alias stdout: FileDescriptor = 1
alias stderr: FileDescriptor = 2

# Stat result
struct stat_result:
    var st_mode: Int
    var st_ino: Int
    var st_dev: Int
    var st_nlink: Int
    var st_uid: Int
    var st_gid: Int
    var st_size: Int
    var st_atimespec: _CTimeSpec
    var st_mtimespec: _CTimeSpec
    var st_ctimespec: _CTimeSpec
    var st_birthtimespec: _CTimeSpec
    var st_blocks: Int
    var st_blksize: Int
    var st_rdev: Int
    var st_flags: Int

# Atomic operations
struct Atomic[type: DType, *, scope: StringLiteral = ""]:
    var value: Scalar[type]
    fn load(self) -> Scalar[type]
    fn fetch_add(self, rhs: Scalar[type]) -> Scalar[type]
    fn fetch_sub(self, rhs: Scalar[type]) -> Scalar[type]
    fn compare_exchange_weak(self, mut expected: Scalar[type], desired: Scalar[type]) -> Bool
    fn max(self, rhs: Scalar[type])
    fn min(self, rhs: Scalar[type])
```

## Traits

```mojo
trait PathLike:
    fn __fspath__(self) -> String
```

## Functions

```mojo
# Environment functions
fn getenv(name: String, default: String = "") -> String
fn setenv(name: String, value: String, overwrite: Bool = True) -> Bool
fn unsetenv(name: String) -> Bool

# File system operations
fn stat[PathLike: os.PathLike](path: PathLike) raises -> stat_result
fn lstat[PathLike: os.PathLike](path: PathLike) raises -> stat_result
fn listdir[PathLike: os.PathLike](path: PathLike) raises -> List[String]
fn remove[PathLike: os.PathLike](path: PathLike) raises
fn unlink[PathLike: os.PathLike](path: PathLike) raises
fn mkdir[PathLike: os.PathLike](path: PathLike, mode: Int = 0o777) raises
fn makedirs[PathLike: os.PathLike](path: PathLike, mode: Int = 0o777, exist_ok: Bool = False) -> None
fn rmdir[PathLike: os.PathLike](path: PathLike) raises
fn removedirs[PathLike: os.PathLike](path: PathLike) -> None

# System information
fn getuid() -> Int
fn abort[result: AnyType = NoneType._mlir_type]() -> result
fn abort[result: AnyType = NoneType._mlir_type, *Ts: Writable](*messages: *Ts) -> result
```