# Secrets and Git LFS

This project uses pre-commit hooks to prevent large or sensitive files from accidentally entering the repository. The `detect-large-files` hook blocks binaries over 5&nbsp;MB except for archived history data.

## Installing Git LFS

1. Install the Git LFS package for your platform. On Ubuntu:
   ```bash
   sudo apt-get install git-lfs
   ```
2. Enable it for your user account:
   ```bash
   git lfs install
   ```

## Files Tracked in LFS

The repository automatically tracks these patterns via `.gitattributes`:

- `*.png`
- `*.gif`

Git will store matching files as pointers, reducing clone size and avoiding large pushes.
