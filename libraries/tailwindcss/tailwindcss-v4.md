# Unified Technical Documentation: Tailwind CSS v4.0

## Metadata Section
```
TITLE: Tailwind CSS
VERSION: 4.0
RELEASED: 2025-03-10
COMPATIBILITY: Modern browsers supporting cascade layers, registered custom properties, color-mix(), and logical properties; Node.js for build tools
DOCUMENTATION_SOURCE: https://tailwindcss.com/blog/tailwindcss-v4
```

## Conceptual Overview
- **High-Performance Engine**: Complete rewrite achieving 3.78x faster full builds (378ms → 100ms) and up to 182x faster incremental builds with no new CSS (35ms → 192µs).
- **Modern CSS Foundation**: Leverages native cascade layers, registered custom properties, and `color-mix()` for improved maintainability, performance, and smaller CSS output.
- **Simplified Developer Experience**: Reduces setup complexity with zero configuration defaults, automatic content detection, and CSS-first configuration.
- **Design System Access**: All design tokens exposed as native CSS variables for runtime access and manipulation without additional tooling.
- **Enhanced Feature Set**: Built-in container queries, 3D transforms, expanded gradient APIs, and wider color gamut through P3 colors in OKLCH.

## Technical Reference

### Core Features

#### Installation and Setup [`STABLE`]

**Package:** `tailwindcss`, `@tailwindcss/postcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** Yes

**Dependencies/Imports:**
```bash
# Install Tailwind CSS
npm i tailwindcss @tailwindcss/postcss
```

**Configuration:**
```js
// postcss.config.js
export default {
  plugins: ["@tailwindcss/postcss"],
};
```

**Usage Example:**
```css
/* styles.css */
@import "tailwindcss";

/* Start using Tailwind CSS utilities */
.my-component {
  @apply flex items-center justify-between p-4 bg-white rounded-lg shadow;
}
```

**Context:**
- Purpose: Simplified installation with fewer dependencies and zero configuration
- Patterns: Single CSS import replaces multiple `@tailwind` directives
- Alternatives: Previous versions required explicit content configuration and multiple directives
- Behavior: Automatically detects template files and provides sensible defaults
- Performance: Reduces initial setup time and configuration complexity

**Edge Cases and Anti-patterns:**
- Common Mistakes: Including both `@tailwind` directives and `@import "tailwindcss"` causes duplication
- Anti-patterns:
```css
/* ANTI-PATTERN: Mixing old and new import styles */
@import "tailwindcss";
@tailwind utilities; /* Unnecessary and causes conflicts */

/* CORRECT: */
@import "tailwindcss";
```
- Gotchas: The single import loads all styles in a specific order; custom components might need explicit layer declaration

**Migration:**
```css
/* BEFORE (v3.x): */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* AFTER (v4.0): */
@import "tailwindcss";
```
**Migration Difficulty:** Simple

#### High-Performance Engine [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Benchmarks:**
| Operation | v3.4 | v4.0 | Improvement |
| --- | --- | --- | --- |
| Full build | 378ms | 100ms | 3.78x |
| Incremental rebuild (new CSS) | 44ms | 5ms | 8.8x |
| Incremental rebuild (no new CSS) | 35ms | 192µs | 182x |

**Context:**
- Purpose: Optimizes build performance for faster development cycles and production builds
- Performance: Most significant for repeated builds where classes have been used before
- Behavior: Non-blocking, optimized for common utility usage patterns
- Limitations: Performance gains vary based on project size and complexity

**Edge Cases and Anti-patterns:**
- Gotchas: Extremely large projects might still experience longer initial build times
- Edge Cases: When many new utilities are dynamically generated, builds will be slower than cached builds

#### CSS-First Configuration [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** Yes

**Signature:**
```css
@import "tailwindcss";

@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 1920px;
  --color-primary-500: oklch(0.84 0.18 117.33);
  --spacing: 0.25rem;
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  /* ... */
}
```

**Generated CSS:**
```css
:root {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 1920px;
  --color-primary-500: oklch(0.84 0.18 117.33);
  --spacing: 0.25rem;
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  /* ... */
}
```

**Usage Example:**
```css
@import "tailwindcss";

