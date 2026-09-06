// 英語論文の日本語翻訳PDF向け共通テンプレート

#let font-serif = ("Source Han Serif", "Hiragino Mincho ProN", "YuMincho", "Times New Roman")
#let font-sans = ("Source Han Sans", "Hiragino Sans", "YuGothic", "Arial")
#let font-mono = ("Source Han Mono", "Menlo")
#let font-en = ("Times New Roman", "Source Han Serif")

#let setup-bibliography(
  bib-file,
  lang: "ja",
  style: "ieee",
  title: auto,
  full: false,
) = {
  if bib-file != none {
    let bib-title = if title == auto {
      if lang == "ja" { "参考文献" } else { "References" }
    } else {
      title
    }

    set bibliography(
      title: bib-title,
      style: style,
    )

    bibliography(bib-file, full: full)
  }
}

#let meta-line(label, value) = {
  if value != none {
    block[
      #text(font: font-sans, weight: "bold")[#label]
      #h(0.5em)
      #value
    ]
  }
}

#let keyword-line(label, values, separator: "、") = {
  if values.len() > 0 {
    block[
      #set par(first-line-indent: 0em)
      #text(font: font-sans, weight: "bold")[#label]
      #h(0.5em)
      #values.join(separator)
    ]
  }
}

#let info-box(title, body, fill: luma(247)) = {
  block(
    fill: fill,
    inset: 8pt,
    radius: 3pt,
    stroke: (left: 1.2pt + luma(180)),
  )[
    #set par(first-line-indent: 0em, leading: 0.62em)
    #text(font: font-sans, weight: "bold")[#title]
    #v(0.25em)
    #body
  ]
}

#let translated-paper(
  // 翻訳成果物のタイトル
  title-ja: none,
  subtitle-ja: none,
  title-original: none,
  subtitle-original: none,
  // 原論文のメタデータ
  authors: (),
  venue: none,
  published: none,
  doi: none,
  source-url: none,
  license-note: none,
  translator-note: none,
  // 概要・キーワード
  abstract-ja: none,
  abstract-original: none,
  keywords-ja: (),
  keywords-original: (),
  // レイアウト
  lang: "ja",
  body-columns: 1,
  body-pagebreak: false,
  page-numbering: "1",
  // 参考文献
  bib-file: none,
  bib-full: false,
  bib-style: "ieee",
  bib-title: auto,
  // 本文
  body,
) = {
  set page(
    paper: "a4",
    margin: (
      top: 22mm,
      bottom: 22mm,
      left: 20mm,
      right: 20mm,
    ),
    numbering: page-numbering,
    number-align: center,
  )

  set text(
    font: font-serif,
    size: 10.5pt,
    lang: lang,
  )
  set par(
    justify: true,
    leading: 0.72em,
    first-line-indent: 1em,
  )
  set heading(numbering: "1.1")
  set figure.caption(separator: " ")
  show raw: set text(font: font-mono, size: 0.9em)

  show heading: it => {
    let title-size = if it.level == 1 { 13pt } else if it.level == 2 { 11pt } else { 10.5pt }
    let before = if it.level == 1 { 1.0em } else { 0.7em }
    let after = if it.level == 1 { 0.45em } else { 0.25em }

    v(before)
    block[
      #set text(font: font-sans, weight: "bold", size: title-size)
      #if it.numbering != none {
        counter(heading).display(it.numbering)
        h(0.45em)
      }
      #it.body
    ]
    v(after)
  }

  align(center)[
    #if title-ja != none {
      text(font: font-sans, size: 18pt, weight: "bold")[#title-ja]
    }

    #if subtitle-ja != none {
      v(0.35em)
      text(font: font-sans, size: 12pt, weight: "bold")[#subtitle-ja]
    }

    #if title-original != none {
      v(0.75em)
      text(font: font-en, size: 11pt, weight: "bold")[#title-original]
    }

    #if subtitle-original != none {
      v(0.25em)
      text(font: font-en, size: 10pt)[#subtitle-original]
    }

    #if authors.len() > 0 {
      v(0.7em)
      text(font: font-en, size: 10pt)[#authors.join(", ")]
    }
  ]

  if venue != none or published != none or doi != none or source-url != none or license-note != none {
    v(0.9em)
    info-box(
      [原論文情報],
      [
        #meta-line([掲載先:], venue)
        #meta-line([出版年:], published)
        #meta-line([DOI:], doi)
        #meta-line([URL:], source-url)
        #meta-line([ライセンス・利用条件:], license-note)
      ],
    )
  }

  if translator-note != none {
    v(0.65em)
    info-box([翻訳注], translator-note, fill: luma(250))
  }

  if abstract-ja != none {
    v(1em)
    block[
      #set par(first-line-indent: 0em)
      #text(font: font-sans, weight: "bold")[概要]
      #h(0.5em)
      #abstract-ja
    ]
  }

  if abstract-original != none {
    v(0.55em)
    block[
      #set par(first-line-indent: 0em)
      #text(font: font-en, weight: "bold")[Original Abstract]
      #h(0.5em)
      #text(font: font-en)[#abstract-original]
    ]
  }

  if keywords-ja.len() > 0 {
    v(0.55em)
    keyword-line([キーワード], keywords-ja)
  }

  if keywords-original.len() > 0 {
    v(0.25em)
    keyword-line([Keywords], keywords-original, separator: ", ")
  }

  if body-pagebreak {
    pagebreak()
  } else {
    v(1em)
  }

  if body-columns == 2 {
    show: columns.with(2, gutter: 7mm)
    body
  } else {
    body
  }

  setup-bibliography(
    bib-file,
    lang: lang,
    style: bib-style,
    title: bib-title,
    full: bib-full,
  )
}

#let indent(spacing: 1em) = h(spacing)

#let source-page(page) = {
  text(font: font-sans, size: 8pt, fill: luma(90))[
    原文 p.#page
  ]
}

#let todo(body) = {
  block(
    fill: rgb("#fff6d6"),
    inset: 6pt,
    radius: 3pt,
    stroke: 0.7pt + rgb("#d8a700"),
  )[
    #set par(first-line-indent: 0em)
    #text(font: font-sans, weight: "bold")[要確認]
    #h(0.5em)
    #body
  ]
}

#let translation-note(body) = {
  block(
    fill: luma(250),
    inset: 6pt,
    radius: 3pt,
    stroke: 0.5pt + luma(210),
  )[
    #set par(first-line-indent: 0em)
    #text(font: font-sans, weight: "bold")[訳注]
    #h(0.5em)
    #body
  ]
}

#let fig(path, caption: "", width: 100%, placement: auto) = {
  figure(
    image(path, width: width),
    caption: figure.caption(caption, position: bottom),
    supplement: [図],
    kind: image,
    placement: placement,
  )
}

#let raw-fig(content, caption: "", placement: auto) = {
  figure(
    content,
    caption: figure.caption(caption, position: bottom),
    supplement: [図],
    kind: image,
    placement: placement,
  )
}

#let tbl(content, caption: "", placement: auto) = {
  figure(
    content,
    caption: figure.caption(caption, position: top),
    supplement: [表],
    kind: "table",
    placement: placement,
  )
}

#let equation-block(content, caption: none) = {
  if caption == none {
    block[
      #align(center)[#content]
    ]
  } else {
    figure(
      align(center)[#content],
      caption: caption,
      supplement: [式],
      kind: "equation",
    )
  }
}
