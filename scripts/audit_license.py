import json
import sys
import argparse
from pathlib import Path

ALLOWED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "MPL-2.0"}

def audit(file_path: Path) -> bool:
    with file_path.open() as f:
        repos = json.load(f)

    offending = []
    for repo in repos:
        license_info = repo.get("license")
        spdx = None
        if isinstance(license_info, dict):
            spdx = license_info.get("spdx_id")
        if spdx not in ALLOWED_LICENSES:
            name = repo.get("full_name") or repo.get("name")
            offending.append((name, spdx))

    if offending:
        print("Offending repositories with non-compliant licenses:")
        for name, spdx in offending:
            print(f"{name}: {spdx}")
        return False
    else:
        print("All repositories have approved licenses.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Audit repository licenses")
    parser.add_argument("path", nargs="?", default="data/repos.json",
                        help="Path to JSON file with repository metadata")
    args = parser.parse_args()

    file_path = Path(args.path)
    if not file_path.is_file():
        print(f"File not found: {file_path}")
        sys.exit(1)

    ok = audit(file_path)
    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