@theme {
  --color-brand: oklch(0.7 0.15 240);
  --breakpoint-xl: 1440px;
}

/* Custom components using theme values */
.brand-button {
  background-color: var(--color-brand);
  color: white;
  padding: calc(var(--spacing) * 4) calc(var(--spacing) * 6);
}
```

**Context:**
- Purpose: Replace JavaScript-based configuration with CSS-based configuration
- Alternatives: Previous versions used tailwind.config.js for customization
- Behavior: All configuration happens in CSS using the `@theme` directive
- Performance: Reduces configuration overhead and leverages browser's CSS parsing
- Related: Automatically exposes design tokens as CSS variables for runtime access

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting to include units for dimension values
- Anti-patterns:
```css
/* ANTI-PATTERN: Using @theme outside main CSS file */
/* styles/theme.css */
@theme { /* ... */ } /* Won't work properly if imported */

/* CORRECT: */
/* styles/main.css */
@import "tailwindcss";
@theme { /* ... */ }
```
- Gotchas: CSS variables defined elsewhere might conflict with theme variables
- Edge Cases: Complex theme extensions might require grouping related variables

**Migration:**
```js
// BEFORE (v3.x, tailwind.config.js):
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: { 500: '#3b82f6' },
      },
      fontFamily: {
        display: ['Satoshi', 'sans-serif'],
      },
      screens: {
        '3xl': '1920px',
      },
    },
  },
};

// AFTER (v4.0, styles.css):
@import "tailwindcss";
@theme {
  --color-primary-500: #3b82f6;
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 1920px;
}
```
**Migration Difficulty:** Medium

#### Automatic Content Detection [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** Yes

**Signature:**
```css
@import "tailwindcss";

/* Optional explicit source inclusion */
@source "../node_modules/@my-company/ui-lib";
```

**Context:**
- Purpose: Eliminates the need to manually configure content paths
- Behavior: Uses heuristics to discover template files, respecting .gitignore and excluding binary files
- Patterns: Auto-detects all version-controlled files with common template extensions
- Performance: Improves initial setup experience and reduces configuration errors
- Limitations: May scan unnecessary files in complex projects without proper .gitignore setup

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting to update .gitignore for generated files
- Anti-patterns:
```css
/* ANTI-PATTERN: Using overly broad @source paths */
@source "node_modules";  /* Scans too many files unnecessarily */

/* CORRECT: */
@source "../node_modules/@my-company/ui-lib";
```
- Gotchas: Binary files are excluded automatically; add specific paths if needed
- Edge Cases: Complex monorepo setups might require explicit `@source` declarations

**Migration:**
```js
// BEFORE (v3.x, tailwind.config.js):
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,html}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
};

// AFTER (v4.0):
// No configuration needed for standard projects
// For special cases:
@import "tailwindcss";
@source "./src/special-location";
```
**Migration Difficulty:** Simple

### APIs

#### @tailwind Directives [`REMOVED`]

**Package:** `tailwindcss`
**Available Until:** `v3.x`
**Status:** Removed in v4.0
**Breaking:** Yes

**Signature (v3.x):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**New Approach (v4.0):**
```css
@import "tailwindcss";
```

**Context:**
- Purpose: Previous approach for injecting Tailwind's styles into CSS
- Breaking: Replaced by single `@import` statement in v4.0
- Migration: Replace all `@tailwind` directives with a single import

**Edge Cases:**
- Gotchas: Custom layer additions needed explicit @layer syntax in v4.0
- Migration Path: Ensure custom components are properly wrapped in @layer directives

**Migration:**
```css
/* BEFORE (v3.x): */
@tailwind base;
@tailwind components;
@layer components {
  .custom-button { /* ... */ }
}
@tailwind utilities;

/* AFTER (v4.0): */
@import "tailwindcss";
@layer components {
  .custom-button { /* ... */ }
}
```
**Migration Difficulty:** Simple

#### @layer Directive [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v3.0` (enhanced in v4.0)
**Status:** Stable
**Breaking:** No

**Signature:**
```css
@layer theme, base, components, utilities;

@layer components {
  .custom-button {
    @apply px-4 py-2 rounded bg-blue-500 text-white;
  }
}
```

