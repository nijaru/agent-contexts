# Release Management Patterns for AI Agents

*Standard patterns for software release processes, changelog maintenance, and version management*

## CRITICAL RULES

### 🚨 NEVER RELEASE WITHOUT EXPLICIT APPROVAL
- **"prep release"** = prepare only, do NOT publish
- **"release it"** = explicit approval to publish to PyPI/GitHub
- Build packages, update docs, stage everything - but STOP until approved

## DECISION TREES

### Release Documentation Strategy
```
IF python_package:
    → Use CHANGELOG.md + GitHub Releases (dual approach)
IF web_framework:
    → Follow Keep a Changelog format with clear categories
IF library/tool:
    → CHANGELOG.md sufficient, GitHub releases optional
IF enterprise_software:
    → Add detailed release notes in docs/ directory
```

### Version Bumping Strategy
```
IF breaking_changes:
    → Major version bump (1.0.0 → 2.0.0)
IF new_features:
    → Minor version bump (1.0.0 → 1.1.0)
IF bug_fixes_only:
    → Patch version bump (1.0.0 → 1.0.1)
```

### Release Timing
```
IF critical_security_fix:
    → Release immediately after testing
IF major_feature_complete:
    → Wait for comprehensive testing, then release
IF breaking_changes:
    → Announce deprecations first, breaking changes in next major
```

## FILE STRUCTURE PATTERNS

### Standard Layout
```
/CHANGELOG.md              # Keep a Changelog format
/docs/release-notes/       # Optional: detailed release notes
/.github/RELEASE_TEMPLATE  # Optional: GitHub release template
```

### Version Files
```python
# For Python packages
/package_name/__version__.py    # Single source of truth
__version__ = "1.2.3"

# pyproject.toml
dynamic = ["version"]           # Read from __version__.py
```

## CHANGELOG.MD FORMAT

### Header Template
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.3] - 2025-09-18

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features

### Deprecated
- Features marked for removal

### Security
- Security vulnerability fixes
```

### Change Categories (Use These Consistently)
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Fixed**: Bug fixes
- **Removed**: Features removed
- **Deprecated**: Features marked for future removal
- **Security**: Security vulnerability fixes

### Writing Guidelines
- Write for humans, not machines
- Use past tense: "Added SSE support" not "Add SSE support"
- Be specific: "Fixed SSE throttling after first event" not "Fixed SSE bug"
- Group similar changes together
- Most recent version first
- Use ISO dates (YYYY-MM-DD)

## RELEASE PROCESS PATTERNS

### Pre-Release Checklist
```bash
# Version consistency check
grep -E "version.*[0-9]\.[0-9]\.[0-9]" pyproject.toml package/__version__.py README.md

# Test suite verification
pytest --maxfail=1 -x -q

# Example/documentation verification
for f in examples/*.py; do python -m py_compile "$f"; done

# Clean artifacts
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
```

### Build and Release Commands
```bash
# Build packages
uv build

# Upload to PyPI (ONLY after explicit approval)
twine upload dist/package-name-*

# Create GitHub release
gh release create v1.2.3 --title "v1.2.3: Brief Description" --notes-file RELEASE_NOTES.md
```

### Post-Release Tasks
```bash
# Verify package availability
pip install package-name==1.2.3 --dry-run

# Clean up temporary files
rm RELEASE_NOTES_*.md

# Update documentation if needed
```

## GITHUB RELEASES BEST PRACTICES

### Release Title Format
```
v1.2.3: Brief Description of Main Feature
```

### Release Notes Structure
```markdown
## 🚀 What's New
- Key features and improvements

## 🔧 Technical Changes
- Performance improvements
- Architecture changes

## 📋 Bug Fixes
- Critical fixes
- Minor fixes

## 💥 Breaking Changes
- List any breaking changes
- Migration instructions

## 📦 Installation
pip install package-name==1.2.3
```

### Use Emojis Sparingly
- ✅ For major sections (🚀 🔧 📋 💥)
- ❌ For individual bullet points
- ❌ Overuse that clutters readability

## VERSION MANAGEMENT

### Semantic Versioning Rules
- **MAJOR**: Breaking changes (1.0.0 → 2.0.0)
- **MINOR**: New features, backward compatible (1.0.0 → 1.1.0)
- **PATCH**: Bug fixes, backward compatible (1.0.0 → 1.0.1)

### Pre-release Versions
- **Alpha**: 1.0.0-alpha.1 (internal testing)
- **Beta**: 1.0.0-beta.1 (external testing)
- **RC**: 1.0.0-rc.1 (release candidate)

### Version Consistency Check
```bash
# Ensure version is consistent across files
VERSION=$(python -c "from package import __version__; print(__version__)")
grep -q "$VERSION" README.md || echo "README version mismatch"
grep -q "$VERSION" pyproject.toml || echo "pyproject.toml version mismatch"
```

## DEPRECATION PATTERNS

### Announcing Deprecations
```markdown
## [1.5.0] - 2025-09-18

### Deprecated
- `old_function()` is deprecated. Use `new_function()` instead. Will be removed in v2.0.0.
- The `legacy_config` parameter is deprecated. Use `modern_config` instead.
```

### Code Deprecation Warnings
```python
import warnings

def old_function():
    warnings.warn(
        "old_function() is deprecated and will be removed in v2.0.0. "
        "Use new_function() instead.",
        DeprecationWarning,
        stacklevel=2
    )
```

## ERROR PATTERNS → SOLUTIONS

| Error | Solution | Context |
|-------|----------|---------|
| `twine: command not found` | `pip install twine` | PyPI upload |
| `gh: command not found` | `brew install gh` or download from GitHub | GitHub releases |
| `Version already exists` | Bump version number | PyPI won't allow overwrites |
| `Invalid changelog format` | Follow Keep a Changelog structure | Automated tools expect standard format |

## FRAMEWORK-SPECIFIC PATTERNS

### Python Web Frameworks
- Maintain both CHANGELOG.md and GitHub releases
- Include performance benchmarks in major releases
- Document breaking changes prominently
- Provide migration guides for major versions

### Python Libraries
- CHANGELOG.md often sufficient
- GitHub releases for major milestones
- Include API compatibility notes
- Document dependencies changes

### CLI Tools
- GitHub releases primary
- Include installation instructions
- Document command changes
- Provide before/after examples

## AUTOMATION OPPORTUNITIES

### GitHub Actions for Releases
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build package
        run: uv build
      - name: Upload to PyPI
        run: twine upload dist/*
```

### Automated Changelog Generation
- Use conventional commits for automated changelog
- Tools: `auto-changelog`, `conventional-changelog`
- Generate first draft, then human review/edit

---

*Remember: Releases are permanent. Take time to verify everything before publishing.*