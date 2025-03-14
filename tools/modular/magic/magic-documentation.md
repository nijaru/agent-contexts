# TITLE: Magic Package Manager
VERSION: 25.1 (based on MAX version references)
COMPATIBILITY: macOS and Ubuntu, supports Python and Mojo languages
DOCUMENTATION_SOURCE: https://docs.modular.com/magic/
MODEL: Claude-3.7-Sonnet-Thinking

## Conceptual Overview

- **Magic is a unified package manager and virtual environment manager** for multiple programming languages, with special support for Python and Mojo
- **Built on conda and PyPI ecosystems**, providing access to thousands of existing packages while adding specialized functionality for MAX and Mojo
- **Creates reproducible, isolated environments** with automatic dependency resolution and management
- **Supports multiple project formats** including pyproject.toml for Python projects and mojoproject.toml for Mojo projects
- **Simplified workflow** for creating, managing, and sharing development environments across different machines

## Core Features

### `magic init` [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
magic init [OPTIONS] [PATH]
```

**Parameters:**
- `PATH` - Where to place the project (defaults to current path)
- `--channel, -c <channel>` - Channels to use in the project
- `--platform, -p <platform>` - Platforms that the project supports
- `--import, -i <ENV_FILE>` - Environment.yml file to bootstrap the project
- `--format <FORMAT>` - The manifest format to create (magic, pyproject, mojoproject)

**Usage Example:**
```bash
# Create a Python project
magic init my-project --format pyproject

# Create a Mojo project
magic init my-mojo-project --format mojoproject

# Import from existing conda environment
magic init --import environment.yml
```

**Context:**
- Purpose: Creates a new project with its own package dependencies and virtual environment
- Patterns: Creates a configuration file (pixi.toml, pyproject.toml, or mojoproject.toml) that defines project dependencies and settings
- Alternatives: conda create, venv, pyenv
- Behavior: Creates project configuration and directory structure
- Related: `magic add`, `magic run`, `magic shell`

**Edge Cases and Anti-patterns:**
- Common Mistake: Not specifying a format, which defaults to pixi.toml instead of specialized formats
- Anti-pattern: Creating nested Magic projects (may cause environment conflicts)
- Gotcha: The --format flag is important for language-specific features

### `magic add` [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
magic add [OPTIONS] <SPECS>...
```

**Parameters:**
- `SPECS` - The dependencies as names, conda MatchSpecs or PyPi requirements
- `--host` - The specified dependencies are host dependencies
- `--build` - The specified dependencies are build dependencies
- `--pypi` - The specified dependencies are PyPI dependencies
- `--platform, -p <PLATFORM>` - The platform(s) for which the dependency should be modified
- `--feature, -f <FEATURE>` - The feature for which the dependency should be modified
- `--no-lockfile-update` - Don't update lockfile, implies no-install as well
- `--no-install` - Don't modify the environment, only modify the lock-file

**Usage Example:**
```bash
# Add a specific version of a package
magic add "max~=25.1"

# Add multiple packages
magic add "numpy<2.0" "pandas>=2.0"

# Add a PyPI package
magic add --pypi "requests>=2.0"

# Add a platform-specific dependency
magic add python --platform linux-64 --platform osx-arm64
```

**Context:**
- Purpose: Adds packages to the project's dependencies
- Patterns: Uses conda MatchSpec or PyPI requirement formats for version specification
- Behavior: Updates the project configuration file and lock file, then installs the package
- Related: `magic remove`, `magic update`, `magic install`

**Edge Cases and Anti-patterns:**
- Common Mistake: Mixing conda and PyPI packages in the same project (should be avoided)
- Gotcha: Without version specification, the latest version will be chosen automatically
- Anti-pattern: Adding packages without version constraints, leading to potential future compatibility issues

### `magic run` [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
magic run [OPTIONS] <TASK>...
```

**Parameters:**
- `TASK` - The magic task or a task shell command to run in the project's environment
- `--environment, -e <ENVIRONMENT>` - The environment to run the task in
- `--frozen` - Install the environment as defined in the lockfile
- `--locked` - Check if lockfile is up-to-date before installing the environment
- `--clean-env` - Use a clean environment to run the task

**Usage Example:**
```bash
# Run a Python command in the project environment
magic run python --version

