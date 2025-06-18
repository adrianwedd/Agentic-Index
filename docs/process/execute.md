# Step 4: Execute

Purpose: To implement the changes required to complete the tasks selected in the "Decide" step.

This is where the actual coding, configuration changes, and test writing happen.

## Activities

For each task taken from `tasks.yml` (usually starting with the highest priority):

1.  **Understand the Task**: Thoroughly read the task description and any related information or analysis findings. Ensure the goal is clear.

2.  **Create a Branch**: Create a new Git branch for the task. A common naming convention is `feature/<task-id>-short-description` or `fix/<task-id>-short-description`. For example: `feature/task-4-update-example-lib`.

3.  **Install or Upgrade Dependencies (if applicable)**:
    *   If the task involves updating dependencies, modify `requirements.txt`, `pyproject.toml`, or other relevant files.
    *   Install the new versions (e.g., `pip install -r requirements.txt`).
    *   Ensure any lock files (`requirements.lock`, `poetry.lock`) are updated.

4.  **Apply Code or Configuration Changes**:
    *   Make the necessary modifications to source code, configuration files, CI scripts, etc.
    *   Follow project coding standards and best practices.
    *   Keep changes focused on the scope of the current task. If new, unrelated issues are discovered, note them down for a future cycle rather than expanding the current task's scope (unless critical).

5.  **Write or Update Tests**:
    *   If implementing new functionality, write unit tests and integration tests as appropriate.
    *   If fixing a bug, write a test that reproduces the bug first, then confirm the fix makes the test pass.
    *   If refactoring, ensure existing tests pass and add new ones if behavior is modified or new edge cases are covered.
    *   Aim to maintain or improve test coverage.

6.  **Run Local Validation**:
    *   Run tests locally (e.g., `pytest`).
    *   Run linters locally (e.g., `flake8 .`).
    *   Address any issues identified.

7.  **Stage and Commit Changes**:
    *   Stage the relevant changes (`git add <files>`).
    *   Commit the changes with a clear and descriptive message. The required format for this project is:
        ```
        feat(task-{id}): {short description of the change}
        ```
        Or, if it's a fix:
        ```
        fix(task-{id}): {short description of the fix}
        ```
        Or, for chores:
        ```
        chore(task-{id}): {short description of the chore}
        ```
        Replace `{id}` with the actual task ID from `tasks.yml`. The description should be concise and informative.

        Example: `feat(task-4): Update example-lib to v1.2.4`

    *   If a task requires multiple commits, ensure each commit is logical and the final commit message for the Pull Request (if applicable) summarizes the overall change for the task.

## Output

*   One or more commits on a feature branch, implementing the changes for a specific task.
*   Updated codebase, configurations, and tests.
*   Code that is ready for the "Validate" step.
