#!/usr/bin/env python3
"""
Update agent-contexts submodules across all projects
"""

import os
import subprocess
from pathlib import Path
from typing import List, Tuple

def find_repos_with_submodule(base_path: str = "~/github") -> List[Path]:
    """Find all git repos that have agent-contexts as a submodule"""
    base = Path(base_path).expanduser()
    repos = []
    
    # Search for .gitmodules files
    for gitmodules in base.rglob(".gitmodules"):
        if gitmodules.is_file():
            with open(gitmodules) as f:
                if "agent-contexts" in f.read():
                    repos.append(gitmodules.parent)
    
    return repos

def get_submodule_path(repo: Path) -> str:
    """Get the path of agent-contexts submodule in a repo"""
    result = subprocess.run(
        ["git", "config", "--file", ".gitmodules", "--get-regexp", "path"],
        cwd=repo,
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.splitlines():
        if "agent-contexts" in line:
            return line.split()[-1]
    return None

def update_submodule(repo: Path) -> Tuple[bool, str]:
    """Update agent-contexts submodule in a repository"""
    submodule_path = get_submodule_path(repo)
    if not submodule_path:
        return False, "No agent-contexts submodule found"
    
    # Update the submodule
    result = subprocess.run(
        ["git", "submodule", "update", "--remote", submodule_path],
        cwd=repo,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return False, f"Update failed: {result.stderr}"
    
    # Check if there are changes
    result = subprocess.run(
        ["git", "diff", "--quiet", submodule_path],
        cwd=repo
    )
    
    if result.returncode == 0:
        return True, "Already up to date"
    
    # Commit the update
    subprocess.run(["git", "add", submodule_path], cwd=repo)
    subprocess.run(
        ["git", "commit", "-m", "chore: update agent-contexts submodule"],
        cwd=repo
    )
    
    return True, "Updated and committed"

def main():
    print("🔄 Updating agent-contexts submodules in all projects...\n")
    
    repos = find_repos_with_submodule()
    
    if not repos:
        print("No repositories with agent-contexts submodule found.")
        return
    
    print(f"Found {len(repos)} repositories with agent-contexts submodule:\n")
    
    for repo in repos:
        repo_name = f"{repo.parent.name}/{repo.name}"
        print(f"📦 {repo_name}...")
        
        success, message = update_submodule(repo)
        status = "✅" if success else "❌"
        print(f"   {status} {message}\n")
    
    print("✨ All submodules processed!")
    print("\n📝 Note: Remember to push changes in each repository:")
    print("   cd [repo] && git push")

if __name__ == "__main__":
    main()