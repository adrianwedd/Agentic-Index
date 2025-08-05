#!/usr/bin/env python3
"""
Automated CI Issue Creator - Creates GitHub issues for critical CI failures
Integrates with the CI Status Monitor to provide actionable failure reporting
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class CIIssueCreator:
    """Creates and manages GitHub issues for CI failures."""

    def __init__(self, ci_report_path: Path):
        self.ci_report_path = ci_report_path
        self.report = self._load_report()

    def _load_report(self) -> Dict:
        """Load CI health report."""
        try:
            with open(self.ci_report_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ CI report not found at {self.ci_report_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {self.ci_report_path}")
            sys.exit(1)

    def get_critical_workflows(self) -> List[tuple]:
        """Get workflows that need immediate attention."""
        critical = []

        for name, workflow in self.report["workflows"].items():
            # Define critical criteria
            is_critical = workflow["critical_issues"] and (
                workflow["failure_rate"] > 0.8  # >80% failure rate
                or "Recent failure in last 24h" in workflow["critical_issues"]
                or "3+ consecutive failures" in workflow["critical_issues"]
            )

            if is_critical:
                critical.append((name, workflow))

        # Sort by severity (most issues first, then highest failure rate)
        critical.sort(
            key=lambda x: (len(x[1]["critical_issues"]), x[1]["failure_rate"]),
            reverse=True,
        )

        return critical

    def issue_exists(self, workflow_name: str) -> bool:
        """Check if an issue already exists for this workflow."""
        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "list",
                    "--search",
                    f"CI Failure: {workflow_name}",
                    "--state",
                    "open",
                    "--json",
                    "title,number",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            issues = json.loads(result.stdout)
            if issues:
                print(
                    f"📝 Issue already exists for {workflow_name}: #{issues[0]['number']}"
                )
                return True
            return False

        except subprocess.CalledProcessError:
            return False

    def get_failure_analysis(self, workflow_name: str, workflow: Dict) -> str:
        """Generate detailed failure analysis."""
        analysis = []

        # Basic stats
        analysis.append(
            f"**Failure Rate:** {workflow['failure_rate']:.1%} ({workflow['failures']}/{workflow['total_runs']} recent runs)"
        )
        analysis.append(
            f"**Trend:** {workflow['trend']} {'📉' if workflow['trend'] == 'degrading' else '📈' if workflow['trend'] == 'improving' else '➡️'}"
        )

        # Latest run info
        if workflow["latest_run"]:
            latest = workflow["latest_run"]
            analysis.append(
                f"**Latest Run:** [{latest['conclusion']}]({latest['url']}) ({latest['age_hours']:.1f}h ago)"
            )

        # Critical issues
        if workflow["critical_issues"]:
            analysis.append("\n### 🚨 Critical Issues:")
            for issue in workflow["critical_issues"]:
                analysis.append(f"- {issue}")

        # Recommended actions
        analysis.append("\n### 🛠️ Recommended Actions:")

        if workflow["failure_rate"] > 0.9:
            analysis.append(
                "- 🔥 **URGENT**: Workflow is completely broken - immediate attention required"
            )
        elif "Recent failure in last 24h" in workflow["critical_issues"]:
            analysis.append("- ⏰ **Priority**: Recent failure indicates fresh issue")

        if "3+ consecutive failures" in workflow["critical_issues"]:
            analysis.append(
                "- 🔄 **Pattern**: Multiple consecutive failures suggest systematic issue"
            )

        # Common troubleshooting steps
        analysis.extend(
            [
                "- 📋 Review the [CI Dashboard](../../web/ci_dashboard.html) for patterns",
                "- 🔍 Check recent code changes that might have introduced the issue",
                "- 🧪 Test the workflow locally if possible",
                "- 📊 Compare with similar successful workflows",
            ]
        )

        # Workflow-specific guidance
        workflow_guides = {
            "Update index": [
                "- 🔧 Check data pipeline dependencies and API rate limits",
                "- 📊 Verify repository scoring and ranking logic",
            ],
            "Daily README Injection": [
                "- 📝 Check README.md markers and injection logic",
                "- 🔄 Verify data sources are accessible",
            ],
            "FOSSA Scan": [
                "- 🔐 Verify FOSSA API credentials and permissions",
                "- 📦 Check for new dependencies that might trigger scan issues",
            ],
            "Snyk Scan": [
                "- 🛡️ Check Snyk API credentials and project configuration",
                "- 🔍 Review for new security vulnerabilities in dependencies",
            ],
        }

        if workflow_name in workflow_guides:
            analysis.extend(workflow_guides[workflow_name])

        return "\n".join(analysis)

    def create_issue(self, workflow_name: str, workflow: Dict) -> bool:
        """Create a GitHub issue for the workflow failure."""

        # Determine priority and labels
        priority = "critical" if workflow["failure_rate"] > 0.9 else "high"
        labels = ["bug", "ci", f"priority-{priority}"]

        # Add specific labels based on workflow type
        workflow_labels = {
            "Update index": ["data-pipeline"],
            "Daily README Injection": ["documentation"],
            "FOSSA Scan": ["security", "dependencies"],
            "Snyk Scan": ["security", "dependencies"],
            "Metrics Monitor": ["monitoring"],
            "CI": ["meta"],
        }

        if workflow_name in workflow_labels:
            labels.extend(workflow_labels[workflow_name])

        title = f"CI Failure: {workflow_name} - {workflow['failure_rate']:.1%} failure rate ({priority})"

        body = f"""## 🚨 Critical CI/CD Failure Detected

