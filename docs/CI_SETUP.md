# CI Setup

This repository's runners may have outbound access to PyPI blocked. To ensure `pre-commit` installs correctly, the workflow uses an explicit PyPI index.

```bash
pip install -i https://pypi.org/simple \
            --trusted-host pypi.org \
            pre-commit
```

Using this mirror (Option B) avoids firewall issues while keeping the installation steps simple.

## Example Workflow Step

Install the package in editable mode and run the ranking command:

```yaml
- name: Install dependencies
  run: pip install -e .
- name: Run ranking script
  run: agentic-index rank data/repos.json
```
