from __future__ import annotations

import argparse
from pathlib import Path

import fitz


def render_pages(pdf_path: Path, output_dir: Path, scale: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    matrix = fitz.Matrix(scale, scale)
    for index in range(doc.page_count):
        page = doc.load_page(index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(output_dir / f"page-{index + 1:03d}.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG files.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--scale", type=float, default=1.5)
    args = parser.parse_args()
    render_pages(args.pdf, args.output_dir, args.scale)


if __name__ == "__main__":
    main()