# Run a Mojo command in the project environment
magic run mojo --version
```

**Context:**
- Purpose: Executes commands within the project's virtual environment
- Patterns: Used for running project code or environment commands
- Alternatives: Activating the environment with `magic shell` then running commands
- Behavior: Temporarily activates the environment, runs the command, then exits
- Related: `magic shell`

**Edge Cases and Anti-patterns:**
- Common Mistake: Running `magic run` outside a project directory
- Anti-pattern: Using `magic run` for long-running processes when `magic shell` would be more appropriate

### `magic shell` [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
magic shell [OPTIONS]
```

**Parameters:**
- `--environment, -e <ENVIRONMENT>` - The environment to activate in the shell
- `--frozen` - Install the environment as defined in the lockfile
- `--locked` - Check if lockfile is up-to-date before installing the environment
- `--change-ps1 <CHANGE_PS1>` - Control whether to change the PS1 variable (true/false)

**Usage Example:**
```bash
# Activate the project environment
magic shell

# When finished, exit the environment shell
exit
```

**Context:**
- Purpose: Activates the project's virtual environment in an interactive shell
- Patterns: Used for interactive development sessions
- Behavior: Modifies the current shell to use the project's environment
- Related: `magic run`, `magic shell-hook`

**Edge Cases and Anti-patterns:**
- Common Mistake: Forgetting to exit the shell before switching to another project
- Edge Case: Must always exit the shell with `exit` before changing projects

### `magic update` [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
magic update [OPTIONS] [PACKAGES]...
```

**Parameters:**
- `PACKAGES` - The packages to update
- `--environment, -e <ENVIRONMENTS>` - The environments to update
- `--platform, -p <PLATFORMS>` - The platforms to update
- `--no-install` - Don't install the environments needed for PyPI-dependencies solving
- `--dry-run, -n` - Don't write the lockfile or update any environment

**Usage Example:**
```bash
# Update a specific package
magic update max

