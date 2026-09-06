# ツールと環境

## 必須ツール

- Typst CLI: `translation/main.typ` から PDF を生成する。
- Poppler: `pdfinfo`、`pdftotext`、`pdfimages` で PDF を確認・抽出する。
- Python 3.12: 抽出、検査、ビルド補助に使う。
- uv: Python 依存関係を管理する。
- PyMuPDF: PDF テキスト、画像、ページ情報の抽出に使う。

## 推奨コマンド

```sh
direnv exec . python .agents/skills/en-to-ja-paper-translator/scripts/extract_text.py papers/<title-slug>/source/<title-slug>.pdf papers/<title-slug>/extracted/text
direnv exec . python .agents/skills/en-to-ja-paper-translator/scripts/extract_images.py papers/<title-slug>/source/<title-slug>.pdf papers/<title-slug>/extracted/images
direnv exec . python .agents/skills/en-to-ja-paper-translator/scripts/inspect_pdf_images.py papers/<title-slug>/source/<title-slug>.pdf --output papers/<title-slug>/extracted/images/inspection.json
direnv exec . python .agents/skills/en-to-ja-paper-translator/scripts/crop_pdf_region.py papers/<title-slug>/source/<title-slug>.pdf papers/<title-slug>/extracted/images/figure-005.png --page 8 --rect 40,90,560,720 --dpi 300
direnv exec . python .agents/skills/en-to-ja-paper-translator/scripts/check_citations.py papers/<title-slug>/translation/main.typ papers/<title-slug>/translation/references.bib
direnv exec . python .agents/skills/en-to-ja-paper-translator/scripts/build_paper.py papers/<title-slug>/translation/main.typ papers/<title-slug>/build/<title-slug>-ja.pdf
direnv exec . pdftotext papers/<title-slug>/build/<title-slug>-ja.pdf -
direnv exec . pdfinfo papers/<title-slug>/build/<title-slug>-ja.pdf
```

## 条件付きツール

- GROBID: 章構造や参考文献を TEI XML として取りたい場合に使う。
- OCRmyPDF / Tesseract: スキャン PDF の場合だけ使う。
- camelot / tabula-java: 表抽出の自動化が必要な場合だけ使う。
- pandoc / latexml: 数式や LaTeX 由来の構造を補助変換したい場合だけ使う。

条件付きツールは、対象 PDF で必要性が分かってから導入する。最初から増やすと、翻訳 PDF 作成よりツール検証に時間を使いやすい。

## Nix / direnv / uv

プロジェクトに Nix と direnv がある場合は、`direnv exec .` を前置してコマンドを実行する。Python パッケージは uv で同期する。

この skill 自体は特定リポジトリに依存しないが、実行先プロジェクトには Typst、Poppler、Python、PyMuPDF が必要である。
