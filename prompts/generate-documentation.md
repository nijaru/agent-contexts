# Technical Documentation Generator for LLM Coding Assistants

This template creates structured, LLM-optimized documentation based on technical content for coding assistants. It works for both comprehensive documentation and version-specific release notes.

## Information Gathering Process

1. **Analyze the Primary Source**
   - Thoroughly read and analyze all content at the provided URL
   - Identify key technical components, APIs, patterns, concepts, and changes
   - Note version information, release dates, and compatibility requirements

2. **Follow All Referenced Links**
   - Fetch all referenced links to detailed API documentation to extract complete signatures and type definitions
   - For new features/components, locate the canonical documentation via links
   - When primary documentation lacks technical details, find and analyze the complete specifications
   - Trace links to implementation details, especially for non-obvious behavior or edge cases
   - Examine referenced issues, discussions, or examples to understand design decisions
   - Continue until you have complete technical details for each significant component or change

3. **Collect Comprehensive Technical Details**
   - Gather complete function/method signatures with all parameters and return types
   - Document class/type definitions with properties and methods
   - Identify required imports, dependencies, or prerequisites
   - Extract representative code examples showing proper usage
   - Note compatibility constraints, platform requirements, or version limitations
   - Research backward compatibility information and migration paths
   - Identify relationships with other components and features
   - Note any performance characteristics or benchmarks
   - Understand idiomatic usage patterns in the ecosystem

## Handling Incomplete Information

When source documentation lacks complete details:
1. Clearly mark information gaps with `[INCOMPLETE]` tags
2. Propose reasonable defaults based on ecosystem conventions
3. Document assumptions made when filling gaps
4. Prioritize accuracy over completeness - do not fabricate signatures or behavior
5. Indicate confidence level in derived information (High/Medium/Low)
6. For critical components with incomplete documentation, examine actual implementation code if available

Example:
```
**Parameters:**
- `options`: ConfigOptions - Configuration object [INCOMPLETE: full type definition not provided]
  - `timeout`: number - Request timeout in ms (default: 5000) [ASSUMED]
  - `retries`: number - Number of retry attempts [CONFIDENCE: Medium, based on usage examples]
```

## Documentation Structure

Create a token-efficient document with this structure:

### Metadata Section
```
TITLE: [Technology/Component Name]
VERSION: [version number/date]
RELEASED: [YYYY-MM-DD] (if applicable for release notes)
COMPATIBILITY: [runtime requirements, dependencies, breaking changes]
DOCUMENTATION_SOURCE: [primary URL referenced]
MODEL: [Claude-3.7-Sonnet-Thinking]
```

### Conceptual Overview
Provide 3-5 bullet points summarizing:
- Key concepts or programming patterns introduced
- Major capabilities, features, or changes
- Significant changes from previous versions (if applicable)
- Intended use cases or problems solved
- Performance impact (if significant)

### Technical Reference

For each significant component or change, use this consistent structure:

#### [Component/Feature Name] [`STABLE`|`EXPERIMENTAL`|`PREVIEW`|`DEPRECATED`|`REMOVED`]

**Package:** `package/namespace/path`
**Available Since:** `v1.2.3`
**Status:** Stable/Experimental/Deprecated/Removed
**Breaking:** Yes/No (if applicable for release notes)

**Signature:**
```[language]
// Complete technical signature with all parameters and return types
function componentName(param: ParamType): ReturnType;

// For types/classes, include complete definition
interface ComponentType {
    property: PropertyType;
    method(param: MethodParamType): MethodReturnType;
}
```

**Dependencies/Imports:**
```[language]
// Required imports, libraries, or prerequisites
import { dependency } from 'package';
require('module');
// Or equivalent for the relevant technology
```

**Usage Example:**
```[language]
// Minimal but complete example showing correct usage
// Must be syntactically valid and demonstrate the component
// Include only setup that's essential to understanding

// Example:
const result = componentName('input');
result.property.method();
```

**Context:**
- Purpose: What problem does this solve?
- Patterns: Common usage patterns or idioms
- Alternatives: Related approaches or previous methods
- Limitations: Edge cases, performance considerations, constraints
- Related: Related components or features that work together with this one
- Behavior: Thread-safety, blocking/non-blocking, deterministic/non-deterministic
- Performance: Key metrics and characteristics (e.g., "5-10% faster for large collections")

