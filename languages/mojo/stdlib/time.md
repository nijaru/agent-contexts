# time

Provides time-related utilities.

## Functions

```mojo
# Time measurement functions
fn perf_counter() -> Float64  # High-resolution time in seconds
fn perf_counter_ns() -> UInt  # High-resolution time in nanoseconds
fn monotonic() -> UInt  # Monotonic time in nanoseconds

# Time execution of a function
fn time_function[func: fn () raises capturing [_] -> None]() raises -> UInt
fn time_function[func: fn () capturing [_] -> None]() -> UInt

# Sleep function
fn sleep(sec: Float64)  # Sleep for floating point seconds
fn sleep(sec: UInt)     # Sleep for integer seconds
```