**Usage Example:**
```css
@import "tailwindcss";

@layer utilities {
  .scrollbar-hide {
    scrollbar-width: none;
    &::-webkit-scrollbar {
      display: none;
    }
  }
}
```

**Context:**
- Purpose: Define custom styles within Tailwind's cascade layering system
- Patterns: Common for extending components and utilities with custom styles
- Related: Works with native CSS cascade layers in v4.0
- Behavior: Ensures proper style precedence and organization
- Alternatives: Custom CSS without layers (less organized)

**Edge Cases and Anti-patterns:**
- Common Mistakes: Putting utilities in the components layer or vice versa
- Anti-patterns:
```css
/* ANTI-PATTERN: Breaking layer precedence */
@layer utilities {
  .btn { @apply text-lg; } /* Should be in components layer */
}

/* CORRECT: */
@layer components {
  .btn { @apply text-lg; }
}
```
- Gotchas: Custom layers outside the standard ones require explicit declaration
- Edge Cases: Layer conflicts can be challenging to debug

#### theme() Function [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v3.0` (enhanced in v4.0)
**Status:** Stable
**Breaking:** No

**Signature:**
```css
selector {
  property: theme("path.to.value");
}
```

**Usage Example:**
```css
.custom-element {
  background-color: theme("colors.blue.500");
  margin-top: theme("spacing.4");
  font-family: theme("fontFamily.sans");
}
```

**Context:**
- Purpose: Access Tailwind theme values inside custom CSS
- Patterns: Useful for extending styles using theme tokens
- Alternatives: Direct CSS variable references in v4.0
- Related: Works alongside CSS variables from `@theme` configuration
- Behavior: Resolved at build time to actual CSS values

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using theme() outside of CSS processed by Tailwind
- Anti-patterns:
```css
/* ANTI-PATTERN: Using theme() for values available as CSS vars */
.element {
  color: theme("colors.blue.500"); /* In v4, use CSS variables instead */
}

/* BETTER in v4.0: */
.element {
  color: var(--color-blue-500);
}
```
- Gotchas: Path syntax must match theme structure exactly
- Edge Cases: Dynamic theme path references aren't supported

#### @source Directive [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Signature:**
```css
@source "path/to/template/files";
```

**Usage Example:**
```css
@import "tailwindcss";

/* Include templates from design system package */
@source "../node_modules/@company/design-system";
@source "./generated/**/*.js";
```

**Context:**
- Purpose: Explicitly include specific directories in content scanning
- Patterns: Useful for including templates from npm packages or non-standard locations
- Related: Works with automatic content detection
- Behavior: Follows same scanning heuristics as automatic detection

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using overly broad paths that slow down builds
- Anti-patterns:
```css
/* ANTI-PATTERN: Too broad, scans everything */
@source "node_modules";

/* BETTER: */
@source "node_modules/specific-package/dist";
```
- Gotchas: Still excludes binary files and respects .gitignore by default
- Edge Cases: Complex glob patterns may not work as expected

### Utilities

#### Dynamic Utility Values [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Generated CSS:**
```css
@layer utilities {
  .grid-cols-15 {
    grid-template-columns: repeat(15, minmax(0, 1fr));
  }
  .mt-8 {
    margin-top: calc(var(--spacing) * 8);
  }
  .w-17 {
    width: calc(var(--spacing) * 17);
  }
}
```

**Usage Example:**
```html
<!-- Grid with any column count -->
<div class="grid grid-cols-15">
  <!-- ... -->
</div>

<!-- Custom spacing values -->
<div class="mt-17 w-29 p-13">
  <!-- ... -->
</div>

<!-- Data attribute variants -->
<div data-active class="opacity-75 data-active:opacity-100">
  <!-- ... -->
</div>
```

**Context:**
- Purpose: Allows arbitrary numerical values for utilities without configuration or square bracket syntax
- Behavior: Values are dynamically calculated from base scales using CSS calculations
- Performance: Generates only the CSS needed for used values
- Related: Replaces many use cases for arbitrary value syntax (e.g., `w-[4.25rem]`)

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using excessively large values that scale poorly
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Using unnecessarily large values -->
<div class="p-72"><!-- Probably too large --></div>

