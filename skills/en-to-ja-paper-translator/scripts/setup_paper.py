from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "templates" / "paper-template.typ"


def slugify(title: str) -> str:
    value = title.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def ensure_typst_template(papers_dir: Path, template_source: Path = DEFAULT_TEMPLATE) -> Path:
    typst_dir = papers_dir / "_typst"
    typst_dir.mkdir(parents=True, exist_ok=True)

    template_dest = typst_dir / "paper-template.typ"
    if not template_dest.exists():
        shutil.copy2(template_source, template_dest)
    return template_dest


def setup_paper(pdf_path: Path, title: str, papers_dir: Path) -> Path:
    ensure_typst_template(papers_dir)

    slug = slugify(title)
    paper_dir = papers_dir / slug
    source_dir = paper_dir / "source"
    for child in [
        source_dir,
        paper_dir / "extracted" / "text",
        paper_dir / "extracted" / "images",
        paper_dir / "extracted" / "tables",
        paper_dir / "extracted" / "equations",
        paper_dir / "translation",
        paper_dir / "build",
        paper_dir / "notes",
    ]:
        child.mkdir(parents=True, exist_ok=True)

    shutil.copy2(pdf_path, source_dir / f"{slug}.pdf")
    return paper_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a paper workspace.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--papers-dir", type=Path, default=Path("papers"))
    args = parser.parse_args()
    paper_dir = setup_paper(args.pdf, args.title, args.papers_dir)
    print(paper_dir)


if __name__ == "__main__":
    main()
