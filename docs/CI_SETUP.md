# CI Setup

This repository's runners may have outbound access to PyPI blocked. To ensure `pre-commit` installs correctly, the workflow uses an explicit PyPI index.

```bash
pip install -i https://pypi.org/simple \
            --trusted-host pypi.org \
            pre-commit
```

Using this mirror (Option B) avoids firewall issues while keeping the installation steps simple.

## Setting `PIP_INDEX_URL`

Some environments block direct internet access. Set the `PIP_INDEX_URL` environment
variable to your internal PyPI mirror so all `pip` commands automatically use it.

```bash
export PIP_INDEX_URL=https://pypi.mycompany.com/simple
pip install -r requirements.txt
```

`pip install -r requirements.txt` must succeed before running `pip-audit` so the
audit tool can resolve every dependency.

## Example Workflow Step

Install the package in editable mode and run the ranking command:

```yaml
- name: Install dependencies
  run: pip install -e .
- name: Run ranking script
  run: agentic-index rank data/repos.json
```
