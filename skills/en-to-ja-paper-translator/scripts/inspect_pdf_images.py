from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

import fitz


def inspect_images(
    pdf_path: Path,
    *,
    min_width: int,
    min_height: int,
) -> list[dict[str, Any]]:
    doc = fitz.open(pdf_path)
    records: list[dict[str, Any]] = []

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        for image in page.get_images(full=True):
            xref = cast(int, image[0])
            width = cast(int, image[2])
            height = cast(int, image[3])
            rects = [
                [rect.x0, rect.y0, rect.x1, rect.y1]
                for rect in page.get_image_rects(xref)
            ]
            reasons: list[str] = []
            if width < min_width:
                reasons.append(f"width<{min_width}")
            if height < min_height:
                reasons.append(f"height<{min_height}")
            if len(rects) == 0:
                reasons.append("no-placement-rect")

            records.append(
                {
                    "page": page_index + 1,
                    "xref": xref,
                    "width": width,
                    "height": height,
                    "rects": rects,
                    "suspect": len(reasons) > 0,
                    "reasons": reasons,
                }
            )

    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect embedded PDF image objects and flag small fragment images."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-width", type=int, default=300)
    parser.add_argument("--min-height", type=int, default=300)
    args = parser.parse_args()

    records = inspect_images(args.pdf, min_width=args.min_width, min_height=args.min_height)
    payload = json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
