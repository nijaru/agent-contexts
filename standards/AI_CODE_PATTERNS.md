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

## COMMENT PATTERNS

### ❌ WRONG vs ✅ CORRECT Comments

**❌ WRONG: Obvious comments**
```javascript
// Increment i by 1
i++;

// Create a new array
const items = [];

// Return the user object
return user;
```

**✅ CORRECT: Context-providing comments**
```javascript
// Handle edge case where API returns null user on first login attempt
if (!user && isFirstLogin) {
  return await retryUserFetch();
}

// Cache result for 5 minutes to reduce API calls during peak hours
const cached = await cache.set(key, result, 300);

// Business rule: Premium users get unlimited retries
const maxRetries = user.isPremium ? Infinity : 3;
```

**❌ WRONG: Outdated/wrong comments**
```javascript
// Returns user email (actually returns full user object)
function getUserData(id) {
  return database.users.find(id);
}
```

**✅ CORRECT: Accurate and maintained comments**
```javascript
// Returns complete user profile including preferences and settings
function getUserData(id) {
  return database.users.find(id);
}
```

### Dev Notes Decision Tree
```
IF temporary_solution OR known_issue:
    → TODO: [specific action needed]
IF performance_concern OR optimization_opportunity:
    → PERF: [what to optimize and why]
IF potential_bug OR edge_case_not_handled:
    → BUG: [describe issue and impact]
IF security_concern OR requires_review:
    → SECURITY: [describe risk]
IF complex_business_logic OR non_obvious_requirement:
    → NOTE: [explain context]
IF quick_fix OR needs_proper_solution:
    → HACK: [why this approach, what proper fix would be]
```

### Dev Note Patterns
```javascript
// TODO: Add input validation after user requirements finalized
// TODO: @alice - needs review of algorithm efficiency
// TODO: Replace with proper error handling when new API available

// PERF: Consider caching here - called 1000+ times per request
// PERF: O(n²) complexity, optimize with Set lookup for n > 100

// BUG: Race condition possible if multiple users modify same resource
// BUG: Memory leak when processing large files, investigate cleanup

// SECURITY: Validate user permissions before allowing admin actions
// SECURITY: Sanitize input to prevent XSS attacks

// NOTE: Business rule - invoices locked after 24 hours per accounting
// NOTE: Keep in sync with mobile app constants (version 2.1.4)

// HACK: Temporary workaround for Safari CSS bug, remove when fixed
// HACK: API doesn't support batch updates, doing individual calls
```

### Comment Maintenance Patterns
```
ON code_change:
  IF comment_mentions_changed_behavior:
    → UPDATE_COMMENT_OR_DELETE
  IF function_signature_changed:
    → UPDATE_PARAMETER_DESCRIPTIONS

ON refactoring:
  IF extracted_function:
    → MOVE_RELEVANT_COMMENTS_TO_NEW_LOCATION
  IF merged_functions:
    → CONSOLIDATE_AND_UPDATE_COMMENTS
```

## CODE REMOVAL PATTERNS

### Clean Deletion Principle
Version control tracks history - code should be production-ready without removal artifacts.

### ❌ WRONG vs ✅ CORRECT Code Removal

**❌ WRONG: Leaving placeholder comments**
```javascript
// gc section removed
// const gcConfig = { ... }
// function runGC() { ... }

// authentication removed
// import { auth } from './auth';
// auth.initialize();
```

**✅ CORRECT: Clean deletion**
```javascript
// Just delete the code completely
// Version control preserves the history
```

**❌ WRONG: Commenting out code blocks**
```python
def process_data(data):
    validate(data)
    # transform(data)  # removed old transformation
    # clean(data)      # deprecated cleaning step
    return data
```

**✅ CORRECT: Remove cleanly or document why**
```python
def process_data(data):
    validate(data)
    # Note: Direct transformation removed in v2.0 - data now pre-processed by upstream service
    return data
```

### Code Removal Decision Tree
```
IF removing_code_section:
    IF temporary_removal_for_testing:
        → Use feature flag or environment variable
    ELIF permanent_removal:
        → Delete completely, rely on version control
    ELIF keeping_for_reference:
        → Move to documentation or archive file
    
IF modifying_configuration:
    IF removing_config_section:
        → Delete section entirely
    ELIF disabling_feature:
        → Set to false/disabled, don't comment out
```

### Anti-Pattern Examples
```
❌ # Section removed
❌ // Deleted authentication logic  
❌ /* Removed old implementation */
❌ // BEGIN REMOVED CODE ... // END REMOVED CODE
❌ # --- DELETED ---
❌ // gc configuration removed here

✅ [Clean file with no removal artifacts]
✅ [Use git log/blame to see what was removed]
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
rg "TODO|FIXME|HACK|BUG|PERF|SECURITY" .  # Find all dev notes
rg "console\.log|print\(" .                # Find debug statements
rg "/\*.*\*/" . -U                        # Find block comments to review
```

### Comment Quality Checks
```bash
# Find comments that might be obvious
rg "// (Get|Set|Return|Create|Delete) " . 

# Find potentially outdated comments
rg "// (Old|Previous|Legacy|Temp)" .

# Find empty or placeholder comments  
rg "// (TODO|FIXME|HACK)$" .
```