{self.get_failure_analysis(workflow_name, workflow)}

### 📈 Metrics
- **Repository:** {self.report['repository']}
- **Total Workflows:** {self.report['summary']['total_workflows']}
- **Healthy Workflows:** {self.report['summary']['healthy_workflows']}
- **Total Critical Issues:** {self.report['summary']['total_critical_issues']}

### 📊 Resources
- [🔍 Full CI Dashboard](../../web/ci_dashboard.html)
- [📄 JSON Report](../../web/ci_report.json)
- [📈 Workflow Trends](../../web/ci_status.md)

### 🤖 Automation
This issue was automatically created by the CI Health Monitor.
- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Report Time:** {self.report['generated_at']}

**Note:** This issue will be automatically updated as the workflow health improves.

---
*To prevent future automatic issues for this workflow, fix the underlying issues or add `skip-ci-issues` label.*
"""

        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "create",
                    "--title",
                    title,
                    "--body",
                    body,
                    "--label",
                    ",".join(labels),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            # Extract issue number from output
            issue_url = result.stdout.strip()
            issue_number = issue_url.split("/")[-1]

            print(f"✅ Created issue #{issue_number} for {workflow_name}")
            print(f"   URL: {issue_url}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create issue for {workflow_name}")
            print(f"   Error: {e.stderr}")
            return False

    def update_existing_issue(self, workflow_name: str, workflow: Dict) -> None:
        """Update existing issue with latest status."""
        # This could be implemented to update existing issues
        # with current status, but for now we'll skip duplicates
        pass

    def run(self, dry_run: bool = False, max_issues: int = 5) -> None:
        """Main execution - create issues for critical workflows."""
        critical_workflows = self.get_critical_workflows()

        if not critical_workflows:
            print("✅ No critical CI issues found!")
            return

        print(f"🔍 Found {len(critical_workflows)} workflows with critical issues")

        if dry_run:
            print("\n🧪 DRY RUN - Would create issues for:")
            for workflow_name, workflow in critical_workflows[:max_issues]:
                print(
                    f"  - {workflow_name} ({workflow['failure_rate']:.1%} failure rate)"
                )
            return

        created_count = 0
        skipped_count = 0

        for workflow_name, workflow in critical_workflows[:max_issues]:
            if self.issue_exists(workflow_name):
                skipped_count += 1
                continue

            if self.create_issue(workflow_name, workflow):
                created_count += 1

            # Rate limiting - don't spam too many issues at once
            if created_count >= 3:
                print(
                    f"⚠️  Rate limit: Created {created_count} issues, stopping to avoid spam"
                )
                break

        print(f"\n📊 Summary:")
        print(f"  ✅ Created: {created_count} issues")
        print(f"  ⏭️  Skipped: {skipped_count} (already exist)")
        print(f"  🔍 Total critical workflows: {len(critical_workflows)}")


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create GitHub issues for critical CI failures"
    )
    parser.add_argument(
        "--report",
        type=Path,
        default="web/ci_report.json",
        help="Path to CI health report JSON",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating issues",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=5,
        help="Maximum number of issues to create in one run",
    )

    args = parser.parse_args()

    if not args.report.exists():
        print(f"❌ CI report not found: {args.report}")
        print("   Run 'python scripts/ci_status_monitor.py --format json' first")
        sys.exit(1)

    creator = CIIssueCreator(args.report)
    creator.run(dry_run=args.dry_run, max_issues=args.max_issues)


if __name__ == "__main__":
    main()
