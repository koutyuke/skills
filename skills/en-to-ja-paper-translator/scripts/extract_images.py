from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


def extract_images(pdf_path: Path, output_dir: Path) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    records: list[dict[str, object]] = []
    image_index = 1

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        for image in page.get_images(full=True):
            xref = image[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            elif pix.colorspace and pix.colorspace.n != 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)

            filename = f"image-{image_index:03d}.png"
            path = output_dir / filename
            pix.save(path)

            records.append(
                {
                    "index": image_index,
                    "page": page_index + 1,
                    "filename": filename,
                    "width": pix.width,
                    "height": pix.height,
                    "xref": xref,
                }
            )
            image_index += 1

    return records


def write_outputs(pdf_path: Path, output_dir: Path) -> None:
    records = extract_images(pdf_path, output_dir)
    (output_dir / "images.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract embedded images from a PDF.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    write_outputs(args.pdf, args.output_dir)


if __name__ == "__main__":
    main()
