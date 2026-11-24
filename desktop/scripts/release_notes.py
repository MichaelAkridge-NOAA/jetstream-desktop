"""Print one version's release notes from desktop/CHANGELOG.md.

    python desktop/scripts/release_notes.py 0.2.0            # print them
    python desktop/scripts/release_notes.py desktop-v0.2.0 -o notes.md

Fails if the changelog has no section for that version, so a release can't go out without notes.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


def notes_for(text: str, version: str) -> str:
    """The body of the `## <version>` section (up to the next `## ` heading)."""
    version = version.removeprefix("desktop-v").removeprefix("v")
    lines = text.splitlines()
    heading = re.compile(rf"^##\s+v?{re.escape(version)}(\s|$)")
    for start, line in enumerate(lines):
        if heading.match(line):
            body = []
            for line in lines[start + 1 :]:
                if line.startswith("## "):
                    break
                body.append(line)
            notes = "\n".join(body).strip()
            if notes:
                return notes + "\n"
            break
    raise ValueError(f"No notes for {version} in CHANGELOG.md")


def add_version_notes(text: str, version: str, subjects: list[str]) -> str:
    version = version.removeprefix("desktop-v").removeprefix("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Invalid desktop version: {version}")
    if re.search(rf"^##\s+v?{re.escape(version)}(?:\s|$)", text, re.MULTILINE):
        raise ValueError(f"Notes for {version} already exist in CHANGELOG.md")
    subjects = [subject.strip() for subject in subjects if subject.strip()]
    if not subjects:
        raise ValueError("No changes found for the new release")
    section = f"## {version}\n\n### Changes\n" + "".join(f"- {subject}\n" for subject in subjects) + "\n"
    match = re.search(r"^##\s", text, re.MULTILINE)
    return text[:match.start()] + section + text[match.start():] if match else text.rstrip() + "\n\n" + section


def git_subjects() -> list[str]:
    tag = subprocess.run(
        ["git", "describe", "--tags", "--match", "desktop-v[0-9]*", "--abbrev=0", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    revision = f"{tag.stdout.strip()}..HEAD" if tag.returncode == 0 else "HEAD"
    subjects = subprocess.check_output(["git", "log", "--no-merges", "--format=%s", revision], text=True, encoding="utf-8").splitlines()
    subjects = [subject for subject in subjects if not subject.startswith("Bump desktop version to ")]
    if not subjects:
        subjects = subprocess.check_output(["git", "log", "-1", "--format=%s", "HEAD"], text=True, encoding="utf-8").splitlines()
    return subjects


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("version")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--record-git", action="store_true", help="add a changelog section from git commit subjects")
    args = parser.parse_args()
    try:
        text = CHANGELOG.read_text(encoding="utf-8")
        if args.record_git:
            CHANGELOG.write_text(add_version_notes(text, args.version, git_subjects()), encoding="utf-8")
            return 0
        notes = notes_for(text, args.version)
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1
    if args.output:
        args.output.write_text(notes, encoding="utf-8")
    else:
        sys.stdout.write(notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
