# 節の骨格と技術ごとの差し替え

参考例 2 つに共通する骨格と、技術 X に合わせて何を差し替えるかをまとめる。節名は英語、本文は日本語で書く。

## 共通骨格

| 節                              | 役割                                   | Rust 版での中身                            | Effect 版での中身                                      | X で決めること                                            |
| ------------------------------- | -------------------------------------- | ------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------------- |
| `Role`                          | メンターの立場と最終目標               | Rust 初学者に考え方まで教える              | TypeScript は書けるが Effect は初学者                  | 読者の出発点と到達点                                      |
| `Basic Policy`                  | 回答の基本方針                         | 小さな例、なぜ、コラム                     | 同じ + 図                                              | X 固有に強調する方針                                      |
| `Target User`                   | 知っているもの / 前提にしないもの      | 所有権、`Option`、トレイト、…              | `Effect<A, E, R>`、`Layer`、`Fiber`、…                 | 前提にしない概念の一覧                                    |
| `Response Style`                | 結論 → 例 → 動き → なぜ                | `&name` の借用を例に                       | `yield*` の実行を例に                                  | 各段の回答例                                              |
| `X Mental Model`                | X の中心概念を図付きで                 | 所有権、借用、可変借用、ライフタイム       | 計画としての Effect、3 型引数、失敗/欠陥、Tag/Layer、… | 柱を 3〜8 個                                              |
| `Error Explanation`             | 最初に出会うエラーの 6 段階説明        | 所有権の移動によるコンパイルエラー         | `R` が残る型エラー、`yield*` 忘れ                      | 最初に出会うエラーの種類と実例                            |
| `Comparisons`                   | 似た概念の比較(選び方まで)             | `String` と `&str`、`Rc` と `Arc`、…       | `Promise` と `Effect`、`fail` と `die`、…              | 15 項目以上                                               |
| `Step-by-Step Explanation`      | 複雑な処理の分解                       | イテレータチェーンの流れ                   | `pipe` での `A`、`E`、`R` の変化                       | 分解して見せる代表例                                      |
| `Type Explanation`              | 型を手がかりにする                     | イテレータやクロージャの型                 | `Effect` の 3 型引数を注釈で示す                       | 型が無い技術では「構造」「状態」に置き換える              |
| `Compiler Perspective`          | 検査器や実行系の視点                   | コンパイラから見た move                    | 型検査が `E` と `R` を集計する様子                     | コンパイラ / 型検査 / ランタイム / インタープリタのどれか |
| `Bad Example and Good Example`  | 動かない例と修正版                     | move 後の使用                              | `try`/`catch` で囲む、`gen` 内の `await`               | X で典型的な間違い 2〜3 組                                |
| `Advanced Knowledge`            | 「もう一歩踏み込むと」の話題           | メモリ、性能、標準ライブラリの設計         | Fiber ランタイム、`Layer` のメモ化、版差               | 話題の一覧と長さの上限                                    |
| `Column`                        | コラムの形式と実例                     | なぜ `String` と `str` が分かれている      | なぜ `yield*`、なぜ `_tag`                             | 2 本以上の実例と候補リスト                                |
| `Practical Knowledge`           | X らしい慣習                           | `&str` を引数に取る                        | ポートは `Tag`、実装は `Layer`、`Live` 命名            | 「動くか」ではなく「一般的か」の例                        |
| `Do Not Overcomplicate`         | 優先順位と、最初から出さない話題       | MIR、LLVM IR、variance                     | Fiber 内部、`STM`、`Stream`                            | 具体名で挙げる                                            |
| `Avoid Unnecessary Jargon`      | 用語の初出説明                         | deref coercion                             | モナド、`R` チャネル                                   | 悪い例と良い例                                            |
| `When Multiple Solutions Exist` | 初心者向け → 一般的な書き方            | `match` → `?`                              | `gen` → `pipe`、`Tag` → `Effect.Service`               | 代表的な二択                                              |
| 学習用の近道の節                | 学習では許し、本番では注意する操作     | `unwrap()` と `expect()`                   | `runSync` と `runPromise`                              | X での近道と本番での注意                                  |
| 危険に見える機能の節            | 「危険」で終わらせず意図を説明する対象 | `unsafe`                                   | `die`、`orDie`、`*Sync`                                | X で誤解されやすい機能                                    |
| `Suggested Response Structure`  | 回答の節構成                           | 結論 / コード例 / 解説 / なぜ / … / コラム | 同じ + 図                                              | 必要な節だけ使う旨                                        |
| `When User Provides Code`       | 提示コードを基に説明する手順           | 4 段階                                     | 同じ                                                   | ほぼ共通                                                  |
| `When Refactoring Code`         | 改善理由の観点                         | 可読性、所有権、借用、…                    | 失敗と依存が型に現れるか、差し替え、解放、…            | X の価値に沿った観点                                      |
| `Questions From Beginners`      | 否定しない、素朴な問いへの答え方       | なぜ全部 `clone()` してはいけないか        | なぜ `async`/`await` で十分ではないか                  | X で最も多い素朴な問い                                    |
| `Performance Explanations`      | 根拠なく速い / 遅いと言わない          | stack と heap、allocation                  | Fiber の間接処理、バンドルサイズ                       | X で計測すべき軸                                          |
| `Diagrams`                      | 図の種類と簡略図である旨               | メモリ図                                   | 依存グラフ、型引数の変化                               | 2 種類以上                                                |
| ツールチェーンの節              | コマンドの意味                         | `Cargo`                                    | `pnpm`、`tsc`、`vitest`                                | 主要コマンド 3 つ前後                                     |
| エコシステムの節                | 外部パッケージの紹介の仕方             | `External Crates`                          | `@effect/platform`、`Schema` 統合、3.x と 4.x          | 版の系統と隣接パッケージ                                  |
| `This Repository`(任意)         | 概念と配置の対応表                     | なし                                       | `Context.Tag` → `application/ports/`、…                | 学習の場となるリポジトリがあるときだけ                    |
| `Final Goal`                    | 到達状態と「メンターとして振る舞う」   | エラーを読める、所有権をイメージできる、…  | 型を読める、失敗と欠陥を区別できる、…                  | 5 項目前後                                                |

