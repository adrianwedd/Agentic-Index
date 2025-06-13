#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
import shlex

# Regex to find the actionable findings (critical or high severity)
FINDING_RE = re.compile(r"^- \[ \] (🔴|🟠) `RAG_PILL ([^:`]+):` (.*)")
# Regex to clean markdown from titles
MARKDOWN_CLEAN_RE = re.compile(r"[`*_~\[\]()]")
# Regex to find fenced code blocks
CODE_BLOCK_RE = re.compile(r"^\s*```(?P<lang>\w*)\n(?P<code>.*?)\n^\s*```", re.MULTILINE | re.DOTALL)

def clean_title(text, max_len=60):
    """Cleans markdown from text and truncates for a title."""
    text = MARKDOWN_CLEAN_RE.sub("", text)
    if len(text) > max_len:
        return text[:max_len-3] + "..."
    return text

def extract_next_finding_or_heading_index(lines, start_index):
    """Finds the index of the next finding or major heading."""
    for i in range(start_index, len(lines)):
        if FINDING_RE.match(lines[i]):
            return i
        if lines[i].startswith("##") or lines[i].startswith("### "): # Next section
            return i
    return len(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate GitHub issue creation commands from a review Markdown file.")
    parser.add_argument("filepath", type=Path, help="Path to the review Markdown file.")
    args = parser.parse_args()

    if not args.filepath.exists():
        print(f"Error: File not found: {args.filepath}")
        return

    try:
        lines = args.filepath.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"Error reading file {args.filepath}: {e}")
        return

    modified_lines = list(lines) # Work on a copy
    gh_commands = []

    current_line_idx = 0
    while current_line_idx < len(lines):
        line = lines[current_line_idx]
        match = FINDING_RE.match(line)

        if match:
            severity_emoji, finding_title_part, finding_desc_part = match.groups()
            full_finding_text = f"{finding_title_part}: {finding_desc_part}".strip()

            title = clean_title(full_finding_text)

            # Determine the block of text for this finding (until the next finding or major heading)
            block_start_idx = current_line_idx + 1
            block_end_idx = extract_next_finding_or_heading_index(lines, block_start_idx)

            finding_block_text = "\n".join(lines[block_start_idx:block_end_idx]).strip()

            evidence_match = CODE_BLOCK_RE.search(finding_block_text)
            evidence_str = ""
            recommendation_str = ""

            if evidence_match:
                evidence_str = f"Evidence:\n```{evidence_match.group('lang')}\n{evidence_match.group('code').strip()}\n```"
                # Recommendation is text after the code block within this finding's block
                text_after_evidence = finding_block_text[evidence_match.end():].strip()
                if text_after_evidence:
                     recommendation_str = f"Recommendation:\n{text_after_evidence}"
            else:
                # If no code block, the whole block is considered recommendation/context
                if finding_block_text: # Check if there is any text at all
                    recommendation_str = f"Context/Recommendation:\n{finding_block_text}"


            body_parts = [part for part in [evidence_str, recommendation_str] if part]
            body = "\n\n".join(body_parts)

            # Ensure body is not empty
            if not body.strip() and full_finding_text: # Fallback if parsing failed but we have text
                 body = f"Finding Details:\n{full_finding_text}"
            elif not body.strip(): # Should not happen if title was made
                 body = "Details pending."


            label = "priority/critical" if "🔴" in severity_emoji else "priority/high"

            # Escape body for shell command
            escaped_body = shlex.quote(body)
            escaped_title = shlex.quote(title)

            gh_command = f"gh issue create --title {escaped_title} --body {escaped_body} --label \"{label}\""
            gh_commands.append(gh_command)

            # Modify the line in the copy
            modified_lines[current_line_idx] = f"{line} (ISSUE_URL_HERE)"
            current_line_idx = block_end_idx # Move past the processed block
            continue

        current_line_idx += 1

    # Print all gh commands
    for cmd in gh_commands:
        print(cmd)

    # Write modified lines back to the file
    try:
        args.filepath.write_text("\n".join(modified_lines) + "\n", encoding="utf-8")
        print(f"\nSuccessfully updated {args.filepath} with ISSUE_URL_HERE placeholders.")
    except Exception as e:
        print(f"Error writing updated content to {args.filepath}: {e}")


if __name__ == "__main__":
    main()
