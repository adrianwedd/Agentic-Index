# Step 5: Validate

Purpose: To ensure that the changes made during the "Execute" step are correct, do not introduce new issues, and meet the task's objectives.

This step typically involves running automated checks and potentially manual review after changes are integrated or proposed for integration (e.g., in a Pull Request).

## Activities

1.  **Run Full Test Suite**:
    *   Execute all automated tests (unit, integration, end-to-end) in a clean environment, similar to CI. (e.g., `pytest --cov=.`)
    *   Ensure all tests pass. If not, return to the "Execute" step to fix the issues.

2.  **Re-run Linting, Complexity, and Security Scans**:
    *   Run all relevant static analysis tools again on the changed codebase. This includes:
        *   Linters (e.g., `flake8 .`)
        *   Complexity checkers (e.g., `radon cc . -a -s`)
        *   Security scanners (e.g., `snyk test`, `trivy fs .`, `pip-audit`)
    *   These checks are often performed automatically by the CI system upon submitting a Pull Request.

3.  **Confirm Exit Codes and No New Critical Issues**:
    *   Verify that all tool executions complete successfully (exit code 0).
    *   Review the output of the scans to ensure no new critical or high-severity issues have been introduced by the changes.
    *   Compare with baseline scans if available, to distinguish new issues from pre-existing ones.

4.  **Review Test Coverage**:
    *   Check the updated test coverage report.
    *   Ensure that test coverage has not decreased, especially for the modified code sections. Ideally, it should increase or stay the same.

5.  **Summarize Pass/Fail and Any Remaining Warnings**:
    *   Document the outcome of the validation process.
    *   Note any new warnings or non-critical issues that were identified but deemed acceptable for the current cycle (these might become tasks in a future cycle).
    *   If validation fails, the issues must be addressed by returning to the "Execute" step.

## Output

*   Confirmation that the changes are correct, all tests pass, and no new critical issues have been introduced.
*   A summary of the validation results, including any minor warnings or issues to be addressed later.
*   Confidence to proceed to the "Document" step.