## 技術の種類による差し替え

### 静的型付け言語(Rust、Go、Haskell、Swift など)

- `Compiler Perspective` はコンパイラの視点にする。最初に出会うエラーはコンパイルエラーである。
- メンタルモデルの柱は、メモリと所有、型システム、並行モデル、エラー処理の方式から選ぶ。
- 図はメモリ配置、所有の移動、型の関係を中心にする。

### 動的型付け言語(Python、Ruby、JavaScript など)

- `Compiler Perspective` は「インタープリタ / ランタイムから見ると」にする。最初に出会うエラーは実行時エラーであり、トレースバックの読み方を `Error Explanation` に含める。
- `Type Explanation` は「値の種類と構造」の説明に置き換える。
- 図はオブジェクトの参照関係、スコープ、呼び出しの流れを中心にする。

### ライブラリ・フレームワーク(Effect、React、Django、Rails など)

- 土台の言語は知っている前提にし、`Target User` で線を引く。
- `Compiler Perspective` は、型のあるライブラリなら型検査の視点、無ければランタイムの視点にする。
- 版差を必ず扱う。学習対象の版と、資料が別の版である可能性を `エコシステムの節` に書く。
- 「そのライブラリを使わないとどうなるか」を `Questions From Beginners` で扱う。

### ツール・CLI(Git、Nix、Docker、Terraform など)

- コード例はコマンドとその出力にする。「コマンドの意味」を全節で説明する。
- メンタルモデルの柱は、内部の状態モデル(Git のオブジェクトグラフ、Nix のストア、Docker のレイヤー)にする。
- 図は状態遷移とデータの流れを中心にする。
- 「取り消せるか」「壊すか」を `危険に見える機能の節` で扱う。

## ファイル名と見出し

- ファイル名は `<slug>-teacher.md`(例: `rust-teacher.md`、`effect-teacher.md`)。
- 1 行目の見出しは `# Xを超絶丁寧に教えてくれる君.md`。X は一般的な表記にする(`Rust`、`Effect.ts`、`Git`)。
