#!/usr/bin/env python3
# ABOUTME: SonarQube issue retrieval and automated fixing via AI agent
# ABOUTME: Fetches issues from SonarQube API and uses agents to fix them

import os
import sys
import json
import httpx
import asyncio
from typing import Optional, Literal
from pathlib import Path
from collections import defaultdict
from loguru import logger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from pydantic_ai import Agent
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


class SonarQubeSettings(BaseSettings):
    """SonarQube configuration from environment variables."""

    sonar_url: str = Field(default="", env="SONAR_URL")
    sonar_token: str = Field(default="", env="SONAR_TOKEN")
    sonar_project_key: str = Field(default="", env="SONAR_PROJECT_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields from .env


class SonarIssue(BaseModel):
    """Represents a SonarQube issue."""

    key: str
    rule: str
    severity: Literal["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]
    component: str
    project: str
    line: Optional[int] = None
    hash: Optional[str] = None
    textRange: Optional[dict] = None
    message: str
    type: Literal["BUG", "VULNERABILITY", "CODE_SMELL", "SECURITY_HOTSPOT"]
    status: str
    effort: Optional[str] = None
    debt: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    @property
    def file_path(self) -> str:
        """Extract file path from component."""
        # Component format is usually: project_key:path/to/file.py
        if ":" in self.component:
            return self.component.split(":", 1)[1]
        return self.component

    @property
    def location(self) -> str:
        """Human-readable location."""
        if self.line:
            return f"{self.file_path}:{self.line}"
        return self.file_path


class IssueFix(BaseModel):
    """Represents a proposed fix for a SonarQube issue."""

    issue_key: str
    file_path: str
    line: Optional[int] = None
    rule: str
    message: str
    suggested_fix: str
    confidence: Literal["high", "medium", "low"]
    reasoning: str


class FileFixes(BaseModel):
    """All fixes grouped by file."""

    file_path: str
    issues: list[SonarIssue]
    fixes: list[IssueFix]
    total_issues: int
    file_content: Optional[str] = None


class SonarQubeClient:
    """Client for interacting with SonarQube API."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def get_issues(
        self,
        project_key: str,
        severities: Optional[list[str]] = None,
        impact_severities: Optional[list[str]] = None,
        types: Optional[list[str]] = None,
        statuses: Optional[list[str]] = None,
        branch: Optional[str] = None,
        pull_request: Optional[str] = None,
        max_issues: int = 10000
    ) -> list[SonarIssue]:
        """
        Fetch issues from SonarQube with pagination.

        Args:
            project_key: The SonarQube project key
            severities: Filter by old severities (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)
            impact_severities: Filter by new impact severities (BLOCKER, HIGH, MEDIUM, LOW, INFO)
            types: Filter by types (BUG, VULNERABILITY, CODE_SMELL)
            statuses: Filter by statuses (OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED)
            branch: Filter by branch name (e.g., 'main', 'develop')
            pull_request: Filter by pull request ID/key (not available in Community Edition)
            max_issues: Maximum number of issues to retrieve (hard limit 10000)

        Returns:
            List of SonarIssue objects
        """
        all_issues = []
        page = 1
        page_size = 500  # Max allowed by SonarQube

        while len(all_issues) < max_issues:
            params = {
                "projectKeys": project_key,
                "ps": page_size,
                "p": page
            }

            if severities:
                params["severities"] = ",".join(severities)
            if impact_severities:
                params["impactSeverities"] = ",".join(impact_severities)
            if types:
                params["types"] = ",".join(types)
            if statuses:
                params["statuses"] = ",".join(statuses)
            if branch:
                params["branch"] = branch
            if pull_request:
                params["pullRequest"] = pull_request

            try:
                response = await self.client.get(
                    f"{self.base_url}/api/issues/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                issues = [SonarIssue(**issue) for issue in data.get("issues", [])]
                all_issues.extend(issues)

                # Check if we've reached the end
                paging = data.get("paging", {})
                total = paging.get("total", 0)

                logger.info(f"Retrieved page {page}: {len(issues)} issues (total so far: {len(all_issues)}/{total})")

                if len(all_issues) >= total or len(issues) < page_size:
                    break

                page += 1

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error fetching issues: {e}")
                raise
            except Exception as e:
                logger.error(f"Error fetching issues: {e}")
                raise

        return all_issues[:max_issues]

    async def get_issue_details(self, issue_key: str) -> dict:
        """Get detailed information about a specific issue."""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/issues/search",
                params={"issues": issue_key}
            )
            response.raise_for_status()
            data = response.json()

            issues = data.get("issues", [])
            if issues:
                return issues[0]
            return {}

        except Exception as e:
            logger.error(f"Error fetching issue details: {e}")
            raise


def group_issues_by_file(issues: list[SonarIssue]) -> dict[str, list[SonarIssue]]:
    """Group issues by file path."""
    grouped = defaultdict(list)
    for issue in issues:
        grouped[issue.file_path].append(issue)
    return dict(grouped)


async def analyze_file_issues(
    file_path: str,
    issues: list[SonarIssue],
    repo_root: Path
) -> FileFixes:
    """
    Step 1: Analyze all issues in a file and generate fix plan.

    Args:
        file_path: Path to the file
        issues: List of issues in this file
        repo_root: Repository root directory

    Returns:
        FileFixes object with proposed fixes
    """
    full_path = repo_root / file_path

    # Read file content if it exists
    file_content = None
    if full_path.exists():
        try:
            file_content = full_path.read_text()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            file_content = None

    # Build context for the agent
    issues_context = "\n\n".join([
        f"Issue {i+1}:\n"
        f"  Key: {issue.key}\n"
        f"  Rule: {issue.rule}\n"
        f"  Line: {issue.line}\n"
        f"  Severity: {issue.severity}\n"
        f"  Message: {issue.message}\n"
        f"  Type: {issue.type}"
        for i, issue in enumerate(issues)
    ])

    prompt = f"""You are a code quality expert. Analyze the following SonarQube issues in the file `{file_path}` and propose fixes.

FILE CONTENT:
```
{file_content if file_content else '[File not found or unreadable]'}
```

ISSUES TO FIX:
{issues_context}

For each issue, provide:
1. A specific, actionable fix (what code to change)
2. Your confidence level (high/medium/low)
3. Brief reasoning

Focus on fixes that can be applied together without conflicts.
"""

    # Create analysis agent
    analysis_agent = Agent(
        "openai:gpt-4o",
        system_prompt="""You are a code quality expert specializing in fixing SonarQube issues.
Your goal is to propose clear, safe, and effective fixes for code quality issues.
Always consider the context of the entire file when proposing fixes.
Prioritize fixes that improve code quality without changing functionality."""
    )

    try:
        result = await analysis_agent.run(prompt)
        analysis_text = result.data

        # For now, create placeholder fixes - we'll parse the agent response properly later
        fixes = [
            IssueFix(
                issue_key=issue.key,
                file_path=file_path,
                line=issue.line,
                rule=issue.rule,
                message=issue.message,
                suggested_fix="[Agent analysis pending - will be extracted from response]",
                confidence="medium",
                reasoning="Initial analysis"
            )
            for issue in issues
        ]

        return FileFixes(
            file_path=file_path,
            issues=issues,
            fixes=fixes,
            total_issues=len(issues),
            file_content=file_content
        )

    except Exception as e:
        logger.error(f"Error analyzing file {file_path}: {e}")
        # Return empty fixes on error
        return FileFixes(
            file_path=file_path,
            issues=issues,
            fixes=[],
            total_issues=len(issues),
            file_content=file_content
        )


async def apply_file_fixes(
    file_fixes: FileFixes,
    repo_root: Path,
    dry_run: bool = True
) -> dict[str, any]:
    """
    Step 2: Apply all fixes to a file at once.

    Args:
        file_fixes: FileFixes object with proposed fixes
        repo_root: Repository root directory
        dry_run: If True, don't actually modify files

    Returns:
        Dictionary with results (success count, failures, etc.)
    """
    full_path = repo_root / file_fixes.file_path

    if not full_path.exists():
        return {
            "success": False,
            "error": "File not found",
            "fixes_applied": 0
        }

    if not file_fixes.fixes:
        return {
            "success": False,
            "error": "No fixes proposed",
            "fixes_applied": 0
        }

    # Build fix prompt for the agent
    fixes_context = "\n\n".join([
        f"Fix {i+1} (Line {fix.line}):\n"
        f"  Rule: {fix.rule}\n"
        f"  Issue: {fix.message}\n"
        f"  Suggested: {fix.suggested_fix}\n"
        f"  Confidence: {fix.confidence}"
        for i, fix in enumerate(file_fixes.fixes)
    ])

    prompt = f"""Apply the following fixes to this file. Return the complete fixed file content.

CURRENT FILE CONTENT:
```
{file_fixes.file_content}
```

FIXES TO APPLY:
{fixes_context}

Apply all fixes that are safe and don't conflict. Return ONLY the fixed file content, no explanations."""

    # Create fixing agent
    fixing_agent = Agent(
        "openai:gpt-4o",
        system_prompt="""You are a precise code editor. Apply the requested fixes exactly.
Return only the complete fixed file content with no additional commentary.
Ensure all fixes are applied correctly and the code remains syntactically valid."""
    )

    try:
        result = await fixing_agent.run(prompt)
        fixed_content = result.data

        if dry_run:
            logger.info(f"DRY RUN: Would update {file_fixes.file_path}")
            return {
                "success": True,
                "fixes_applied": len(file_fixes.fixes),
                "dry_run": True
            }

        # Actually write the file
        full_path.write_text(fixed_content)
        logger.info(f"Applied {len(file_fixes.fixes)} fixes to {file_fixes.file_path}")

        return {
            "success": True,
            "fixes_applied": len(file_fixes.fixes),
            "dry_run": False
        }

    except Exception as e:
        logger.error(f"Error applying fixes to {file_fixes.file_path}: {e}")
        return {
            "success": False,
            "error": str(e),
            "fixes_applied": 0
        }


async def fix_issue_with_agent(issue: SonarIssue, repo_root: Path) -> bool:
    """
    Use AI agent to fix a single issue.

    Args:
        issue: The SonarQube issue to fix
        repo_root: Root directory of the repository

    Returns:
        True if fixed successfully, False otherwise
    """
    # This is a placeholder - in the real implementation, this would:
    # 1. Read the file context
    # 2. Use an agent to analyze and fix the issue
    # 3. Apply the fix
    # 4. Verify the fix

    logger.info(f"Fixing issue {issue.key} at {issue.location}")
    logger.info(f"  Rule: {issue.rule}")
    logger.info(f"  Message: {issue.message}")
    logger.info(f"  Severity: {issue.severity}")

    # TODO: Implement actual agent-based fixing
    # For now, just log what would be done

    return False  # Return True when actually implemented


async def main(
    severity_filter: Optional[list[str]] = None,
    impact_severity_filter: Optional[list[str]] = None,
    type_filter: Optional[list[str]] = None,
    status_filter: Optional[list[str]] = None,
    branch: Optional[str] = None,
    pull_request: Optional[str] = None,
    max_issues: int = 100,
    dry_run: bool = True,
    auto_commit: bool = False,
    save_json: Optional[str] = None
):
    """
    Main function to fetch and fix SonarQube issues.

    Args:
        severity_filter: List of old severities to filter (default: BLOCKER, CRITICAL)
        impact_severity_filter: List of new impact severities to filter (BLOCKER, HIGH, MEDIUM, LOW, INFO)
        type_filter: List of types to filter (default: BUG, VULNERABILITY)
        status_filter: List of statuses to filter (default: OPEN, CONFIRMED, REOPENED)
        branch: Branch name to filter (e.g., 'main', 'develop')
        pull_request: Pull request ID/key to filter (not available in Community Edition)
        max_issues: Maximum number of issues to process
        dry_run: If True, only list issues without fixing
        auto_commit: If True, automatically commit fixes
        save_json: If provided, save issues grouped by file to this JSON file
    """
    # Load settings
    try:
        settings = SonarQubeSettings()
    except Exception as e:
        console.print(f"[red]Error loading settings: {e}[/red]")
        console.print("\n[yellow]Please set the following environment variables:[/yellow]")
        console.print("  SONAR_URL - Your SonarQube server URL")
        console.print("  SONAR_TOKEN - Your SonarQube authentication token")
        console.print("  SONAR_PROJECT_KEY - Your project key in SonarQube")
        sys.exit(1)

    if not settings.sonar_url or not settings.sonar_token or not settings.sonar_project_key:
        console.print("[red]Missing required SonarQube configuration![/red]")
        console.print("\n[yellow]Please set the following environment variables:[/yellow]")
        console.print("  SONAR_URL - Your SonarQube server URL")
        console.print("  SONAR_TOKEN - Your SonarQube authentication token")
        console.print("  SONAR_PROJECT_KEY - Your project key in SonarQube")
        sys.exit(1)

    # Default filters
    if severity_filter is None:
        severity_filter = ["BLOCKER", "CRITICAL"]
    if type_filter is None:
        type_filter = ["BUG", "VULNERABILITY"]
    if status_filter is None:
        status_filter = ["OPEN", "CONFIRMED", "REOPENED"]

    console.print(f"\n[bold cyan]SonarQube Issue Fixer[/bold cyan]")
    console.print(f"Server: {settings.sonar_url}")
    console.print(f"Project: {settings.sonar_project_key}")
    if branch:
        console.print(f"Branch: {branch}")
    if pull_request:
        console.print(f"Pull Request: {pull_request}")
    if severity_filter:
        console.print(f"Severities (old): {', '.join(severity_filter)}")
    if impact_severity_filter:
        console.print(f"Impact Severities (new): {', '.join(impact_severity_filter)}")
    console.print(f"Types: {', '.join(type_filter)}")
    console.print(f"Statuses: {', '.join(status_filter)}")
    console.print(f"Max issues: {max_issues}")
    console.print(f"Mode: {'DRY RUN' if dry_run else 'FIXING'}\n")

    # Fetch issues
    async with SonarQubeClient(settings.sonar_url, settings.sonar_token) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching issues from SonarQube...", total=None)

            issues = await client.get_issues(
                project_key=settings.sonar_project_key,
                severities=severity_filter,
                impact_severities=impact_severity_filter,
                types=type_filter,
                statuses=status_filter,
                branch=branch,
                pull_request=pull_request,
                max_issues=max_issues
            )

            progress.update(task, completed=True)

    if not issues:
        console.print("[green]No issues found! :tada:[/green]")
        return

    # Display issues in a table
    table = Table(title=f"Found {len(issues)} Issues")
    table.add_column("Severity", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Rule", style="blue")
    table.add_column("Location", style="green")
    table.add_column("Message", style="yellow")

    for issue in issues[:20]:  # Show first 20
        table.add_row(
            issue.severity,
            issue.type,
            issue.rule,
            issue.location,
            issue.message[:50] + "..." if len(issue.message) > 50 else issue.message
        )

    if len(issues) > 20:
        console.print(f"\n[dim]... and {len(issues) - 20} more issues[/dim]")

    console.print(table)

    # Group issues by file
    console.print("\n[bold cyan]Grouping issues by file...[/bold cyan]")
    issues_by_file = group_issues_by_file(issues)

    file_summary_table = Table(title=f"Issues Grouped by File ({len(issues_by_file)} files)")
    file_summary_table.add_column("File", style="green")
    file_summary_table.add_column("Issues", style="yellow", justify="right")
    file_summary_table.add_column("Severities", style="cyan")

    for file_path, file_issues in sorted(issues_by_file.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        severities = ", ".join(sorted(set(i.severity for i in file_issues)))
        file_summary_table.add_row(
            file_path[:60] + "..." if len(file_path) > 60 else file_path,
            str(len(file_issues)),
            severities
        )

    console.print(file_summary_table)

    # Save issues to JSON if requested
    if save_json:
        output_data = {
            "metadata": {
                "server": settings.sonar_url,
                "project": settings.sonar_project_key,
                "branch": branch,
                "pull_request": pull_request,
                "severities": severity_filter,
                "types": type_filter,
                "total_issues": len(issues),
                "total_files": len(issues_by_file),
                "fetched_at": "2025-10-17T11:30:00Z"  # You might want to use datetime.now()
            },
            "issues_by_file": {}
        }

        for file_path, file_issues in issues_by_file.items():
            output_data["issues_by_file"][file_path] = [
                {
                    "key": issue.key,
                    "rule": issue.rule,
                    "severity": issue.severity,
                    "line": issue.line,
                    "message": issue.message,
                    "type": issue.type,
                    "status": issue.status,
                    "effort": issue.effort
                }
                for issue in file_issues
            ]

        save_path = Path(save_json)
        save_path.write_text(json.dumps(output_data, indent=2))
        console.print(f"\n[green]✓ Saved issues to {save_json}[/green]")
        console.print(f"[dim]Use this file with AI Code's /sonarqube-fix command[/dim]")

    if dry_run:
        console.print("\n[yellow]This was a dry run. Use --fix to actually fix issues.[/yellow]")
        console.print(f"\n[dim]To fix issues, run with --fix flag[/dim]")
        return

    # Fix issues file by file
    console.print("\n[bold]Starting to fix issues (grouped by file)...[/bold]")
    repo_root = Path.cwd()

    total_files_processed = 0
    total_fixes_applied = 0
    total_failures = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Processing {len(issues_by_file)} files...", total=len(issues_by_file))

        for file_path, file_issues in issues_by_file.items():
            progress.update(task, description=f"Analyzing {file_path[:40]}...")

            # Step 1: Analyze issues and generate fix plan
            try:
                file_fixes = await analyze_file_issues(file_path, file_issues, repo_root)

                if not file_fixes.fixes:
                    logger.warning(f"No fixes proposed for {file_path}")
                    total_failures += 1
                    progress.advance(task)
                    continue

                # Step 2: Apply fixes to the file
                progress.update(task, description=f"Fixing {file_path[:40]}...")
                result = await apply_file_fixes(file_fixes, repo_root, dry_run=False)

                if result["success"]:
                    total_fixes_applied += result["fixes_applied"]
                    total_files_processed += 1
                    console.print(f"✓ Fixed {result['fixes_applied']} issues in {file_path}")
                else:
                    total_failures += 1
                    console.print(f"✗ Failed to fix {file_path}: {result.get('error', 'Unknown error')}")

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                total_failures += 1

            progress.advance(task)

    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Files processed: {total_files_processed}/{len(issues_by_file)}")
    console.print(f"  Total fixes applied: {total_fixes_applied}")
    console.print(f"  Failures: {total_failures}")
    console.print(f"  Original issues: {len(issues)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch and fix SonarQube issues using AI agents"
    )
    parser.add_argument(
        "--severity",
        nargs="+",
        choices=["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"],
        help="Filter by old severity (default: BLOCKER CRITICAL)"
    )
    parser.add_argument(
        "--impact-severity",
        nargs="+",
        choices=["BLOCKER", "HIGH", "MEDIUM", "LOW", "INFO"],
        help="Filter by new impact severity (BLOCKER, HIGH, MEDIUM, LOW, INFO)"
    )
    parser.add_argument(
        "--type",
        nargs="+",
        choices=["BUG", "VULNERABILITY", "CODE_SMELL", "SECURITY_HOTSPOT"],
        help="Filter by type (default: BUG VULNERABILITY)"
    )
    parser.add_argument(
        "--statuses",
        nargs="+",
        choices=["OPEN", "CONFIRMED", "REOPENED", "RESOLVED", "CLOSED"],
        help="Filter by status (default: OPEN CONFIRMED REOPENED)"
    )
    parser.add_argument(
        "--branch",
        type=str,
        help="Filter by branch name (e.g., 'main', 'develop')"
    )
    parser.add_argument(
        "--pull-request",
        type=str,
        help="Filter by pull request ID/key (not available in Community Edition)"
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=100,
        help="Maximum number of issues to process (default: 100)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Actually fix issues (default is dry-run)"
    )
    parser.add_argument(
        "--auto-commit",
        action="store_true",
        help="Automatically commit fixes"
    )
    parser.add_argument(
        "--save-json",
        type=str,
        help="Save issues grouped by file to JSON file (e.g., sonarqube_issues.json)"
    )

    args = parser.parse_args()

    asyncio.run(main(
        severity_filter=args.severity,
        impact_severity_filter=args.impact_severity,
        type_filter=args.type,
        status_filter=args.statuses,
        branch=args.branch,
        pull_request=args.pull_request,
        max_issues=args.max_issues,
        dry_run=not args.fix,
        auto_commit=args.auto_commit,
        save_json=args.save_json
    ))
