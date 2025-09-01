# AI Agent Code Patterns

## NAMING DECISION TREES

### Variable Naming
```
IF local_scope AND short_lived → single_letter (i, n, err)
IF shared_across_functions → descriptive (activeSessionCount)
IF boolean → question_form (isEnabled, hasData, canRetry)
IF number_with_unit → include_unit (timeoutMs, bufferKB)
IF constant → UPPER_SNAKE (MAX_RETRIES, DEFAULT_PORT)
IF collection → plural (users, items, connections)
```

### Function Naming
```  
IF side_effects → action_verb (updateDatabase, saveUser)
IF query_only → get/find/check (getUser, findById, checkStatus)
IF returns_boolean → is/has/can (isValid, hasPermission, canAccess)
IF async → add_async_suffix (fetchDataAsync, uploadAsync)
```

## ANTI-PATTERNS → CORRECT PATTERNS

### Variable Names
```
❌ data, info, manager, helper    → Too generic
✅ userProfiles, configSettings, authValidator, stringFormatter

❌ getUserInfo()                  → Vague "info"  
✅ getUserProfile(), getUserPreferences()

❌ timeout                        → No units
✅ timeoutMs, timeoutSeconds
```

### Function Structure
```
❌ function doStuff(data) {       → Generic names
     // lots of code
   }
✅ function processPayment(request) {
     validateRequest(request);
     chargeCard(request.payment);
     updateDatabase(request.orderId);
   }
```

## PATTERN RECOGNITION

### Code Smells → Fixes
| Smell | Pattern | Fix |
|-------|---------|-----|
| Functions > 50 lines | `function name() { ...50+ lines }` | Extract helper functions |
| Nested ifs > 3 deep | `if { if { if { if` | Early returns/guard clauses |
| Magic numbers | `sleep(300)` | Named constants `RETRY_DELAY_MS = 300` |
| Generic names | `data`, `info`, `stuff` | Domain-specific names |

### File Organization Decision
```
IF new_functionality AND < 100_lines → add_to_existing_file
IF new_functionality AND > 100_lines → create_new_file  
IF refactoring_existing → edit_in_place
IF completely_different_domain → new_file_new_directory
```

## COMMAND PATTERNS

### Before Writing Code
```bash
rg "class.*${FEATURE_NAME}" .     # Check existing patterns
rg "function.*${VERB}" .          # Check naming conventions  
rg "interface.*${DOMAIN}" .       # Check existing interfaces
```

### After Writing Code  
```bash
rg "TODO|FIXME|HACK" .           # Find temporary code
rg "console\.log|print\(" .       # Find debug statements
rg "var |let " . | wc -l         # Count variable declarations
```

### Performance Checks
```bash
rg "for.*for.*for" .             # Find nested loops O(n³)
rg "\.map\(.*\.map\(" .          # Find nested maps
rg "JSON\.parse\(" .             # Find JSON operations
rg "fs\.readFileSync" .          # Find blocking I/O
```