# Update all packages
magic update
```

**Context:**
- Purpose: Updates dependencies to newer versions while respecting version constraints
- Behavior: Updates the lock file and installs the updated packages
- Related: `magic add`, `magic install`

## Configuration Management

### Project Configuration Files [`STABLE`]

**Available Since:** Not explicitly specified
**Status:** Stable

**Types:**
- `pixi.toml` - Default Magic project configuration
- `pyproject.toml` - Enhanced Python project configuration
- `mojoproject.toml` - Enhanced Mojo project configuration

**Structure Example:**
```toml
# Example pyproject.toml content
[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
requires-python = ">= 3.11"

[dependencies]
# Magic-specific dependencies section
max = "~=25.1"
numpy = "<2.0"

[tool.magic]
channels = ["https://conda.modular.com/max-nightly", 
            "https://conda.modular.com/max", 
            "https://repo.prefix.dev/modular-community", 
            "conda-forge"]
```

**Context:**
- Purpose: Defines the project metadata, dependencies, and configuration
- Patterns: Configuration is in TOML format with project-specific sections
- Behavior: Controls how Magic manages the project environment

**Edge Cases and Anti-patterns:**
- Common Mistake: Editing both the configuration file and using CLI commands to manage the same settings
- Gotcha: Manual edits to the file may require running `magic install` to apply changes

### `magic.lock` File [`STABLE`]

**Available Since:** Not explicitly specified
**Status:** Stable

**Context:**
- Purpose: Ensures reproducible environments by locking all dependencies and their versions
- Patterns: Automatically generated and updated, should not be manually edited
- Behavior: Records exact versions of all dependencies, including transitive dependencies
- Related: Lock file concepts from package managers like npm (package-lock.json) or pip (requirements.txt)

**Edge Cases and Anti-patterns:**
- Anti-pattern: Manually editing the lock file (should always be managed by Magic)
- Gotcha: The lock file should be committed to version control to ensure reproducibility

## Package Management

### Default Channels [`STABLE`]

**Available Since:** Not explicitly specified
**Status:** Stable

**Available Channels:**
- `https://conda.modular.com/max-nightly` - Includes all MAX packages, including nightly and stable builds
- `https://conda.modular.com/max` - Includes only MAX stable builds
- `https://repo.prefix.dev/modular-community` - Official community-created packages for MAX
- `conda-forge` - Comprehensive repository of conda packages from the conda-forge community

**Usage Example:**
```toml
# In pyproject.toml or mojoproject.toml
channels = ["https://conda.modular.com/max-nightly", 
            "https://conda.modular.com/max", 
            "https://repo.prefix.dev/modular-community", 
            "conda-forge"]
```

**Context:**
- Purpose: Specifies package sources for conda dependencies
- Behavior: Magic searches channels in the order specified for packages
- Related: PyPI for Python packages

**Edge Cases and Anti-patterns:**
- Gotcha: Channel order matters, as packages from earlier channels take precedence
- Common Mistake: Using `max-nightly` in production environments instead of stable channels

### Version Specification [`STABLE`]

**Available Since:** Not explicitly specified
**Status:** Stable

**Syntax Examples:**
- `package==1.0.0` - Exact version
- `package>=1.0.0` - Greater than or equal to version
- `package<2.0.0` - Less than version
- `package~=1.0.0` - Compatible with version (equivalent to >=1.0.0,<2.0.0)

**Usage Example:**
```bash
# Specify an exact version
magic add "python==3.9.0"

# Specify a compatible version
magic add "max~=25.1"

# Specify a version range
magic add "numpy>=1.20.0,<2.0.0"
```

**Context:**
- Purpose: Defines version constraints for dependencies
- Patterns: Uses standard Python version specifier syntax
- Behavior: Ensures consistent dependency resolution across environments
- Related: Python's PEP 440 version specifiers

**Edge Cases and Anti-patterns:**
- Common Mistake: Not specifying version constraints, potentially leading to breaking changes
- Best Practice: Always specify version constraints for production environments

## Installation and Setup

### Installation [`STABLE`]

**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
curl -ssL https://magic.modular.com/ | bash
```

**Platforms:**
- macOS
- Ubuntu

**Context:**
- Purpose: Installs the Magic CLI tool
- Behavior: Downloads and installs Magic to ~/.modular/bin/magic
- Related: `magic self-update`

**Edge Cases and Anti-patterns:**
- Gotcha: Must run the source command that's printed in the terminal after installation
- Security: Review the install script if concerned about running commands directly from curl

### `magic self-update` [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Signature:**
```bash
magic self-update
```

**Context:**
- Purpose: Updates Magic to the latest version
- Behavior: Downloads and installs the latest version of Magic

## Python Project Workflows

### Python Project Creation [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Usage Example:**
```bash
# Create a Python project
magic init my-project --format pyproject

# Navigate to the project
cd my-project

# Run Python in the environment
magic run python --version

# Add Python packages
magic add "numpy<2.0" "pandas"
```

**Context:**
- Purpose: Streamlines setup of Python development environments
- Patterns: Creates standardized pyproject.toml for Python project configuration
- Behavior: Sets up Python-specific project structure and environment
- Related: `magic add`, `magic run`, `magic shell`

**Migration from Conda:**
```bash
# Import existing conda environment
magic init --import environment.yml
```

## Mojo Project Workflows

### Mojo Project Creation [`STABLE`]

**Package:** Magic CLI
**Available Since:** Not explicitly specified
**Status:** Stable

**Usage Example:**
```bash
# Create a Mojo project
magic init my-mojo-project --format mojoproject

# Navigate to the project
cd my-mojo-project

# Run Mojo in the environment
magic run mojo --version

# Add Python alongside Mojo
magic add "python==3.9"
```

**Context:**
- Purpose: Streamlines setup of Mojo development environments
- Patterns: Creates standardized mojoproject.toml for Mojo project configuration
- Behavior: Sets up Mojo-specific project structure and environment with MAX
- Related: `magic add`, `magic run`, `magic shell`

## Known Issues and Limitations

- Invoking `magic` within a `conda` or `venv` virtual environment may cause issues
- Mixing Magic with other virtual environment tools is not recommended
- Linux aarch64 (ARM64) does not work with projects using PyTorch 2.2.2
- The MAX Replit pipeline currently doesn't work with the max-conda package
- Magic does not support `exec`, `auth`, and `upload` commands that are available in Pixi

## Additional Information

Magic is built upon `pixi`, and much of the documentation for `pixi` applies to Magic (with `magic` replacing `pixi` in commands). However, there are differences between the two tools, as noted in the Known Issues and Limitations section.

### Further Documentation:
- [Magic Commands](https://docs.modular.com/magic/commands) - Complete command reference
- [Magic FAQ](https://docs.modular.com/magic/faq) - Frequently asked questions
- [Magic Tutorial](https://docs.modular.com/max/tutorials/magic/) - Detailed tutorial on using Magic
- [Pixi Documentation](https://pixi.sh/latest/) - Documentation for the underlying Pixi tool