**Edge Cases and Anti-patterns:**
- Common Mistakes: Frequently encountered errors when using the component
- Anti-patterns: Discouraged usage patterns that lead to problems
- Edge Cases: Behavior in unusual or extreme situations
- Gotchas: Surprising or non-obvious behavior that differs from expectations

```[language]
// ANTI-PATTERN (explains the problem):
component.method().then(() => {
  // Problem: this creates a race condition
});

// CORRECT:
await component.method();
// Or safer alternative approach
```

**Security Considerations:** (when applicable)
- Authentication/authorization requirements
- Input validation best practices
- Potential security risks of misuse
- Secure configuration guidance

**Migration:** (if applicable)
```[language]
// BEFORE:
oldFunction(param);

// AFTER:
newFunction(param);
```
**Migration Difficulty:** Simple/Medium/Complex (if applicable)

### Logical Grouping

Choose the appropriate grouping based on documentation purpose:

#### For General Documentation:
- `## Core Features:` Primary capabilities and central components
- `## APIs:` Public interfaces and functions
- `## Data Types:` Type definitions, interfaces, and structures
- `## Utilities:` Helper functions and convenience methods
- `## Configuration:` Setup and configuration options
- `## Advanced Usage:` Complex patterns and advanced techniques
- `## Breaking Changes:` All breaking changes (also mentioned in their respective sections)
- `## Platform-Specific:` Environment or platform-dependent features

#### For Release Notes:
- `## Core Language:` Syntax, semantics, and built-in features
- `## Standard Library:` Package and API changes
- `## Tooling:` CLI tools, compilers, build system
- `## Runtime:` Performance, memory, concurrency
- `## Platform:` OS-specific, hardware support
- `## Breaking Changes:` All breaking changes (also mentioned in their respective sections)

## Documentation Guidelines

1. **Code Examples:**
   - Must be syntactically correct and functional
   - Include necessary imports and setup in the example or dependencies section
   - Demonstrate only the specific component, not ancillary functionality
   - Show typical usage patterns that an LLM should emulate
   - For complex features, include a basic and advanced example when appropriate
   - Balance completeness with conciseness:
     * Include just enough context to show proper usage
     * Consider what information would be necessary to write new code using this component
     * Eliminate boilerplate that doesn't illustrate the component's unique aspects
     * Show error handling for critical operations
     * For security-related features, show secure usage patterns

2. **Prioritize Information:**
   - Parameter types, order, and constraints
   - Return value structures and error handling patterns
   - Thread-safety and concurrency considerations
   - Interaction patterns with other components
   - Version-specific behavior differences
   - Security considerations or best practices
   - Migration paths and backward compatibility information
   - Performance characteristics for critical operations

