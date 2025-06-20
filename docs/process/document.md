# Step 6: Document

Purpose: To update all relevant project documentation to reflect the changes made and to record the work completed during the cycle.

Accurate and up-to-date documentation is crucial for project maintainability and onboarding new contributors.

## Activities

1.  **Update `ARCHITECTURE.md` (if structure changed)**:
    *   If the changes made during the "Execute" step resulted in modifications to the project's overall architecture, component interactions, or significant structural aspects, update `ARCHITECTURE.md`.
    *   This might involve updating text descriptions or regenerating diagrams (e.g., if using `scripts/gen_arch_diagrams.py`).
    *   If no architectural changes were made, this step can be skipped.

2.  **Append Changelog Entry in `CHANGELOG.md`**:
    *   Add an entry to `CHANGELOG.md` under the `[Unreleased]` section (or a new version section if a release is being prepared).
    *   The entry should follow the project's changelog format. For self-improvement cycles, use the following format:
        ```
        * [YYYY-MM-DD] chore(self-improve): cycle #{n} – summary of work done in this cycle.
        ```
        Replace `YYYY-MM-DD` with the current date and `#{n}` with the current cycle number. The summary should briefly describe the main tasks accomplished.
    *   Example:
        ```markdown
        ## [Unreleased]
        ### Changed
        * ... other changes ...

        ### Internal
        * [2023-10-27] chore(self-improve): cycle #5 – Updated dependencies, refactored auth module, and added tests for user service.
        ```
        (Note: The issue specified `chore(self-improve): cycle #{n} – summary of work`. If a more specific categorization like `### Internal` or `### Added` is preferred for these entries, adapt as necessary, but ensure the core `chore(self-improve): cycle #{n}` part is present.)

3.  **Annotate `tasks.yml`**:
    *   **Mark Completed Tasks**: For each task from `tasks.yml` that was completed during the cycle, update its `status` to `done`.
        ```yaml
        - id: 4
          description: "Fix critical vulnerability in `example-lib` by updating to v1.2.4"
          component: deps
          dependencies: []
          priority: 1
          status: done # Updated status
        ```
    *   **Add Newly Discovered Follow-up Tasks**: If any new issues or necessary follow-up work were identified during the cycle (e.g., during "Validate" or "Execute"), add them to `tasks.yml` with an appropriate description, component, priority, and `todo` status. These will be considered in the next cycle's "Decide" step.
    *   Run `scripts/validate_tasks.py tasks.yml` to verify the file matches the task schema.

## Output

*   Updated `ARCHITECTURE.md` (if applicable).
*   A new entry in `CHANGELOG.md` summarizing the cycle's achievements.
*   An updated `tasks.yml` with completed tasks marked as "done" and any new tasks added for future consideration.
*   The project's documentation accurately reflects its current state.
