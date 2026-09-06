# 作業フロー詳細

## ディレクトリ構成

```text
papers/<title-slug>/
├── source/
│   └── <title-slug>.pdf
├── extracted/
│   ├── text/
│   │   ├── raw.md
│   │   └── pages.json
│   ├── images/
│   │   ├── image-001.png
│   │   └── images.json
│   ├── tables/
│   ├── equations/
│   └── extraction-report.md
├── translation/
│   ├── main.typ
│   ├── references.bib
│   └── glossary.md
├── build/
│   └── <title-slug>-ja.pdf
└── notes/
    ├── decisions.md
    └── qa-checklist.md
```

共通 Typst テンプレートは `papers/_typst/paper-template.typ` に置く。初回セットアップ時に skill の `assets/templates/paper-template.typ` からコピーし、各論文の `translation/main.typ` は `papers/_typst` 側を参照する。skill 配下の asset を直接 import しない。

`title-slug` は論文タイトルから作る。英字は小文字化し、空白・記号・ダッシュ類は `-` に寄せ、連続する `-` と先頭末尾の `-` を削除する。

## 抽出

最初に PDF がテキスト PDF かスキャン PDF かを確認する。テキストが取れるなら PyMuPDF と Poppler を優先し、OCR は最後の手段にする。

抽出時に確認する項目:

- ページ数
- 段組
- 図、表、式の数
- 参考文献形式
- PDF 内テキストの抽出品質
- 画像抽出時の解像度

抽出結果と既知の欠落は `extracted/extraction-report.md` に残す。

### 図画像の抽出判定

`extract_images.py` は PDF 内部の image XObject を抽出するだけであり、PDF 上で見える図全体を保証しない。グラフ、チャート、フローチャートは vector drawing、text、小さな raster image object の混在として保存されていることがある。

抽出後は `inspect_pdf_images.py` で image object のサイズと配置を確認する。次に当てはまる場合、その `image-*.png` は図全体として採用しない。

- width / height が極端に小さい。
- 同じページに小さな image object が複数あり、ひとつの figure の部品に見える。
- caption は存在するが、対応する大きな image object がない。
- グラフや図の軸、ラベル、線、点の一部しか含まれていない。

この場合は `crop_pdf_region.py` でページの該当領域を raster crop し、`figure-<番号>.png` または `figure-<番号>-page<n>.png` として保存する。`extraction-report.md` には、不採用にした `image-*.png` と crop 画像を採用した理由を書く。

座標決定は、できるだけ `pdftotext -bbox`、PyMuPDF の text blocks、`page.get_drawings()` などのテキスト・座標情報で行う。ページ全体画像を Agent に読み込ませて判断しない。

## 翻訳

翻訳前に `translation/glossary.md` を作り、訳語が揺れやすい用語を固定する。

翻訳時のルール:

- 技術用語は初出で原語を併記する。
- 原文の主張を強めたり弱めたりしない。
- Abstract, Introduction, Method, Results, Discussion, Conclusion の論理構造を維持する。
- 図表番号、式番号、citation key は原文との対応を保つ。
- 訳しにくい文は、原文の構文より論文日本語としての明確さを優先する。

## Typst 原稿

`translation/main.typ` は `papers/_typst` にコピーされたテンプレートを import する。

```typst
#import "/papers/_typst/paper-template.typ": *
```

図は `fig(...)` helper で参照し、表は可能な限り `table(...)` で再構成する。数式は Typst math を基本にし、判断が不安定なものは `extracted/equations/` に原形を残す。

本文は最初は 1 段組を推奨する。2 段組は日本語訳後の文量差、図表再配置、脚注調整が増えるため、原論文に近い見た目を優先する段階で検討する。

## 参考文献

`references.bib` は、PDF から抽出した参考文献をそのまま貼らず、原文参考文献、DOI、出版元情報を確認して整える。

本文側には Typst の `@key` 形式で citation key を埋め込む。

```typst
Transformer は sequence transduction の基盤モデルとして提案された @vaswani-2017-attention。
```

公開用原稿では `bib-full: true` を使わない。全件出力は「未引用文献の確認」など一時作業だけに限定し、最終的には本文中で引用された文献だけが参考文献一覧に出る状態にする。

## QA

QA はテキストベースで行う。ページ全体画像を Agent に読み込ませる確認は禁止する。

確認項目:

- `typst compile` が成功するか。
- `pdfinfo` でページ数と PDF 生成を確認できるか。
- `pdftotext` で参考文献一覧、citation 番号、主要見出しが確認できるか。
- `check_citations.py` で missing key が 0 件か。
- 図画像について、embedded image object を採用したか、page crop を採用したかが `extraction-report.md` に記録されているか。
- 図表番号と本文参照が一致しているか。
- 数式の添字・上付き・ギリシャ文字が Typst 側で崩れていないか。
- 原文にない断定や補足が混ざっていないか。

ページ画像を作る場合は、図の切り出しや抽出失敗箇所の局所確認に限定する。Agent にページ全体を画像として読ませない。
