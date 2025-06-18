# Step 2: Analyze

Purpose: To dive deeper into the areas identified in the "Reflect" step using static analysis tools and test results.

This step focuses on gathering concrete data about specific issues within the codebase.

## Activities

1.  **Run Static Analysis Tools**: Execute available static analysis tools to identify potential problems. Common tools and their uses in this project include:
    *   **Linting**:
        *   **Flake8**: Run `flake8 .` from the repository root to check for Python style and syntax errors.
        *   **Markdownlint**: Used for checking Markdown file formatting (often via pre-commit hooks or specific linters).
    *   **Complexity Analysis**:
        *   **Radon**: Use `radon cc . -a -s` to identify overly complex code blocks. Pay attention to blocks with high cyclomatic complexity scores.
    *   **Dependency Vulnerability Scan**:
        *   **Dependabot Alerts**: Review alerts in the GitHub "Security" tab.
        *   **Snyk**: Check Snyk reports (often integrated into CI via `.github/workflows/snyk.yml`).
        *   **Trivy**: Check Trivy scan results (see `.github/workflows/trivy.yml`).
        *   **Pip Audit**: Run `pip-audit` (see `.github/workflows/pip-audit.yml`) to check for vulnerabilities in Python packages.
    *   **Security Scans**:
        *   **CodeQL**: Review alerts from GitHub CodeQL scans (see `.github/workflows/codeql.yml`).
        *   **Trufflehog**: Check for leaked secrets (see `.github/workflows/trufflehog.yml`).

2.  **Produce Table of Findings**: Consolidate the output from the analysis tools into a structured format. A table is often useful:

    | File/Package      | Issue Type          | Description                             | Severity | Tool    |
    |-------------------|---------------------|-----------------------------------------|----------|---------|
    | `module/file.py`  | Complexity          | Function `x` has CC of 15               | Medium   | Radon   |
    | `another_mod/`    | Linting             | Multiple PEP 8 violations               | Low      | Flake8  |
    | `requirements.txt`| Vulnerability       | Package `xyz` v1.2.3 has CVE-YYYY-NNNNN | High     | Snyk    |
    | ...               | ...                 | ...                                     | ...      | ...     |

3.  **Review Test Failures and Coverage**:
    *   Execute the full test suite (e.g., `pytest`).
    *   Examine any test failures to understand the cause.
    *   Review test coverage reports (e.g., from `pytest-cov`). Identify any significant drops in coverage or areas with critically low coverage, especially those identified as potential risks in the "Reflect" step.

## Output

*   A detailed list of specific issues, vulnerabilities, and areas of concern, often summarized in a table.
*   A clear understanding of any test failures or regressions in test coverage.
*   This information will feed directly into the "Decide" step for task prioritization.
