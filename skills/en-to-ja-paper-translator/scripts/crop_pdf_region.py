from __future__ import annotations

import argparse
from pathlib import Path

import fitz


def parse_rect(value: str) -> fitz.Rect:
    parts = [float(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--rect must be x0,y0,x1,y1")
    x0, y0, x1, y1 = parts
    if x1 <= x0 or y1 <= y0:
        raise argparse.ArgumentTypeError("--rect must satisfy x1>x0 and y1>y0")
    return fitz.Rect(x0, y0, x1, y1)


def clamp_rect(rect: fitz.Rect, bounds: fitz.Rect) -> fitz.Rect:
    return fitz.Rect(
        max(rect.x0, bounds.x0),
        max(rect.y0, bounds.y0),
        min(rect.x1, bounds.x1),
        min(rect.y1, bounds.y1),
    )


def crop_pdf_region(
    pdf_path: Path,
    output_path: Path,
    *,
    page_number: int,
    rect: fitz.Rect,
    dpi: int,
    padding: float,
) -> fitz.Rect:
    doc = fitz.open(pdf_path)
    if page_number < 1 or page_number > doc.page_count:
        raise ValueError(f"page must be between 1 and {doc.page_count}")

    page = doc.load_page(page_number - 1)
    padded_rect = fitz.Rect(
        rect.x0 - padding,
        rect.y0 - padding,
        rect.x1 + padding,
        rect.y1 + padding,
    )
    clip = clamp_rect(padded_rect, page.rect)
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(output_path)
    return clip


def main() -> None:
    parser = argparse.ArgumentParser(description="Render and crop a rectangular PDF page region.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--page", type=int, required=True, help="1-based PDF page number.")
    parser.add_argument("--rect", type=parse_rect, required=True, help="x0,y0,x1,y1 in PDF points.")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--padding", type=float, default=0)
    args = parser.parse_args()

    clip = crop_pdf_region(
        args.pdf,
        args.output,
        page_number=args.page,
        rect=args.rect,
        dpi=args.dpi,
        padding=args.padding,
    )
    print(
        f"wrote {args.output} page={args.page} "
        f"clip={clip.x0:.2f},{clip.y0:.2f},{clip.x1:.2f},{clip.y1:.2f} dpi={args.dpi}"
    )


if __name__ == "__main__":
    main()
