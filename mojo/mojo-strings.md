# Mojo String Library Documentation

## Table of Contents

- [String](#string)
- [StringSlice](#stringslice)
- [Codepoint](#codepoint)
- [InlineString](#inlinestring)
- [String Formatters](#string-formatters)
- [Unicode Support](#unicode-support)
- [UTF-8 Validation](#utf-8-validation)
- [Utility Functions](#utility-functions)

## String

A mutable string class with heap-allocated storage.

### Construction

```mojo
fn __init__(out self)  # Empty string
fn __init__[T: Stringable](out self, value: T)  # From Stringable type
fn __init__(out self, *, capacity: Int)  # With pre-allocated capacity
fn __init__(out self, *, owned buffer: List[UInt8, *_])  # From a buffer
fn __init__(out self, literal: StringLiteral)  # From string literal
```

### Properties

```mojo
ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE
DIGITS = "0123456789"
HEX_DIGITS = DIGITS + "abcdef" + "ABCDEF"
OCT_DIGITS = "01234567"
PUNCTUATION = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
PRINTABLE = DIGITS + ASCII_LETTERS + PUNCTUATION + " \t\n\r\v\f"
```

### Methods

#### Capacity and Length

```mojo
fn __len__(self) -> Int  # String length in bytes
fn byte_length(self) -> Int  # Length in bytes (excluding null terminator)
fn reserve(mut self, new_capacity: Int)  # Reserve capacity
```

#### String Manipulation

```mojo
fn __iadd__(mut self, other: StringSlice)  # Append
fn __add__(self, other: StringSlice) -> String  # Concatenate
fn __mul__(self, n: Int) -> String  # Repeat string n times
```

#### Search and Replace

```mojo
fn __contains__(self, substr: StringSlice) -> Bool  # Check if contains substring
fn find(self, substr: StringSlice, start: Int = 0) -> Int  # Find first occurrence
fn rfind(self, substr: StringSlice, start: Int = 0) -> Int  # Find last occurrence
fn count(self, substr: StringSlice) -> Int  # Count occurrences
fn replace(self, old: StringSlice, new: StringSlice) -> String  # Replace all occurrences
```

#### Case Transformation

```mojo
fn lower(self) -> String  # Convert to lowercase
fn upper(self) -> String  # Convert to uppercase
```

#### Whitespace Handling

```mojo
fn strip(self, chars: StringSlice) -> StringSlice[__origin_of(self)]  # Strip from both ends
fn strip(self) -> StringSlice[__origin_of(self)]  # Strip whitespace from both ends
fn lstrip(self, chars: StringSlice) -> StringSlice[__origin_of(self)]  # Strip from left
fn lstrip(self) -> StringSlice[__origin_of(self)]  # Strip whitespace from left
fn rstrip(self, chars: StringSlice) -> StringSlice[__origin_of(self)]  # Strip from right
fn rstrip(self) -> StringSlice[__origin_of(self)]  # Strip whitespace from right
```

#### Splicing and Joining

```mojo
fn split(self, sep: StringSlice, maxsplit: Int = -1) raises -> List[String]  # Split by separator
fn split(self, sep: NoneType = None, maxsplit: Int = -1) -> List[String]  # Split by whitespace
fn splitlines(self, keepends: Bool = False) -> List[String]  # Split by line boundaries
fn join[*Ts: Writable](self, *elems: *Ts) -> String  # Join elements with self as delimiter
```

#### Formatting

```mojo
fn format[*Ts: _CurlyEntryFormattable](self, *args: *Ts) raises -> String  # Format with args
```

#### Prefix/Suffix Handling

```mojo
fn startswith(self, prefix: StringSlice, start: Int = 0, end: Int = -1) -> Bool
fn endswith(self, suffix: StringSlice, start: Int = 0, end: Int = -1) -> Bool
fn removeprefix(self, prefix: StringSlice, /) -> String
fn removesuffix(self, suffix: StringSlice, /) -> String
```

#### Character Type Checking

```mojo
fn isdigit(self) -> Bool  # Check if all chars are digits
fn isspace(self) -> Bool  # Check if all chars are whitespace
fn isupper(self) -> Bool  # Check if all cased chars are uppercase
fn islower(self) -> Bool  # Check if all cased chars are lowercase
fn isprintable(self) -> Bool  # Check if all chars are printable
```

#### Text Justification

```mojo
fn rjust(self, width: Int, fillchar: StringLiteral = " ") -> String  # Right justify
fn ljust(self, width: Int, fillchar: StringLiteral = " ") -> String  # Left justify
fn center(self, width: Int, fillchar: StringLiteral = " ") -> String  # Center
```

#### Iterators

```mojo
fn codepoints(self) -> CodepointsIter[__origin_of(self)]  # Iterate over codepoints
fn codepoint_slices(self) -> CodepointSliceIter[__origin_of(self)]  # Iterate over codepoint slices
```

#### Conversion

```mojo
fn __int__(self) raises -> Int  # Parse as integer
fn __float__(self) raises -> Float64  # Parse as float
fn as_bytes(ref self) -> Span[Byte, __origin_of(self)]  # Get byte representation
fn as_string_slice(ref self) -> StringSlice[__origin_of(self)]  # Get as string slice
```

## StringSlice

A non-owning view to encoded string data. Guarantees the same ABI (size, alignment, field layout) as `llvm::StringRef`.

### Construction

```mojo
fn __init__(out self, lit: StringLiteral)  # From string literal
fn __init__(out self, *, owned unsafe_from_utf8: Span[Byte, origin])  # From UTF-8 bytes
fn __init__(out self, *, unsafe_from_utf8_ptr: UnsafePointer[Byte])  # From null-terminated UTF-8
fn from_utf8(from_utf8: Span[Byte, origin]) raises -> StringSlice[origin]  # With UTF-8 validation
```

### Methods

Many methods mirror the String class, including:
- Search and comparison (`find`, `rfind`, `startswith`, `endswith`, etc.)
- Case transformation (`lower`, `upper`)
- Character type checking (`isspace`, `isupper`, `islower`, etc.)
- Whitespace handling (`strip`, `lstrip`, `rstrip`)
- Splitting (`split`, `splitlines`)
- Formatting (`format`)

#### Unicode-Specific

```mojo
fn char_length(self) -> UInt  # Length in Unicode codepoints
fn is_codepoint_boundary(self, index: UInt) -> Bool  # Check if index is at codepoint boundary
fn codepoints(self) -> CodepointsIter[origin]  # Iterator over codepoints
fn codepoint_slices(self) -> CodepointSliceIter[origin]  # Iterator over codepoint slices
```

#### Immutability

```mojo
fn get_immutable(self) -> StringSlice[ImmutableOrigin.cast_from[origin].result]  # Get immutable version
```

## Codepoint

A Unicode codepoint (scalar value), typically a single user-recognizable character.

### Construction

```mojo
fn __init__(out self, *, unsafe_unchecked_codepoint: UInt32)  # Unchecked (must be valid)
fn __init__(out self, codepoint: UInt8)  # From single byte value
fn from_u32(codepoint: UInt32) -> Optional[Self]  # From 32-bit value with validation
fn ord(string: StringSlice) -> Codepoint  # Get codepoint of a single-character string
```

### Methods

```mojo
fn is_ascii(self) -> Bool  # Check if ASCII character
fn is_ascii_digit(self) -> Bool  # Check if digit [0-9]
fn is_ascii_upper(self) -> Bool  # Check if uppercase [A-Z]
fn is_ascii_lower(self) -> Bool  # Check if lowercase [a-z]
fn is_ascii_printable(self) -> Bool  # Check if printable
fn is_python_space(self) -> Bool  # Check if Python whitespace
fn is_posix_space(self) -> Bool  # Check if POSIX/C locale whitespace
fn to_u32(self) -> UInt32  # Get numeric value as 32-bit unsigned integer
fn utf8_byte_length(self) -> UInt  # Get number of UTF-8 bytes required to encode
```

### UTF-8 Conversion

```mojo
fn unsafe_write_utf8[optimize_ascii: Bool = True](self, ptr: UnsafePointer[Byte]) -> UInt
fn unsafe_decode_utf8_codepoint(_ptr: UnsafePointer[Byte]) -> (Codepoint, Int)
```

## InlineString

A string with small-string optimization to avoid heap allocations for short strings.

```mojo
alias SMALL_CAP: Int = 24  # Bytes that can be stored inline before heap allocation
```

### Construction

```mojo
fn __init__(out self)  # Empty string
fn __init__(out self, literal: StringLiteral)  # From string literal
fn __init__(out self, owned heap_string: String)  # Take ownership of existing heap string
```

### Methods

```mojo
fn __iadd__(mut self, str_slice: StringSlice)  # Append
fn __add__(self, other: StringSlice) -> Self  # Concatenate
fn unsafe_ptr(self) -> UnsafePointer[UInt8]  # Get pointer to underlying data
fn as_string_slice(ref self) -> StringSlice[__origin_of(self)]  # Get as string slice
fn as_bytes(ref self) -> Span[Byte, __origin_of(self)]  # Get byte representation
```

## String Formatters

String formatting uses a curly brace syntax similar to Python's string formatting.

### Format Specifications

Format strings use curly braces to indicate replacement fields:

```mojo
# Manual indexing:
"{0} {1} {0}".format("Mojo", 1.125)  # "Mojo 1.125 Mojo"

# Automatic indexing:
"{} {}".format(True, "hello world")  # "True hello world"
```

## Unicode Support

### Case Conversion

```mojo
fn to_uppercase(s: StringSlice) -> String  # Convert to uppercase
fn to_lowercase(s: StringSlice) -> String  # Convert to lowercase
fn is_uppercase(s: StringSlice) -> Bool  # Check if all cased chars are uppercase
fn is_lowercase(s: StringSlice) -> Bool  # Check if all cased chars are lowercase
```



## UTF-8 Validation

The library includes fast UTF-8 validation using SIMD instructions to ensure proper handling of Unicode text.

## Utility Functions

### Character Functions

```mojo
fn ord(s: StringSlice) -> Int  # Get integer codepoint of a single-character string
fn chr(c: Int) -> String  # Get character string from codepoint
```

### String Parsing

```mojo
fn atol(str_slice: StringSlice, base: Int = 10) raises -> Int  # Parse as integer with base
fn atof(str_slice: StringSlice) raises -> Float64  # Parse as floating point
```

### ASCII Functions

```mojo
fn ascii(value: StringSlice) -> String  # Get ASCII representation
```
