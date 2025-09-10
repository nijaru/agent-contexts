#!/usr/bin/env -S uv run python
"""
Update agent-contexts submodules across all projects
Requires Python 3.12+ (uses Path.walk())

Usage:
    update_submodules.py [base_path] [--dry-run] [--no-commit]
    
Examples:
    update_submodules.py                    # Update all in ~/github
    update_submodules.py ~/projects         # Update all in ~/projects  
    update_submodules.py --dry-run          # Preview what would be updated
    update_submodules.py --no-commit        # Update but don't commit
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

def find_repos_with_submodule(base_path: str = "~/github") -> list[Path]:
    """Find all git repos that have agent-contexts as a submodule"""
    base = Path(base_path).expanduser()
    
    if not base.exists():
        print(f"❌ Path does not exist: {base}")
        sys.exit(1)
    
    repos = []
    skip_dirs = {'node_modules', '.venv', 'venv', '__pycache__', 'target', 
                 'build', 'dist', '.pixi', '.git', '.jj', '.tox', 'site-packages'}
    
    try:
        for root, dirs, files in base.walk():
            # Skip unnecessary directories
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
            
            # Check for .gitmodules
            if '.gitmodules' in files:
                gitmodules_path = root / '.gitmodules'
                try:
                    content = gitmodules_path.read_text()
                    if 'agent-contexts' in content:
                        repos.append(root)
                except (OSError, IOError):
                    continue
    except AttributeError:
        print("❌ Error: This script requires Python 3.12+ for Path.walk()")
        print("   Please upgrade Python or use: uv run python update_submodules.py")
        sys.exit(1)
    
    return sorted(repos)

def check_repo_state(repo: Path) -> Tuple[bool, str]:
    """Check if repo is in a good state for updating"""
    # Check for uncommitted changes
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode != 0:
        return False, "Not a git repository"
    
    if result.stdout.strip():
        return False, "Has uncommitted changes (commit or stash first)"
    
    # Check if we're on a branch (not detached HEAD)
    result = subprocess.run(
        ["git", "symbolic-ref", "-q", "HEAD"],
        cwd=repo,
        capture_output=True,
        timeout=5
    )
    
    if result.returncode != 0:
        return False, "In detached HEAD state"
    
    return True, "OK"

def get_submodule_path(repo: Path) -> Optional[str]:
    """Get the path of agent-contexts submodule in a repo"""
    try:
        result = subprocess.run(
            ["git", "config", "--file", ".gitmodules", "--get-regexp", "path"],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        for line in result.stdout.splitlines():
            if "agent-contexts" in line:
                return line.split()[-1]
    except (subprocess.TimeoutExpired, Exception):
        pass
    return None

def update_submodule(repo: Path, commit: bool = True, dry_run: bool = False) -> Tuple[bool, str]:
    """Update agent-contexts submodule in a repository"""
    # Check repo state first
    ok, message = check_repo_state(repo)
    if not ok:
        return False, message
    
    submodule_path = get_submodule_path(repo)
    if not submodule_path:
        return False, "No agent-contexts submodule found"
    
    if dry_run:
        # Check what would be updated
        result = subprocess.run(
            ["git", "submodule", "status", submodule_path],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout.startswith('+'):
            return True, "Would update (submodule has newer commits)"
        else:
            return True, "Already up to date"
    
    try:
        # Update the submodule to latest
        result = subprocess.run(
            ["git", "submodule", "update", "--remote", submodule_path],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            # Try to provide more helpful error message
            if "fatal: Needed a single revision" in result.stderr:
                return False, "Submodule not initialized (run: git submodule init)"
            return False, f"Update failed: {result.stderr.strip()}"
        
        # Check if there are changes
        result = subprocess.run(
            ["git", "diff", "--quiet", submodule_path],
            cwd=repo,
            timeout=5
        )
        
        if result.returncode == 0:
            return True, "Already up to date"
        
        if not commit:
            return True, "Updated (not committed)"
        
        # Stage and commit the update
        subprocess.run(["git", "add", submodule_path], cwd=repo, timeout=5)
        result = subprocess.run(
            ["git", "commit", "-m", "chore: update agent-contexts submodule"],
            cwd=repo,
            capture_output=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return False, f"Commit failed: {result.stderr.strip()}"
        
        return True, "Updated and committed"
        
    except subprocess.TimeoutExpired:
        return False, "Operation timed out"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Update all agent-contexts submodules"""
    # Parse arguments
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    no_commit = "--no-commit" in args
    
    # Remove flags from args
    args = [a for a in args if not a.startswith("--")]
    
    # Get base path
    base_path = args[0] if args else "~/github"
    
    # Header
    if dry_run:
        print("🔍 DRY RUN - Checking agent-contexts submodules...\n")
    else:
        print("🔄 Updating agent-contexts submodules in all projects...\n")
    
    repos = find_repos_with_submodule(base_path)
    
    if not repos:
        print(f"No repositories with agent-contexts submodule found in {base_path}")
        return 1
    
    print(f"Found {len(repos)} repositories with agent-contexts submodule:\n")
    
    updated = 0
    failed = 0
    skipped = 0
    
    for repo in repos:
        display_name = str(repo).replace(str(Path.home()), "~")
        print(f"📦 {display_name}...")
        
        success, message = update_submodule(repo, commit=not no_commit, dry_run=dry_run)
        
        if success:
            if "Updated" in message and "committed" in message:
                updated += 1
                print(f"   ✅ {message}")
            elif "Would update" in message:
                updated += 1
                print(f"   🔄 {message}")
            else:
                print(f"   ✓ {message}")
        else:
            if "uncommitted changes" in message or "detached HEAD" in message:
                skipped += 1
                print(f"   ⚠️  Skipped: {message}")
            else:
                failed += 1
                print(f"   ❌ {message}")
    
    # Summary
    print(f"\n✨ {'Dry run complete!' if dry_run else 'Complete!'}")
    
    if dry_run:
        print(f"   Would update: {updated}")
    else:
        print(f"   Updated: {updated}")
    
    if failed > 0:
        print(f"   Failed: {failed}")
    if skipped > 0:
        print(f"   Skipped: {skipped}")
    
    already_current = len(repos) - updated - failed - skipped
    if already_current > 0:
        print(f"   Already current: {already_current}")
    
    if updated > 0 and not dry_run and not no_commit:
        print("\n📝 Remember to push changes in updated repositories")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())