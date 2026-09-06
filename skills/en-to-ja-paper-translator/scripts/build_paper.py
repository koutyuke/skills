from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def build(input_typ: Path, output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["typst", "compile", "--root", ".", str(input_typ), str(output_pdf)],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a translated Typst paper.")
    parser.add_argument("input_typ", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    build(args.input_typ, args.output_pdf)


if __name__ == "__main__":
    main()
