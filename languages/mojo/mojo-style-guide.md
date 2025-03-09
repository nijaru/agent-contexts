# Mojo Coding Style Guide

This document outlines the coding style conventions observed in the Mojo standard library, particularly in the built-ins module.

## File Organization

### File Structure

1. **Header and License**
   - Each file begins with a license header (Apache License v2.0 with LLVM Exceptions)
   - Module docstring follows immediately after the license

2. **Import Section**
   - Grouped by source (stdlib modules first, then local imports)
   - Separated by blank lines between different modules
   - Uses relative imports within the same package

3. **Main Content**
   - Structs, traits, and functions defined in logical groupings
   - Separated by comment dividers: `# ===---...---===`

### Naming Conventions

1. **Types and Traits**
   - PascalCase: `StringLiteral`, `Comparable`, `CollectionElement`
   - Type parameters use PascalCase: `T`, `Element`, `Writer`

2. **Functions and Methods**
   - snake_case: `write_to`, `get_string`, `byte_length`
   - Private/internal functions prefixed with underscore: `_format_int`, `_try_write_int`

3. **Variables**
   - snake_case: `value`, `byte_length`, `elements`
   - Private/internal variables may be prefixed with underscore: `_value`, `_handle`

4. **Constants and Aliases**
   - Constants use UPPER_SNAKE_CASE: `MAX`, `MIN`
   - Type aliases use snake_case: `insertion_sort_threshold`

## Docstrings and Comments

1. **Module Docstrings**
   - Begin with a brief summary of the module's purpose
   - May include usage examples and notes
   - Mention if a module provides built-ins that don't need importing

2. **Type/Function Docstrings**
   - Begin with a one-line summary
   - Followed by more detailed explanation if needed
   - Document parameters, return values, and exceptions
   - Include examples for complex or non-obvious usage
   - Use syntax highlighting in examples (```mojo)

3. **Parameters Documentation**
   - Document both type parameters and value parameters
   - Type parameters in "Parameters:" section
   - Value parameters in "Args:" section

4. **Returns and Raises Documentation**
   - Document return values in "Returns:" section
   - Document exceptions in "Raises:" section

5. **Section Headers**
   - Use consistent comment dividers for sections: `# ===...===`
   - Use smaller dividers for subsections: `# ---...---`

## Code Formatting

1. **Indentation and Line Length**
   - 4 spaces for indentation (no tabs)
   - Line length appears to be around 80-90 characters
   - Long lines are wrapped with 4-space continuation indents

2. **Spacing**
   - Space after commas: `fn example(a, b, c)`
   - Space around operators: `a + b`, `x = y`
   - No space between function name and opening parenthesis: `function_name(args)`
   - Space before colon in type annotations: `var x: Int`

3. **Trailing Commas**
   - Used in multi-line parameter lists and data structures
   - Helps with cleaner diffs when adding new items

4. **Blank Lines**
   - One blank line between functions, methods, and logical sections
   - Two blank lines between major sections (traits, structs, etc.)
   - No blank line after function/method opening line

5. **Brackets and Braces**
   - Opening brace on same line as statement: `fn example():`
   - Indented blocks for function/method bodies

## Function and Method Conventions

1. **Parameter Order**
   - Self parameter first for methods
   - Required parameters before optional parameters
   - Variadic parameters last
   - Type parameters come before value parameters in template syntax: `fn example[T: Trait](value: T)`

2. **Default Parameters**
   - Default values for optional parameters: `fn example(value: Int = 0)`
   - Named parameters shown in examples: `function(named_param=value)`

3. **Return Types**
   - Always explicitly specified: `fn example() -> ReturnType`
   - Return type annotations include `raises` if function can raise: `fn example() raises -> ReturnType`

4. **Method Annotations**
   - `@always_inline`, `@no_inline`, etc. for optimization hints
   - `@deprecated` with message for deprecated functionality
   - `@implicit` for implicit constructors
   - `@doc_private` for internal APIs

## Error Handling

1. **Exceptions**
   - Functions that can raise exceptions are marked with `raises`
   - Error messages are descriptive and include context
   - Try/except blocks handle exceptions appropriately

2. **Assertions**
   - `debug_assert` used for runtime checks
   - `constrained` used for compile-time checks

## Type System

1. **Trait Definitions**
   - Defined with clear documentation of expected behavior
   - Required methods clearly marked
   - Trait inheritance clearly indicated: `trait Child(Parent)`

2. **Generic Types**
   - Type constraints expressed through traits
   - Consistent use of `[T: Trait]` syntax for constraints
   - Generic type parameters documented in "Parameters:" section

3. **Type Aliases**
   - Used to create meaningful names for complex types
   - Documented with clear purpose and usage

## Special Patterns

1. **Origin System**
   - Carefully tracks mutability and lifetime of objects
   - Functions use appropriate origin types for references

2. **Operator Overloading**
   - Consistent implementation of dunder methods: `__add__`, `__eq__`, etc.
   - Includes both regular and in-place versions: `__add__` and `__iadd__`
   - Includes right-hand versions where appropriate: `__radd__`

3. **Parameter Forwarding**
   - Variadic parameters used for flexible APIs: `*args`
   - Variadic type parameters for generic functions: `*Ts: Trait`

4. **Cross-Cutting Concerns**
   - Careful handling of memory ownership with `owned` parameter modifiers
   - Consistent use of `mut` for mutable parameters
