# Unified Technical Documentation Generator for LLM Coding Assistants

This template creates structured, LLM-optimized documentation based on technical content for coding assistants like GitHub Copilot, Claude Code, or Cursor. It works for both comprehensive documentation and version-specific release notes.

## Information Gathering Process

1. **Analyze the Primary Source**
   - Thoroughly read and analyze all content at the provided URL
   - Identify key technical components, APIs, patterns, concepts, and changes
   - Note version information, release dates, and compatibility requirements

2. **Follow All Referenced Links (Critical Step)**
   - Always follow links to detailed API documentation to extract complete signatures and type definitions
   - For new features/components, immediately locate the canonical documentation via links
   - When primary documentation lacks technical details, find and analyze the complete specifications
   - Trace links to implementation details, especially for non-obvious behavior or edge cases
   - Examine referenced issues, discussions, or examples to understand design decisions
   - For linked documents that reference additional resources, follow those chains as well
   - Continue until you have complete technical details for each significant component or change
   - Never rely solely on summary information when complete technical details are available via links

3. **Collect Comprehensive Technical Details**
   - Gather complete function/method signatures with all parameters and return types
   - Document class/type definitions with properties and methods
   - Identify required imports, dependencies, or prerequisites
   - Extract representative code examples showing proper usage
   - Note compatibility constraints, platform requirements, or version limitations
   - Research backward compatibility information and migration paths
   - Understand migration paths for deprecations or breaking changes

## Documentation Structure

Create a token-efficient document with this structure:

### Metadata Section
```
TITLE: [Technology/Component Name]
VERSION: [version number/date]
RELEASED: [YYYY-MM-DD] (if applicable for release notes)
COMPATIBILITY: [runtime requirements, dependencies, breaking changes]
DOCUMENTATION_SOURCE: [primary URL referenced]
```

### Conceptual Overview
Provide 3-5 bullet points summarizing:
- Key concepts or programming patterns introduced
- Major capabilities, features, or changes
- Significant changes from previous versions (if applicable)
- Intended use cases or problems solved

### Technical Reference

For each significant component or change, use this consistent structure:

#### [Component/Feature Name] [`NEW`|`CHANGED`|`STABLE`|`EXPERIMENTAL`|`DEPRECATED`|`REMOVED`]

**Namespace/Package:** `package/namespace/path`
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

**Migration:** (if applicable)
```[language]
// BEFORE:
oldFunction(param);

// AFTER:
newFunction(param);
```

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
     * Ensure the example demonstrates any non-obvious patterns or requirements

2. **Prioritize Information:**
   - Parameter types, order, and constraints
   - Return value structures and error handling patterns
   - Interaction patterns with other components
   - Version-specific behavior differences
   - Security considerations or best practices
   - Migration paths and backward compatibility information

3. **Visual Clarity:**
   - Use consistent formatting for similar components
   - Mark breaking changes clearly with 🚨 or `BREAKING`
   - Mark experimental features with 🧪 or `EXPERIMENTAL`
   - Use indentation to show relationships between components
   - Use bold for component names and important constraints

4. **Token Efficiency:**
   - Use concise language throughout
   - Include only the most relevant information for code generation
   - Avoid redundancy across examples and descriptions
   - Include just enough context for proper understanding

## Final Verification

Before submitting the documentation:

1. Verify all technical signatures are complete with proper types
2. Ensure all code examples are syntactically valid and representative
3. Check that all breaking changes have migration examples
4. Confirm all dependencies and requirements are clearly specified
5. Validate that examples demonstrate idiomatic usage patterns
6. Ensure the documentation is organized logically by related functionality
7. For release notes, verify that all significant changes are documented with appropriate version information

The documentation should be comprehensive enough for an LLM coding assistant to generate correct code using the documented technology, while being optimized for token efficiency and context window limitations.

## Documentation Type Selection

When generating documentation:

1. **For comprehensive technical documentation:**
   - Focus on complete API coverage
   - Use component status categories (`NEW`, `STABLE`, `EXPERIMENTAL`, `DEPRECATED`)
   - Organize by functional categories (Core Features, APIs, Data Types, etc.)
   - Emphasize component relationships and architecture

2. **For release notes:**
   - Focus on changes between versions
   - Use change type categories (`NEW`, `CHANGED`, `DEPRECATED`, `REMOVED`)
   - Organize by change impact areas (Core Language, Standard Library, etc.)
   - Emphasize migration paths and version differences
   - Include specific release date information
   - Highlight backward compatibility considerations

Choose the appropriate elements based on the documentation purpose while maintaining the overall structure for consistency.
