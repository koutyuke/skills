---
name: en-to-ja-paper-translator
description: 英語論文PDFから本文・図・表・数式・参考文献を抽出し、日本語訳のTypst原稿とPDFを作成する。論文PDFの翻訳、画像抽出、references.bib整備、citation key埋め込み、Typstビルド、テキストベースQAが必要なときに使う。
---

# 英語論文PDFの日本語Typst化

この skill は、英語論文 PDF を日本語に翻訳し、共通 Typst テンプレートで PDF 化するために使う。

## 必須方針

- 論文ごとの作業ディレクトリは `papers/<title-slug>/` に作る。
- `title-slug` は論文タイトルを小文字化し、kebab-case に正規化する。
- 原 PDF、抽出画像、翻訳本文、生成 PDF は公開時の権利確認が必要なため、原則 Git 管理しない。
- 図は PDF から抽出した画像を使う。表・式・再現可能なグラフは、可能な限り Typst/LaTeX 相当の構造に起こす。
- 参考文献は `translation/references.bib` に置き、本文側に Typst の `@key` citation を埋め込む。
- 公開用原稿では `bib-full: true` による全件出力を使わない。全件出力は一時確認だけに限定する。
- QA でページ全体画像を Agent に読み込ませて画像認識で整合性確認してはいけない。token 消費が大きいため、`typst compile`、`pdfinfo`、`pdftotext`、JSON/テキスト差分、citation key 検査を使う。

## 使うファイル

- Typst テンプレート原本: `assets/templates/paper-template.typ`
- 補助スクリプト: `scripts/`
- 詳細手順: `references/workflow.md`
- ツールと環境: `references/tools.md`

必要になったときだけ reference を読む。まずはこの SKILL.md の手順で進める。

## 標準フロー

1. `setup_paper.py` で論文作業ディレクトリを作る。
2. `extract_text.py` で PDF テキストを `extracted/text/` に抽出する。
3. `extract_images.py` で PDF 内画像を `extracted/images/` に抽出する。
4. `inspect_pdf_images.py` で画像 object のサイズと配置を点検し、図全体ではない小さな部品画像を判定する。
5. 図が vector drawing / text / 小さな raster 部品の混在なら、`crop_pdf_region.py` で該当ページ領域を crop して図画像を作る。
6. 抽出結果をテキストベースで確認し、図表・式・参考文献の対応を記録する。
7. `translation/main.typ` を作り、`papers/_typst/paper-template.typ` を import する。
8. 日本語訳本文を書く。技術用語・図表番号・式番号・citation key は原文との対応を保つ。
9. `references.bib` を DOI、出版元、原文参考文献に基づいて整備する。
10. 本文中に `@key` を埋め込み、`check_citations.py` で未解決 key と未引用 key を確認する。
11. `build_paper.py` で Typst PDF をビルドする。
12. `pdfinfo` と `pdftotext` でページ数、参考文献出力、本文参照、欠落を確認する。

## 代表コマンド

```sh
python .agents/skills/en-to-ja-paper-translator/scripts/setup_paper.py input.pdf --title "Attention Is All You Need"
python .agents/skills/en-to-ja-paper-translator/scripts/extract_text.py papers/attention-is-all-you-need/source/attention-is-all-you-need.pdf papers/attention-is-all-you-need/extracted/text
python .agents/skills/en-to-ja-paper-translator/scripts/extract_images.py papers/attention-is-all-you-need/source/attention-is-all-you-need.pdf papers/attention-is-all-you-need/extracted/images
python .agents/skills/en-to-ja-paper-translator/scripts/inspect_pdf_images.py papers/attention-is-all-you-need/source/attention-is-all-you-need.pdf --output papers/attention-is-all-you-need/extracted/images/inspection.json
python .agents/skills/en-to-ja-paper-translator/scripts/crop_pdf_region.py papers/attention-is-all-you-need/source/attention-is-all-you-need.pdf papers/attention-is-all-you-need/extracted/images/figure-005.png --page 8 --rect 40,90,560,720 --dpi 300
python .agents/skills/en-to-ja-paper-translator/scripts/check_citations.py papers/attention-is-all-you-need/translation/main.typ papers/attention-is-all-you-need/translation/references.bib
python .agents/skills/en-to-ja-paper-translator/scripts/build_paper.py papers/attention-is-all-you-need/translation/main.typ papers/attention-is-all-you-need/build/attention-is-all-you-need-ja.pdf
```

`direnv` や `uv` を使うプロジェクトでは、必要に応じて `direnv exec .` を前置する。

## Typst import 例

```typst
#import "/papers/_typst/paper-template.typ": *

#show: translated-paper.with(
  title-ja: "Attention Is All You Need",
  title-original: "Attention Is All You Need",
  authors: ("Ashish Vaswani", "Noam Shazeer"),
  published: "2017",
  source-url: "https://arxiv.org/abs/1706.03762",
  bib-file: "/papers/attention-is-all-you-need/translation/references.bib",
)

= はじめに

Transformer は sequence transduction の基盤モデルとして提案された @vaswani-2017-attention。
```

## QA の禁止事項

- 原 PDF や生成 PDF のページ全体、抽出した図を PNG 化して Agent に読み込ませない。
- 画像認識で「見た目が合っているか」を網羅確認しない。
- `extract_images.py` の出力を無条件に図全体とみなさない。小さな image object は図の部品である可能性が高い。
- `references.bib` の全項目を出す目的で `bib-full: true` を残さない。
- DOI や書誌情報を推測で埋めない。不確かな場合は未確認として記録する。

## 完了条件

- `typst compile` が成功し、`build/<title-slug>-ja.pdf` が生成されている。
- citation key 検査で missing が 0 件である。
- 参考文献一覧が本文中の citation から出力されている。
- 図画像について、embedded image object を採用したのか、page crop を採用したのかが `extraction-report.md` に記録されている。
- 図表・式の対応と既知の未解決事項が `notes/qa-checklist.md` に記録されている。
- 実行した検証と未実施の検証を最終報告に分けて書く。
