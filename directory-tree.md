# Repository Directory Structure

This document provides a comprehensive list of all directories in the agent-contexts repository with their paths and descriptions.

## Table of Contents

- [Active Directories](#active-directories)
  - [Languages](#languages)
  - [Tools](#tools)
- [Planned Directories](#planned-directories)
- [Contributing](#contributing-new-directories)

## Active Directories

### Languages

- [📁 `/languages/go`](./languages/go)
  <br>Go programming language, including release notes, standard library documentation, and best practices
- [📁 `/languages/mojo`](./languages/mojo)
  <br>Mojo programming language, including built-ins, language guide, style guide, and standard library modules

### Tools

- [📁 `/tools/python`](./tools/python)
  <br>Python development tools
  - [📁 `/tools/python/uv`](./tools/python/uv/uv.md)
    <br> uv package installer and environment manager

## Planned Directories

The following directories are planned but not yet implemented:

- 📁 `/frameworks` - Web, mobile and other frameworks
- 📁 `/patterns` - Design patterns and architecture
- 📁 `/best-practices` - Coding standards and conventions

## Contributing New Directories

When adding new directories to this repository:

1. Create a README.md for major subdirectories outlining their purpose and contents (Use [mojo/README.md](./languages/mojo) for an example)
1. Update this file with the new directory path and description
1. Follow the style guidelines in [CLAUDE.md](./CLAUDE.md)
