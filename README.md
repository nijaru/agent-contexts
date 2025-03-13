# Agent Contexts

A collection of markdown files that provide up-to-date context to AI coding assistants like GitHub Copilot, Cursor, and Claude Code.

## Purpose

This repository contains specialized documentation and reference materials formatted as markdown files that can be added as context when working with AI coding assistants. These files help the AI better understand specific programming languages, frameworks, libraries, development tools, and best practices.

## Use Cases

- Enhancing AI code completion and suggestions
- Providing domain-specific knowledge to AI coding agents
- Standardizing documentation format for AI consumption
- Improving accuracy of AI-assisted programming

## Repository Structure

### Active Directories

#### Languages

- [📁 `/languages/go`](./languages/go)
  <br>Go programming language, including release notes, standard library documentation, and best practices
- [📁 `/languages/mojo`](./languages/mojo)
  <br>Mojo programming language, including built-ins, language guide, style guide, and standard library modules
- [📁 `/languages/python`](./languages/python)
  <br>Python programming language, including release notes for version 3.13.0

#### Tools

- [📁 `/tools/modular`](./tools/modular)
  <br>Modular's AI development tools and ecosystems
  - [📁 `/tools/modular/max`](./tools/modular/max)
    <br>MAX (Modular AI Execution) engine and API documentation for AI model inference
- [📁 `/tools/python`](./tools/python)
  <br>Python development tools
  - [📁 `/tools/python/uv`](./tools/python/uv/uv.md)
    <br>uv package installer and environment manager

#### Libraries

- [📁 `/libraries/tailwindCSS`](./libraries/tailwindCSS)
  <br>Documentation for Tailwind CSS, including version 4 reference

### Planned Directories

The following directories are planned but not yet implemented:

- 📁 `/frameworks` - Web, mobile and other frameworks
- 📁 `/patterns` - Design patterns and architecture
- 📁 `/best-practices` - Coding standards and conventions

## Contributing

Contributions are welcome! Please follow these guidelines:
- Use clear, concise language optimized for AI consumption
- Format using standard markdown following our [Style Guide](./STYLE-GUIDE.md)
- Focus on technical accuracy and current best practices
- Include relevant code examples where helpful
- Run validation tools mentioned in the [Style Guide](./STYLE-GUIDE.md) before submitting

## License

This repository is licensed under the [Apache License, Version 2.0](./LICENSE). You are free to use, modify, and distribute these context files for any AI coding assistant in accordance with the terms of this license.