<!-- BETTER: -->
<div class="p-6"><!-- More reasonable scale --></div>
```
- Gotchas: Different utility types may generate different output for the same number
- Edge Cases: Very large values may lead to performance issues in some browsers

#### Container Queries [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Signature:**
```css
@layer utilities {
  .\\@container {
    container-type: inline-size;
  }
  .\\@sm\\:grid-cols-3 {
    @container (min-width: 640px) {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
  }
}
```

**Usage Example:**
```html
<!-- Basic container queries -->
<div class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-3 @lg:grid-cols-4">
    <!-- ... -->
  </div>
</div>

<!-- Max-width container queries -->
<div class="@container">
  <div class="grid grid-cols-3 @max-md:grid-cols-1">
    <!-- ... -->
  </div>
</div>

<!-- Container query ranges -->
<div class="@container">
  <div class="flex @min-md:@max-xl:hidden">
    <!-- ... -->
  </div>
</div>
```

**Context:**
- Purpose: Style elements based on their container size rather than viewport
- Alternatives: Previously required @tailwindcss/container-queries plugin
- Patterns: Supports min-width (@sm, @md) and max-width (@max-sm, @max-md) queries and ranges
- Related: Similar API to responsive utilities but scoped to container
- Behavior: Uses CSS container queries under the hood

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting to add the `@container` class to parent elements
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Missing @container class -->
<div> <!-- Missing @container class -->
  <div class="@md:flex"><!-- Won't work --></div>
</div>

<!-- CORRECT: -->
<div class="@container">
  <div class="@md:flex"><!-- Works correctly --></div>
</div>
```
- Gotchas: Container queries only apply to size-containment contexts
- Edge Cases: Nesting container contexts can lead to unexpected behavior

#### 3D Transform Utilities [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Usage Example:**
```html
<div class="perspective-distant">
  <article class="rotate-x-51 rotate-z-43 transform-3d scale-y-110 translate-z-12">
    <!-- ... -->
  </article>
</div>
```

**Context:**
- Purpose: Enable 3D transformations directly in HTML
- Features: Includes rotate-x-*, rotate-y-*, scale-z-*, translate-z-*, and perspective utilities
- Related: Works with existing transform utilities to create complex 3D effects
- Alternatives: Custom CSS transforms with more limited control

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting to add perspective to parent container
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Missing perspective context -->
<div> <!-- No perspective -->
  <div class="rotate-x-45"><!-- 3D effect not visible --></div>
</div>

<!-- CORRECT: -->
<div class="perspective-500">
  <div class="rotate-x-45"><!-- 3D effect visible --></div>
</div>
```
- Gotchas: Multiple 3D transforms can interact in unexpected ways
- Edge Cases: Very large transform values can cause visual glitches

#### Expanded Gradient APIs [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** Yes (renames `bg-gradient-*` to `bg-linear-*`)

**Usage Example:**
```html
<!-- Linear gradient with angle -->
<div class="bg-linear-45 from-indigo-500 via-purple-500 to-pink-500"></div>

<!-- Gradient with interpolation mode -->
<div class="bg-linear-to-r/srgb from-indigo-500 to-teal-400">...</div>
<div class="bg-linear-to-r/oklch from-indigo-500 to-teal-400">...</div>

<!-- Conic and radial gradients -->
<div class="size-24 rounded-full bg-conic/[in_hsl_longer_hue] from-red-600 to-red-600"></div>
<div class="size-24 rounded-full bg-radial-[at_25%_25%] from-white to-zinc-900 to-75%"></div>
```

**Context:**
- Purpose: Create sophisticated gradients without custom CSS
- Changes: Renamed bg-gradient-* to bg-linear-*
- Features: Supports angles, interpolation modes, and conic/radial gradients
- Patterns: Works with existing from-*, via-*, and to-* utilities
- Alternatives: Custom CSS with more complex syntax

**Edge Cases and Anti-patterns:**
- Common Mistakes: Mixing incompatible color spaces in the same gradient
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Needlessly complex gradient -->
<div class="bg-linear-45/oklch from-indigo-500 via-blue-400 via-40% via-teal-300 via-60% to-emerald-500"></div>

<!-- BETTER: -->
<div class="bg-linear-45/oklch from-indigo-500 to-emerald-500"></div>
```
- Gotchas: Different interpolation methods can dramatically change gradient appearance
- Edge Cases: Conic gradients can create unexpected effects when percentage stops are used

**Migration:**
```html
<!-- BEFORE (v3.x): -->
<div class="bg-gradient-to-r from-blue-500 to-purple-500"></div>

<!-- AFTER (v4.0): -->
<div class="bg-linear-to-r from-blue-500 to-purple-500"></div>
```
**Migration Difficulty:** Simple

#### not-* Variant [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Generated CSS:**
```css
.not-hover\:opacity-75:not(*:hover) {
  opacity: 75%;
}

@media not (hover: hover) {
  .not-hover\:opacity-75 {
    opacity: 75%;
  }
}

.not-supports-hanging-punctuation\:px-4 {
  @supports not (hanging-punctuation: var(--tw)) {
    padding-inline: calc(var(--spacing) * 4);
  }
}
```

**Usage Example:**
```html
<!-- Not hover state -->
<div class="not-hover:opacity-75">
  <!-- ... -->
</div>

<!-- Not media query -->
<div class="not-dark:text-gray-800">
  <!-- ... -->
</div>

<!-- Not feature support -->
<div class="not-supports-hanging-punctuation:px-4">
  <!-- ... -->
</div>
```

**Context:**
- Purpose: Support CSS :not() pseudo-class for negating conditions
- Features: Works with pseudo-classes, media queries, and @supports queries
- Patterns: Prefix any variant with not- to negate it
- Related: Complements other state variants for comprehensive conditional styling

**Edge Cases and Anti-patterns:**
- Common Mistakes: Complicated negation chains that are hard to reason about
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Overly complex negation -->
<div class="not-hover:not-focus:not-active:bg-gray-100">
  <!-- Hard to understand the intent -->
</div>

<!-- BETTER: -->
<div class="bg-gray-100 hover:bg-white focus:bg-white active:bg-white">
  <!-- Clearer intent -->
</div>
```
- Gotchas: Negating media queries behaves differently than negating pseudo-classes
- Edge Cases: Multiple negated variants can lead to specificity challenges

#### @starting-style Support [`EXPERIMENTAL`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Experimental
**Breaking:** No

**Usage Example:**
```html
<div>
  <button popovertarget="my-popover">Check for updates</button>
  <div popover id="my-popover" class="transition-discrete starting:open:opacity-0 ...">
    <!-- ... -->
  </div>
</div>
```

**Context:**
- Purpose: Animate elements when they first appear without JavaScript
- Limitations: Limited browser support currently
- Related: Works with CSS @starting-style rule for enter/exit transitions
- Alternatives: JavaScript-based animation libraries

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using without checking browser support
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Relying solely on starting-style -->
<div class="starting:opacity-0"> <!-- No fallback for unsupported browsers -->
  <!-- ... -->
</div>

<!-- BETTER: -->
<div class="starting:opacity-0 js-fallback-hidden">
  <!-- With JS fallback for unsupported browsers -->
</div>
```
- Gotchas: No effect in browsers without @starting-style support
- Edge Cases: Complex animations may not work as expected

### Additional Features

#### Color Scheme and Modernized P3 Colors [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Signature:**
```css
@layer utilities {
  .color-scheme-dark {
    color-scheme: dark;
  }
  .color-scheme-light {
    color-scheme: light;
  }
}
```

**Usage Example:**
```html
<!-- Control system UI elements like scrollbars -->
<html class="dark color-scheme-dark">
  <!-- Light scrollbars and form controls in dark mode -->
</html>

<!-- Using P3 colors -->
<div class="bg-blue-500">
  <!-- Uses OKLCH color format for wider gamut -->
</div>
```

**Context:**
- Purpose: Control system UI elements' appearance and provide more vivid colors
- Features: Support for `color-scheme` property and P3 color space via OKLCH
- Related: Works with dark mode variant for consistent theming
- Performance: OKLCH colors render more efficiently on modern displays

**Edge Cases and Anti-patterns:**
- Common Mistakes: Using non-matching color schemes and background colors
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Mismatched scheme -->
<html class="dark color-scheme-light">
  <!-- Dark background but light UI controls = poor contrast -->
</html>

<!-- CORRECT: -->
<html class="dark color-scheme-dark">
  <!-- Everything is dark mode -->
</html>
```
- Gotchas: P3 colors fallback to closest sRGB equivalent on unsupported displays
- Edge Cases: Some older browsers ignore color-scheme property

#### New Utility Features [`STABLE`]

**Package:** `tailwindcss`
**Available Since:** `v4.0.0`
**Status:** Stable
**Breaking:** No

**Features:**
- `inset-shadow-*` and `inset-ring-*`: Stack up to four layers of box shadows
- `field-sizing`: Auto-resize form elements without JavaScript
- `font-stretch`: Adjust variable font widths
- `inert` variant: Style elements with the inert attribute
- `nth-*` variants: Target elements by position
- `in-*` variant: Similar to group-* without needing the group class
- `descendant` variant: Style all descendant elements

**Usage Example:**
```html
<!-- Multiple layered shadows -->
<div class="shadow-md inset-shadow-sm inset-ring-2 inset-ring-blue-500/20">
  <!-- Multiple shadow effects -->
</div>

<!-- Auto-resizing textarea -->
<textarea class="field-sizing-content"></textarea>

<!-- Target positions -->
<ul>
  <li class="nth-1:font-bold nth-even:bg-gray-100">Item 1</li>
  <li>Item 2</li>
</ul>
```

**Context:**
- Purpose: Expand utility coverage to more CSS features
- Patterns: Follows consistent naming patterns with existing utilities
- Alternatives: Custom CSS with more verbose syntax
- Performance: Utilities are only generated when used

**Edge Cases and Anti-patterns:**
- Common Mistakes: Overuse of complex selectors like nth-* and descendant
- Anti-patterns:
```html
<!-- ANTI-PATTERN: Excessive nesting and targeting -->
<div class="descendant:nth-odd:text-blue-500 descendant:nth-even:text-red-500">
  <!-- Hard to maintain and reason about -->
</div>

<!-- BETTER: -->
<div>
  <div class="odd:text-blue-500 even:text-red-500">
    <!-- More explicit and clear -->
  </div>
</div>
```
- Gotchas: Some complex selectors have performance implications
- Edge Cases: Deep nesting with complex variants can lead to specificity issues

## Migration

**Overall Migration Difficulty:** Medium

**Key Breaking Changes:**
1. Replacement of `@tailwind` directives with `@import "tailwindcss"`
2. Moving from `tailwind.config.js` to CSS `@theme` directive
3. Renaming of `bg-gradient-*` to `bg-linear-*`

**Automated Migration:**
- An upgrade tool is available to handle most changes automatically
- Converts tailwind.config.js to @theme rules
- Simplifies arbitrary values that are now supported natively
- Updates class names for renamed utilities

**Context:**
- Purpose: Smooth transition from v3.x to v4.0
- Behavior: Preserves customizations while updating syntax
- Limitations: Complex configurations may require manual adjustments

## Further Documentation

- [Installation Guide](https://tailwindcss.com/docs/installation) - Complete setup instructions
- [Upgrade Guide](https://tailwindcss.com/docs/upgrade-guide) - Migration instructions from v3.x
- [Upgrade Tool](https://tailwindcss.com/docs/upgrade-guide#using-the-upgrade-tool) - Automated migration utility
- [Theme Variables](https://tailwindcss.com/docs/theme) - CSS-first configuration details
- [Container Queries](https://tailwindcss.com/docs/responsive-design#container-queries) - Container-based responsive design
- [Detecting Classes](https://tailwindcss.com/docs/detecting-classes-in-source-files) - How automatic content detection works
- [Tailwind Play](https://play.tailwindcss.com/) - Interactive playground for experimenting with v4.0
- [GitHub Repository](https://github.com/tailwindlabs/tailwindcss) - Source code and issues
