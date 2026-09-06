from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import fitz


def extract_pages(pdf_path: Path) -> list[dict[str, object]]:
    doc = fitz.open(pdf_path)
    pages: list[dict[str, object]] = []
    for index in range(doc.page_count):
        page = doc.load_page(index)
        pages.append(
            {
                "page": index + 1,
                "text": cast(str, page.get_text("text")).strip(),
            }
        )
    return pages


def write_outputs(pdf_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = extract_pages(pdf_path)
    raw_text = "\n\n".join(f"<!-- page {page['page']} -->\n{page['text']}" for page in pages)

    (output_dir / "raw.md").write_text(raw_text + "\n", encoding="utf-8")
    (output_dir / "pages.json").write_text(
        json.dumps(pages, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract page text from a PDF.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    write_outputs(args.pdf, args.output_dir)


if __name__ == "__main__":
    main()
