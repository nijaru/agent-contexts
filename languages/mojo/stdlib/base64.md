# base64

Provides functions for Base64 and Base16 encoding and decoding.

## Functions

```mojo
fn b64encode(input_bytes: Span[Byte, _]) -> String
fn b64encode(input_string: StringSlice) -> String
fn b64decode[validate: Bool = False](str: StringSlice) raises -> String
fn b16encode(str: StringSlice) -> String
fn b16decode(str: StringSlice) -> String
```