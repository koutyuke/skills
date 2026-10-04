# skills

Codex などで使う個人用 Skill のリポジトリです。開発ツールは Nix Flake で固定しています。

```bash
direnv allow
```

リポジトリ全体を整形するには `nix fmt` を実行します。Markdown・YAML・JSON は Oxfmt、Python は Ruff、Typst は Typstyle、Nix は nixfmt が担当します。対象を絞る場合は `nix fmt -- skills/docs-that-work/SKILL.md` のように指定できます。

Markdown の日本語と英数字の間には空白を入れます。`nix develop` に入った後、次のコマンドを使います。

```bash
textlint README.md 'skills/**/*.md'
textlint --fix README.md 'skills/**/*.md'
```

`--fix` は対象ファイルを書き換えます。空白の設定は [`.textlintrc.json`](./.textlintrc.json) にあります。

direnv は [`.envrc`](./.envrc) から Nix 開発環境を自動で読み込みます。Zed では [`.zed/settings.json`](./.zed/settings.json) により保存時整形を有効にしています。Markdown・JSON・YAML は Oxfmt、Python は Ruff、Typst は Typstyle、Nix は nixfmt を使います。Markdown では続けて Textlint の空白修正を実行します。
