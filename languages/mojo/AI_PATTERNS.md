# Mojo AI Agent Patterns

## PATTERN: Type Conversions
TRIGGER: Converting Python types to Mojo
ACTION: Use capitalized Mojo equivalents
```mojo
❌ int(value)    → ERROR: use of unknown declaration 'int'
✅ Int(value)    → Mojo integer type
❌ str(value)    → ERROR: use of unknown declaration 'str' 
✅ String(value) → Mojo string type
❌ float(value)  → ERROR: use of unknown declaration 'float'
✅ Float32(value) → Explicit precision required
```

## PATTERN: Memory Management Decision Tree
```
IF high_performance_required:
    IF memory_constrained:
        → Use quantization patterns (advanced/MOJO_BEST_PRACTICES.md)
    ELSE:
        → Use move semantics (owned parameters, ^ transfer)
ELSE:
    → Use standard def functions with Python interop
```

## PATTERN: Function Type Selection
```
TRIGGER: Creating new function
DECISION:
  Python interop needed → def function_name():
  Performance critical  → fn function_name():
  Memory management     → fn with owned/mut parameters
```

## PATTERN: Import Resolution
```mojo
❌ from python import numpy     → Slow FFI overhead
✅ from tensor import Tensor    → Native Mojo types
❌ import math                  → Python math module  
✅ from math import *           → Mojo math functions
```

## ANTI-PATTERN: Memory Waste
```mojo
❌ NEVER: Store same data twice
struct BadBuffer:
    var original: UnsafePointer[Float32]
    var quantized: UnsafePointer[UInt8]  # BOTH stored = waste

✅ ALWAYS: Single storage with flag  
struct GoodBuffer:
    var data: UnsafePointer[Float32]     # Only one
    var is_quantized: Bool               # Flag for type
```

## ERROR → SOLUTION MAPPINGS
| Error | Root Cause | Fix |
|-------|------------|-----|
| `use of unknown declaration 'int'` | Python syntax | Use `Int()` |
| `use of unknown declaration 'str'` | Python syntax | Use `String()` |
| `cannot implicitly convert` | Type mismatch | Explicit conversion |
| `use of uninitialized value` | No initialization | Assign value at declaration |

## COMMAND SEQUENCES

### SEQUENCE: Convert Python-style code  
```bash
rg "int\(" --type mojo -l | xargs sed -i 's/int(/Int(/g'
rg "str\(" --type mojo -l | xargs sed -i 's/str(/String(/g'  
rg "float\(" --type mojo -l | xargs sed -i 's/float(/Float32(/g'
```

### SEQUENCE: Find performance bottlenecks
```bash
rg "def " --type mojo           # Find Python-style functions
rg "import.*python" --type mojo # Find FFI usage  
rg "\.append\(" --type mojo     # Find list operations
```