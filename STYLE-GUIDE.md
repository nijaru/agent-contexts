# Agent Contexts Style Guide

This document outlines the formatting and style conventions for all markdown files in the Agent Contexts repository. Following these conventions ensures consistency and readability, and optimizes content for AI coding assistants.

## Markdown Formatting

- Use GitHub Flavored Markdown (GFM) for all documentation
- Write one sentence per line for better diff readability
- Use blank lines between paragraphs and logical sections
- Indent nested list items with 2 spaces
- Format code blocks with appropriate language tags:
  ```python
  def example_function():
      return "This is a Python example"
  ```
  ```mojo
  fn example_function() -> String:
      return "This is a Mojo example"
  ```

## Heading Structure

- Use heading levels properly:
  - `# Title` - File title (only one per file)
  - `## Section` - Major sections
  - `### Subsection` - Subsections
  - `#### Minor heading` - Further divisions if needed
- Keep heading hierarchy sequential (don't skip levels)
- Use sentence case for headings

## Content Guidelines

- Focus on practical, concise information optimized for AI assistants
- Include standard library documentation, style guides, and best practices
- Link to official documentation when possible using descriptive link text
- Keep files focused on a single topic or component
- Use tables for presenting structured data
- Include examples that demonstrate practical usage
- Avoid excessive verbosity or tangential information

## File Organization

- Organize language contexts in `languages/` directory
- Organize tool contexts in `tools/` directory
- Each major subdirectory should have a README.md
- Maintain consistent naming conventions (kebab-case for filenames)
- Group related information in logical sections
- Use front matter or table of contents for longer documents

## Images and Diagrams

- Use SVG format when possible for diagrams
- Include alt text for all images
- Ensure diagrams have clear, readable labels
- Place images in an `assets` folder relative to markdown files

## Links and References

- Use relative links for internal repository references
- Check all external links periodically to ensure they are not broken
- Prefer permanent links when referencing external content
- Use descriptive link text rather than generic phrases like "click here"

## Validation

Before submitting changes, validate your markdown using:
- `mdformat --check '**/*.md'` or `mdformat '**/*.md'` to auto-format
- `npx cspell '**/*.md'` for spellchecking
- `npx markdown-link-check '**/*.md'` for link validation