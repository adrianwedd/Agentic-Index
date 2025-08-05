#!/usr/bin/env python3
"""
CI Status Monitor - Comprehensive CI/CD pipeline health monitoring
Generates beautiful visualizations and detailed failure analysis
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse


@dataclass
class CIRun:
    """Represents a single CI run with all relevant metadata."""

    workflow: str
    name: str
    conclusion: str
    status: str
    url: str
    created_at: str
    run_id: str

    @property
    def is_failure(self) -> bool:
        return self.conclusion == "failure"

    @property
    def is_success(self) -> bool:
        return self.conclusion == "success"

    @property
    def age_hours(self) -> float:
        """Hours since this run was created."""
        created = datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
        return (datetime.now().astimezone() - created).total_seconds() / 3600


@dataclass
class WorkflowHealth:
    """Health metrics for a specific workflow."""

    name: str
    total_runs: int
    failures: int
    successes: int
    latest_run: Optional[CIRun]
    failure_rate: float
    trend: str  # "improving", "stable", "degrading"
    critical_issues: List[str]

    @property
    def status_emoji(self) -> str:
        if self.failure_rate == 0:
            return "✅"
        elif self.failure_rate < 0.2:
            return "🟡"
        elif self.failure_rate < 0.5:
            return "🟠"
        else:
            return "❌"


class CIStatusMonitor:
    """Monitors CI/CD pipeline health and generates comprehensive reports."""

    def __init__(self, repo: str = None):
        self.repo = repo or self._detect_repo()
        self.runs: List[CIRun] = []
        self.workflows: Dict[str, WorkflowHealth] = {}

    def _detect_repo(self) -> str:
        """Auto-detect repository from git remote."""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True,
            )
            url = result.stdout.strip()
            if url.startswith("git@github.com:"):
                return url.replace("git@github.com:", "").replace(".git", "")
            elif "github.com/" in url:
                parsed = urlparse(url)
                return parsed.path.strip("/").replace(".git", "")
            return url
        except subprocess.CalledProcessError:
            return "unknown/repo"

    def fetch_ci_runs(self, limit: int = 50) -> None:
        """Fetch recent CI runs using GitHub CLI."""
        try:
            cmd = [
                "gh",
                "run",
                "list",
                "--limit",
                str(limit),
                "--json",
                "status,conclusion,name,workflowName,url,createdAt,databaseId",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            self.runs = [
                CIRun(
                    workflow=run["workflowName"],
                    name=run["name"],
                    conclusion=run.get("conclusion", "unknown"),
                    status=run["status"],
                    url=run["url"],
                    created_at=run["createdAt"],
                    run_id=str(run["databaseId"]),
                )
                for run in data
                if run["status"] == "completed"
            ]

        except subprocess.CalledProcessError as e:
            print(f"Error fetching CI runs: {e}")
            sys.exit(1)

    def analyze_workflow_health(self) -> None:
        """Analyze health metrics for each workflow."""
        workflow_runs = {}

        # Group runs by workflow
        for run in self.runs:
            if run.workflow not in workflow_runs:
                workflow_runs[run.workflow] = []
            workflow_runs[run.workflow].append(run)

        # Calculate health metrics for each workflow
        for workflow_name, runs in workflow_runs.items():
            total = len(runs)
            failures = sum(1 for r in runs if r.is_failure)
            successes = sum(1 for r in runs if r.is_success)
            failure_rate = failures / total if total > 0 else 0

            # Determine trend (last 5 vs previous 5 runs)
            recent_runs = runs[:5]
            older_runs = runs[5:10] if len(runs) > 5 else []

            recent_failure_rate = (
                sum(1 for r in recent_runs if r.is_failure) / len(recent_runs)
                if recent_runs
                else 0
            )
            older_failure_rate = (
                sum(1 for r in older_runs if r.is_failure) / len(older_runs)
                if older_runs
                else 0
            )

            if recent_failure_rate < older_failure_rate - 0.1:
                trend = "improving"
            elif recent_failure_rate > older_failure_rate + 0.1:
                trend = "degrading"
            else:
                trend = "stable"

            # Identify critical issues
            critical_issues = []
            if failure_rate > 0.5:
                critical_issues.append("High failure rate (>50%)")
            if runs[0].is_failure and runs[0].age_hours < 24:
                critical_issues.append("Recent failure in last 24h")
            if all(r.is_failure for r in runs[:3]) and len(runs) >= 3:
                critical_issues.append("3+ consecutive failures")

            self.workflows[workflow_name] = WorkflowHealth(
                name=workflow_name,
                total_runs=total,
                failures=failures,
                successes=successes,
                latest_run=runs[0] if runs else None,
                failure_rate=failure_rate,
                trend=trend,
                critical_issues=critical_issues,
            )

    def get_failure_details(self, run_id: str) -> Dict[str, str]:
        """Get detailed failure information for a specific run."""
        try:
            cmd = ["gh", "run", "view", run_id, "--log"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Extract key failure indicators
            log_lines = result.stdout.split("\n")
            errors = []
            context = []

            for i, line in enumerate(log_lines):
                if any(
                    keyword in line.lower()
                    for keyword in ["error", "failed", "exception"]
                ):
                    # Get context around error
                    start = max(0, i - 2)
                    end = min(len(log_lines), i + 3)
                    context_block = "\n".join(log_lines[start:end])
                    errors.append(context_block)

            return {
                "run_id": run_id,
                "error_count": len(errors),
                "errors": errors[:5],  # Limit to first 5 errors
                "summary": self._summarize_failure(errors),
            }

        except subprocess.CalledProcessError:
            return {"run_id": run_id, "error": "Could not fetch failure details"}

    def _summarize_failure(self, errors: List[str]) -> str:
        """Generate a human-readable failure summary."""
        if not errors:
            return "No specific error details found"

        # Common failure patterns
        patterns = {
            "dependency": [
                "modulenotfounderror",
                "importerror",
                "pip install",
                "npm install",
            ],
            "test": ["test failed", "assertion", "pytest", "failed test"],
            "build": ["build failed", "compilation error", "make failed"],
            "auth": ["authentication", "permission denied", "unauthorized"],
            "network": ["connection refused", "timeout", "dns resolution"],
            "env": ["environment variable", "missing env", "config"],
        }

        error_text = " ".join(errors).lower()

        for category, keywords in patterns.items():
            if any(keyword in error_text for keyword in keywords):
                return f"Likely {category} issue detected"

        return "Generic failure - check logs for details"

    def generate_dashboard_html(self, output_path: Path) -> None:
        """Generate a beautiful HTML dashboard."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Pipeline Dashboard - {self.repo}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .dashboard {{
            max-width: 1200px; margin: 0 auto;
            background: white; border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        .header {{
            text-align: center; margin-bottom: 40px;
            border-bottom: 2px solid #f0f0f0; padding-bottom: 20px;
        }}
        .header h1 {{
            color: #2d3748; margin: 0;
            font-size: 2.5em; font-weight: 700;
        }}
        .header p {{
            color: #718096; margin: 10px 0 0 0;
            font-size: 1.1em;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin-bottom: 40px;
        }}
        .metric-card {{
            background: #f7fafc; padding: 20px;
            border-radius: 8px; border-left: 4px solid #4299e1;
        }}
        .metric-card h3 {{
            margin: 0 0 10px 0; color: #2d3748;
            font-size: 1.1em; font-weight: 600;
        }}
        .metric-value {{
            font-size: 2em; font-weight: 700;
            color: #4299e1; margin: 0;
        }}
        .workflows {{
            display: grid; gap: 20px;
        }}
        .workflow-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px; padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .workflow-header {{
            display: flex; justify-content: space-between;
            align-items: center; margin-bottom: 15px;
        }}
        .workflow-name {{
            font-size: 1.3em; font-weight: 600;
            color: #2d3748; margin: 0;
        }}
        .status-badge {{
            padding: 4px 12px; border-radius: 12px;
            font-size: 0.8em; font-weight: 500;
            text-transform: uppercase;
        }}
        .success {{ background: #c6f6d5; color: #22543d; }}
        .failure {{ background: #fed7d7; color: #742a2a; }}
        .degrading {{ background: #feebc8; color: #744210; }}
        .improving {{ background: #bee3f8; color: #2a4365; }}
        .stable {{ background: #e2e8f0; color: #4a5568; }}
        .workflow-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px; margin: 15px 0;
        }}
        .stat {{
            text-align: center; padding: 10px;
            background: #f7fafc; border-radius: 6px;
        }}
        .stat-value {{
            font-size: 1.4em; font-weight: 600;
            color: #2d3748; margin: 0;
        }}
        .stat-label {{
            font-size: 0.8em; color: #718096;
            margin: 5px 0 0 0; text-transform: uppercase;
        }}
        .critical-issues {{
            background: #fed7d7; border-left: 4px solid #e53e3e;
            padding: 15px; border-radius: 4px; margin-top: 15px;
        }}
        .critical-issues h4 {{
            color: #742a2a; margin: 0 0 10px 0;
            font-size: 1em;
        }}
        .critical-issues ul {{
            color: #742a2a; margin: 0; padding-left: 20px;
        }}
        .timestamp {{
            text-align: center; margin-top: 40px;
            color: #718096; font-size: 0.9em;
        }}
        .trend-arrow {{
            font-size: 1.2em; margin-left: 5px;
        }}
        .trend-improving {{ color: #38a169; }}
        .trend-degrading {{ color: #e53e3e; }}
        .trend-stable {{ color: #718096; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 CI/CD Pipeline Dashboard</h1>
            <p>Repository: <strong>{self.repo}</strong></p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Total Workflows</h3>
                <p class="metric-value">{len(self.workflows)}</p>
            </div>
            <div class="metric-card">
                <h3>Healthy Workflows</h3>
                <p class="metric-value">{sum(1 for w in self.workflows.values() if w.failure_rate < 0.2)}</p>
            </div>
            <div class="metric-card">
                <h3>Critical Issues</h3>
                <p class="metric-value">{sum(len(w.critical_issues) for w in self.workflows.values())}</p>
            </div>
            <div class="metric-card">
                <h3>Recent Runs</h3>
                <p class="metric-value">{len(self.runs)}</p>
            </div>
        </div>
        
        <div class="workflows">
            {self._generate_workflow_cards()}
        </div>
        
        <div class="timestamp">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        </div>
    </div>
</body>
</html>
"""

        output_path.write_text(html_content)
        print(f"✅ Dashboard generated: {output_path}")

    def _generate_workflow_cards(self) -> str:
        """Generate HTML cards for each workflow."""
        cards = []

        # Sort workflows by priority (failures first, then by failure rate)
        sorted_workflows = sorted(
            self.workflows.values(),
            key=lambda w: (len(w.critical_issues) == 0, w.failure_rate, w.name),
        )

        for workflow in sorted_workflows:
            latest_status = (
                "success"
                if workflow.latest_run and workflow.latest_run.is_success
                else "failure"
            )

            trend_class = f"trend-{workflow.trend}"
            trend_arrow = {"improving": "📈", "degrading": "📉", "stable": "➡️"}[
                workflow.trend
            ]

            stats_html = f"""
            <div class="workflow-stats">
                <div class="stat">
                    <p class="stat-value">{workflow.total_runs}</p>
                    <p class="stat-label">Total Runs</p>
                </div>
                <div class="stat">
                    <p class="stat-value">{workflow.successes}</p>
                    <p class="stat-label">Successes</p>
                </div>
                <div class="stat">
                    <p class="stat-value">{workflow.failures}</p>
                    <p class="stat-label">Failures</p>
                </div>
                <div class="stat">
                    <p class="stat-value">{workflow.failure_rate:.1%}</p>
                    <p class="stat-label">Failure Rate</p>
                </div>
            </div>
            """

            critical_issues_html = ""
            if workflow.critical_issues:
                issues_list = "".join(
                    f"<li>{issue}</li>" for issue in workflow.critical_issues
                )
                critical_issues_html = f"""
                <div class="critical-issues">
                    <h4>🚨 Critical Issues</h4>
                    <ul>{issues_list}</ul>
                </div>
                """

            card = f"""
            <div class="workflow-card">
                <div class="workflow-header">
                    <h3 class="workflow-name">
                        {workflow.status_emoji} {workflow.name}
                    </h3>
                    <div>
                        <span class="status-badge {latest_status}">{latest_status}</span>
                        <span class="status-badge {workflow.trend}">
                            {workflow.trend}
                            <span class="trend-arrow {trend_class}">{trend_arrow}</span>
                        </span>
                    </div>
                </div>
                {stats_html}
                {critical_issues_html}
            </div>
            """
            cards.append(card)

        return "".join(cards)

    def generate_json_report(self, output_path: Path) -> None:
        """Generate a machine-readable JSON report."""
        report = {
            "repository": self.repo,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_workflows": len(self.workflows),
                "healthy_workflows": sum(
                    1 for w in self.workflows.values() if w.failure_rate < 0.2
                ),
                "total_critical_issues": sum(
                    len(w.critical_issues) for w in self.workflows.values()
                ),
                "recent_runs": len(self.runs),
            },
            "workflows": {
                name: {
                    "total_runs": w.total_runs,
                    "failures": w.failures,
                    "successes": w.successes,
                    "failure_rate": w.failure_rate,
                    "trend": w.trend,
                    "critical_issues": w.critical_issues,
                    "latest_run": (
                        {
                            "conclusion": w.latest_run.conclusion,
                            "url": w.latest_run.url,
                            "created_at": w.latest_run.created_at,
                            "age_hours": w.latest_run.age_hours,
                        }
                        if w.latest_run
                        else None
                    ),
                }
                for name, w in self.workflows.items()
            },
        }

        output_path.write_text(json.dumps(report, indent=2))
        print(f"✅ JSON report generated: {output_path}")

    def print_console_summary(self) -> None:
        """Print a beautiful console summary."""
        print(f"\n🚀 CI/CD Pipeline Health Report - {self.repo}")
        print("=" * 60)

        # Overall metrics
        healthy = sum(1 for w in self.workflows.values() if w.failure_rate < 0.2)
        critical = sum(len(w.critical_issues) for w in self.workflows.values())

        print(f"📊 Total Workflows: {len(self.workflows)}")
        print(f"✅ Healthy: {healthy} ({healthy/len(self.workflows):.1%})")
        print(f"🚨 Critical Issues: {critical}")
        print(f"📈 Recent Runs Analyzed: {len(self.runs)}")

        print("\n📋 Workflow Details:")
        print("-" * 60)

        # Sort by priority (critical issues first)
        sorted_workflows = sorted(
            self.workflows.values(),
            key=lambda w: (len(w.critical_issues) == 0, w.failure_rate, w.name),
        )

        for workflow in sorted_workflows:
            status = workflow.status_emoji
            trend_emoji = {"improving": "📈", "degrading": "📉", "stable": "➡️"}[
                workflow.trend
            ]

            print(
                f"{status} {workflow.name:<30} "
                f"| {workflow.failure_rate:>6.1%} failure rate "
                f"| {workflow.trend} {trend_emoji}"
            )

            if workflow.critical_issues:
                for issue in workflow.critical_issues:
                    print(f"   🚨 {issue}")

        print(
            f"\n⏰ Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="CI/CD Pipeline Health Monitor")
    parser.add_argument("--repo", help="Repository (owner/name)")
    parser.add_argument(
        "--limit", type=int, default=100, help="Number of runs to analyze"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("."), help="Output directory"
    )
    parser.add_argument(
        "--format",
        choices=["console", "html", "json", "all"],
        default="console",
        help="Output format",
    )

    args = parser.parse_args()

    monitor = CIStatusMonitor(args.repo)

    print(f"🔍 Fetching CI runs for {monitor.repo}...")
    monitor.fetch_ci_runs(args.limit)

    print("📊 Analyzing workflow health...")
    monitor.analyze_workflow_health()

    if args.format in ["console", "all"]:
        monitor.print_console_summary()

    if args.format in ["html", "all"]:
        html_path = args.output_dir / "ci_dashboard.html"
        monitor.generate_dashboard_html(html_path)

    if args.format in ["json", "all"]:
        json_path = args.output_dir / "ci_report.json"
        monitor.generate_json_report(json_path)


if __name__ == "__main__":
    main()