3. **Visual Structure Guidelines:**
   - Use consistent heading hierarchy (# for main sections, ## for components, ### for sub-components)
   - Use tables for parameter descriptions and option enumerations
   - Use blockquotes (>) for important notes, warnings, or tips
   - Use horizontal rules (---) to separate major sections
   - Use inline code formatting for technical terms and identifiers
   - Ensure proper nesting of list items to show relationships
   - Use bold for first mention of key concepts
   - Use consistent formatting for similar components
   - Mark breaking changes clearly with `BREAKING`
   - Mark experimental features with `EXPERIMENTAL`
   - Use indentation to show relationships between components
   - Group related functionality together

4. **Token Efficiency:**
   - Use concise language throughout
   - Include only the most relevant information for code generation
   - Avoid redundancy across examples and descriptions
   - Include just enough context for proper understanding
   - Prefer complete information over brevity for critical details

5. **Documentation Length Guidelines:**
   - **Comprehensive API documentation:**
     - Core components: 200-500 tokens per component
     - Supporting utilities: 100-300 tokens per utility
     - Balance completeness with conciseness

   - **Release notes:**
     - Major features: 150-300 tokens per feature
     - Minor changes: 50-150 tokens per change
     - Breaking changes: 200-400 tokens with migration examples

   Prioritize complete technical details (signatures, types, constraints) over verbose explanations.

6. **Status Indicators:**
   - `STABLE`: API unlikely to change, ready for production use
   - `EXPERIMENTAL`: May change in future versions, use with caution
   - `PREVIEW`: Available for testing but not yet officially supported
   - `DEPRECATED`: Will be removed in a future version, avoid for new code
   - `REMOVED`: No longer available in current version

7. **Performance Annotations:**
   - Include specific metrics when available (e.g., "50% faster than previous approach")
   - Note complexity characteristics (e.g., "O(n) for n elements")
   - Highlight memory usage patterns (e.g., "Lazy allocation, minimal memory footprint")
   - Indicate scaling considerations (e.g., "Scales linearly to hundreds of thousands of entries")

8. **Cross-Feature References:**
   - Briefly note related components that are commonly used together
   - Mention complementary features that enhance functionality
   - Highlight replacements for deprecated features

9. **Security and Compliance Documentation:**
   - Document authentication/authorization requirements
   - Include input validation best practices
   - Highlight potential security risks of misuse
   - Note compliance considerations (GDPR, HIPAA, etc.)
   - Document secure configuration defaults
   - Include security-focused code examples showing proper validation, escaping, etc.
   - Mark components requiring special security review with `[SECURITY-SENSITIVE]`

10. **Links to Further Documentation:**
    - Include links to official or authoritative documentation for each major component
    - Provide links to more detailed API references when abbreviated information is presented
    - Include links to tutorials, guides, and working examples when available
    - Link to relevant specifications, RFCs, or standards documents that inform the implementation
    - Add links to GitHub repositories, issue trackers, or discussion forums for community support
    - Include version-specific documentation links when behavior differs across versions
    - Format links consistently using markdown: `[Link text](URL)`
    - Include link context to explain what information can be found at the destination
    - Group related links under clear headings
    - Include permanent links to documentation whenever possible (versioned URLs, archived pages)
    - Add relevant community resources or third-party documentation when official sources are limited

    Example:
    ```markdown
    **Further Documentation:**
    - [Complete API Reference](https://example.com/api/v2/fetchData) - Detailed parameter options and advanced usage
    - [Performance Optimization Guide](https://example.com/guides/performance) - Techniques for improving fetch performance
    - [Error Handling Best Practices](https://example.com/guides/errors) - Comprehensive error handling strategies
    - [GitHub Repository](https://github.com/example/data-client) - Source code and issue tracking
    - [Specification](https://example.com/specs/v2.1) - Complete technical specification for v2.1
    ```

## Domain-Specific Adaptations

Adjust documentation focus based on technology domain:

### Frontend Frameworks
- Emphasize component composition patterns
- Document DOM interactions and event handling
- Include accessibility considerations (ARIA roles, keyboard navigation)
- Document styling approaches and theming
- Add mobile/responsive behavior information
- Include performance impacts on page loading and rendering

### Backend/API Services
- Emphasize request/response formats
- Document authentication and authorization requirements
- Include rate limiting and caching behavior
- Document transaction and consistency guarantees
- Note statelessness/statefulness of endpoints
- Include error handling patterns and status codes

### Data Processing Systems
- Document performance characteristics with varying data volumes
- Emphasize memory usage patterns
- Include scaling considerations and parallelism
- Document data consistency guarantees
- Note checkpoint and recovery mechanisms
- Include failure handling strategies

### Libraries/SDKs
- Focus on installation and integration
- Document versioning and compatibility
- Include platform-specific considerations
- Emphasize initialization and configuration
- Document resource management (cleanup, disposal)
- Note thread-safety characteristics

### Databases and Storage
- Document schema definitions and migrations
- Include query patterns and optimizations
- Note transaction isolation levels
- Document backup and recovery procedures
- Include replication and consistency guarantees

### Programming Languages
- Document core syntax and semantics comprehensively
- Clearly explain memory management models
- Include compilation, interpretation, and execution details
- Document standard library components and APIs
- Provide migration guidance between language versions
- Explain interoperability with other languages
- Document performance characteristics and optimization techniques
- Include thread and concurrency models
- Use consistent format for language features:
  ```
  ### Feature Name [`STABLE`|`EXPERIMENTAL`|`DEPRECATED`]
  
  **Package:** `package_name`
  **Available Since:** `v1.2.3`
  **Status:** Stable/Experimental/Deprecated
  
  **Signature:**
  ```language
  // Exact technical signature with parameter types
  ```
  
  **Usage Example:**
  ```language
  // Complete, runnable example showing proper usage
  ```
  
  **Context:** Purpose, patterns, alternatives, limitations
  
  **Edge Cases and Anti-patterns:**
  ```language
  // ANTI-PATTERN:
  // Bad code example
  
  // CORRECT:
  // Good code example
  ```
  ```
- For changelogs, clearly mark changes as:
  - [`NEW`] - New features
  - [`CHANGED`] - Modified behavior
  - [`DEPRECATED`] - Features being phased out
  - [`REMOVED`] - Features no longer available
  - [`IMPROVED`] - Enhanced existing functionality
  - [`BREAKING`] - Changes that require code modification

### Systems Programming Languages
- Emphasize memory safety features and practices
- Document explicit memory management patterns
- Include low-level hardware interactions
- Document compiler optimizations and inline assembly
- Explain FFI (Foreign Function Interface) capabilities
- Include representations of primitive types
- Document ABI (Application Binary Interface) compatibility
- Explain integration with system libraries
- Detail ownership semantics and memory lifecycle:
  - For languages with manual memory management, explain allocation/deallocation patterns
  - For languages with ownership models, document transfer and borrowing semantics
  - For languages with reference counting, explain reference cycle concerns
- Document hardware acceleration capabilities:
  - SIMD/vectorization features
  - GPU acceleration interfaces
  - Hardware-specific optimizations

## Testing Documentation Effectiveness

For each documented component, verify:

1. **Code Generation Test:** Can an LLM generate correct, working code using only this documentation?
2. **Comprehension Test:** Can an LLM accurately answer questions about usage patterns and constraints based on this documentation?
3. **Migration Test:** For changed components, can an LLM correctly migrate code from previous versions?
4. **Completeness Test:** Does the documentation cover all parameters, return types, and behaviors?
5. **Resource Access Test:** Can an LLM locate and access the right external resources through provided links?

Example validation prompts:
- "Using only this documentation, write code that [accomplishes task X]"
- "Based on this documentation, explain what happens if [edge case Y occurs]"
- "Update this code from version 1.x to use the new API described in the documentation"
- "Identify any information gaps in this documentation that would prevent correct implementation"
- "Using the links provided in the documentation, find more detailed information about [specific feature Z]"

## Final Verification

Before submitting the documentation:

1. Verify all technical signatures are complete with proper types
2. Ensure all code examples are syntactically valid and representative
3. Check that all breaking changes have migration examples
4. Confirm all dependencies and requirements are clearly specified
5. Validate that examples demonstrate idiomatic usage patterns
6. Ensure the documentation is organized logically by related functionality
7. For release notes, verify that all significant changes are documented with appropriate version information
8. Check that cross-references between related features are accurate
9. Verify that performance characteristics are included for performance-sensitive components
10. Ensure behavior annotations (thread-safety, blocking nature) are included where relevant
11. Verify security considerations are documented for sensitive components
12. Check that edge cases and anti-patterns are clearly identified
13. Test all external links to ensure they resolve to the correct resources
14. Ensure links are properly contextualized so their relevance is clear
15. Verify that links to versioned documentation point to the correct version

## Documentation Type Selection

When generating documentation:

1. **For comprehensive technical documentation:**
   - Focus on complete API coverage
   - Use component status categories (`STABLE`, `EXPERIMENTAL`, `DEPRECATED`)
   - Organize by functional categories (Core Features, APIs, Data Types, etc.)
   - Emphasize component relationships and architecture
   - Include links to comprehensive reference documentation
   - Always include this metadata header for consistency:
     ```
     TITLE: [Component Name]
     VERSION: [Version number where introduced or last significantly updated]
     COMPATIBILITY: [Runtime requirements, dependencies, breaking changes]
     DOCUMENTATION_SOURCE: [Primary URL referenced]
     MODEL: [Claude-3.7-Sonnet-Thinking]
     ```

2. **For release notes:**
   - Focus on changes between versions
   - Use change type categories (`NEW`, `CHANGED`, `DEPRECATED`, `REMOVED`, `IMPROVED`, `BREAKING`)
   - Organize by change impact areas (Core Language, Standard Library, etc.)
   - Emphasize migration paths and version differences
   - Include specific release date information
   - Highlight backward compatibility considerations
   - Link to both previous version documentation and new version detailed docs
   - Always include this metadata header for consistency:
     ```
     TITLE: [Technology/Language Name] - Version [X.Y.Z]
     VERSION: [X.Y.Z]
     RELEASED: [YYYY-MM-DD]
     COMPATIBILITY: [Compatibility with previous versions, required updates]
     DOCUMENTATION_SOURCE: [Primary URL referenced]
     MODEL: [Claude-3.7-Sonnet-Thinking]
     ```

3. **For language features:**
   - Document argument/parameter conventions and ownership semantics clearly
   - For languages with type parameters or generics, document trait/interface requirements
   - Include performance characteristics, especially for performance-critical features
   - Provide clear examples of error handling approaches
   - Document interoperability with other languages or ecosystems
   - Distinguish between compile-time and runtime behaviors
   - Include examples that demonstrate safe patterns and anti-patterns
   - For languages with memory management, document lifecycle and resource handling

Choose the appropriate elements based on the documentation purpose while maintaining the overall structure for consistency.

## Complete Example

Below is a complete example of a documented component following this template:

### `fetchData()` [`STABLE`]

**Package:** `@example/data-client`
**Available Since:** `v2.1.0`
**Status:** Stable

**Signature:**
```typescript
async function fetchData<T>(
  url: string,
  options?: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    headers?: Record<string, string>;
    body?: string | object;
    timeout?: number;
    retry?: {
      attempts: number;
      backoff: 'linear' | 'exponential';
      initialDelay?: number;
    };
    cache?: 'no-cache' | 'force-cache' | 'reload';
  }
): Promise<{
  data: T;
  status: number;
  headers: Record<string, string>;
  timing: {
    total: number;
    ttfb: number;
  };
}>
```

**Dependencies/Imports:**
```typescript
import { fetchData } from '@example/data-client';
```

**Usage Example:**
```typescript
// Basic usage
const { data, status } = await fetchData<User[]>('https://api.example.com/users');
console.log(`Fetched ${data.length} users`);

// Advanced usage with options
const { data, timing } = await fetchData<OrderResponse>('https://api.example.com/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: { orderId: '12345' },
  timeout: 3000,
  retry: {
    attempts: 3,
    backoff: 'exponential',
    initialDelay: 200
  },
  cache: 'no-cache'
});

console.log(`Request took ${timing.total}ms (TTFB: ${timing.ttfb}ms)`);
```

**Context:**
- Purpose: Provides a robust, type-safe HTTP client for fetching data with advanced options
- Patterns: Promise-based API with typed responses and comprehensive error handling
- Alternatives: Native fetch API, axios, request
- Limitations: Does not support streaming responses
- Related: `useFetchData` React hook, `createFetchClient` factory
- Behavior: Non-blocking, handles JSON parsing automatically for appropriate content types
- Performance: 20% faster than axios for repeated requests to the same endpoint due to connection pooling

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting to handle promise rejection for network failures
- Anti-patterns:
```typescript
// ANTI-PATTERN (ignores errors):
fetchData(url).then(result => {
  // No error handling
});

// CORRECT:
try {
  const result = await fetchData(url);
  // Process result
} catch (error) {
  // Handle error appropriately
}
```
- Edge Cases:
  - Automatically converts 204 No Content responses to `{ data: null }`
  - Retry logic does not apply to 4xx client errors except for 429 Too Many Requests
- Gotchas:
  - When passing an object as body, it's automatically stringified, different from native fetch
  - Timeout includes retry attempts by default

**Security Considerations:**
- CSRF tokens must be manually included in headers when needed
- Automatically strips Authorization headers when redirecting to different origins
- Does not perform automatic URL sanitization - validate URLs before passing them
- [SECURITY-SENSITIVE] Stores cookies by default, disable if handling sensitive data

**Migration:** (from v1.x)
```typescript
// BEFORE (v1.x):
import { get } from '@example/data-client';
const data = await get<User[]>(url, options);

// AFTER (v2.x):
import { fetchData } from '@example/data-client';
const { data } = await fetchData<User[]>(url, { ...options, method: 'GET' });
```
**Migration Difficulty:** Medium - requires updating imports and handling the new response structure

**Further Documentation:**
- [Complete API Reference](https://example.com/docs/api/fetchData) - Full parameter and return type definitions
- [Retry Strategies Guide](https://example.com/docs/guides/retry-strategies) - Advanced configuration for retry behavior
- [Caching Behavior](https://example.com/docs/guides/caching) - Detailed explanation of cache options
- [TypeScript Integration](https://example.com/docs/guides/typescript) - Type-safe usage with TypeScript
- [GitHub Repository](https://github.com/example/data-client) - Source code, issues, and examples
- [Performance Benchmarks](https://example.com/docs/benchmarks) - Detailed performance comparison with alternatives
