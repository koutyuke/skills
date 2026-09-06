from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CITATION_PATTERN = re.compile(r"(?<![\w/])@([A-Za-z0-9_-]+)")
BIB_KEY_PATTERN = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)


def read_citation_keys(typ_path: Path) -> set[str]:
    text = typ_path.read_text(encoding="utf-8")
    return set(CITATION_PATTERN.findall(text))


def read_bib_keys(bib_path: Path) -> set[str]:
    text = bib_path.read_text(encoding="utf-8")
    return set(BIB_KEY_PATTERN.findall(text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Typst citation keys against a BibTeX file.")
    parser.add_argument("typ", type=Path)
    parser.add_argument("bib", type=Path)
    parser.add_argument(
        "--allow-uncited",
        action="store_true",
        help="Allow BibTeX entries that are not cited from the Typst file.",
    )
    args = parser.parse_args()

    citations = read_citation_keys(args.typ)
    bib_keys = read_bib_keys(args.bib)
    missing = sorted(citations - bib_keys)
    uncited = sorted(bib_keys - citations)

    print(f"citations: {len(citations)}")
    print(f"bib entries: {len(bib_keys)}")
    print(f"missing in bib: {missing}")
    print(f"uncited in typ: {uncited}")

    if missing or (uncited and not args.allow_uncited):
        sys.exit(1)


if __name__ == "__main__":
    main()
