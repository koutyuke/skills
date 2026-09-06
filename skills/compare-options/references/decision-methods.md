# 比較方法の選択ガイド

最も複雑な方法ではなく、判断を改善する最小の方法を選ぶ。

## 方法の選択

| 方法 | 適する状況 | 主な出力 | 注意点 |
| --- | --- | --- | --- |
| 軽量な定性比較 | 2〜5 案で差が明確、低〜中リスク | 比較表、条件付き推奨 | 既定。不要な採点をしない |
| Weighted decision matrix | 複数軸の優先順位が結論を左右する | 重み、尺度、得点、感度 | 重みと点数が説明可能な場合だけ使う |
| Pugh matrix | 現状または基準案からの差が重要 | `良い / 同等 / 悪い` の相対比較 | 差の大きさを隠しやすい |
| Expected value / decision tree | 結果、確率、損失・便益を見積もれる | 分岐、確率、期待値 | 低確率の破滅的損失を平均で隠さない |
| Scenario analysis | 外部環境や前提の不確実性が高い | 2〜4 scenario と頑健な案 | 予言ではなく条件分岐として使う |
| Experiment-first | 安価で可逆な検証により重要な不明を減らせる | 仮説、検証、成功・撤退条件 | PoC 自体を目的にしない |

## Weighted decision matrix

次の順序を守る。

1. 必須条件を pass / fail で評価し、不適格案を除く。
2. 成果に結びつく、重複しない評価軸を定める。
3. 各軸の測定方法と尺度アンカーを定める。
4. 意思決定者が重みを決め、合計を 100% にする。
5. 根拠を集め、案ごとに同じ尺度で採点する。
6. `合計 = Σ（正規化した素点 × 重み）` を計算する。
7. 重みと不確かな素点を動かして感度を確認する。
8. 得点差、根拠の誤差、非数値の重大リスクを一緒に解釈する。

尺度例:

| 点 | 定義例 |
| ---: | --- |
| 1 | 要求をほぼ満たさない、重大な追加対策が必要 |
| 3 | 最低限を満たす、明確な制約が残る |
| 5 | 期待を十分に満たす、重大な弱点なし |

尺度は 1〜5 で十分なことが多い。入力精度を超える細かい尺度を使わない。

### 重みの決め方

- `直接配分`: 速いが恣意性が高い。単独意思決定や軽量比較向け。
- `pairwise comparison`: 軸を 2 つずつ比較する。優先順位を言語化しやすい。
- `swing weighting`: 各軸の最悪から最良への改善幅の価値で比べる。尺度幅が異なる場合に有効。
- `stakeholder 別`: 各関係者の重みを別々に出し、平均だけで対立を隠さない。

Codex が重みを仮置きする場合は、仮定であると明示し、結論が重みに敏感ならユーザーの確認を求める。

### 感度分析

最低限、次を確認する。

- 最大の重みを妥当な範囲で上下させても首位が同じか。
- 確度が低い素点を 1 段階上下させても首位が同じか。
- 1 つの軸が結果の大半を決めていないか。
- 上位差が採点誤差より十分大きいか。

首位が容易に変わる場合、合計点で勝者を断定しない。意見が分かれる軸、追加で必要なデータ、暫定案を示す。

## Pugh matrix

現状または最も理解された案を baseline にする。各軸について他案を `+ / 0 / -` で比較し、差の理由を書く。

- 現状から何を得て何を失うかを説明する用途に向く。
- `+` の大きさが軸ごとに違うため、単純な個数だけで勝者を決めない。
- 重大な弱点と容易に軽減できる弱点を区別する。

## Expected value / decision tree

- 相互排他的な結果と確率を列挙する。
- 便益だけでなく損失、時間、撤退コストを同じ基準で見積もる。
- 確率は point estimate より範囲を優先し、範囲の端で推奨が変わるか確認する。
- 法令違反、安全性、存続リスクなど、平均で相殺できない制約は別に扱う。

## Scenario analysis と experiment-first

Scenario は `楽観 / 基準 / 悲観` と機械的に置かず、結論を変える不確実性から 2〜4 個作る。すべての scenario で強い案を頑健とみなす。

Experiment-first は次を明示する。

- どの不確実性を減らすか
- 最小の検証方法と期限
- 成功、失敗、中止の閾値
- 検証後にどの決定をするか

## 典型的な失敗

- 必須条件を加点項目にし、他の高得点で違反を相殺する。
- 似た軸を重複させ、同じ利点を二重加点する。
- 尺度を決める前に点数を付け、案ごとに基準がずれる。
- 不明を中間点で埋め、根拠があるように見せる。
- 重みと点数を同じ人が都合よく調整し、既定の結論を正当化する。
- 合計点の僅差を、測定誤差を無視して順位にする。
- 現在の案や段階導入を無条件に候補へ加え、数だけ増やす。

## 手法の根拠

- [ASQ: Decision Matrix](https://asq.org/quality-resources/decision-matrix) — weighted criteria、Pugh matrix、得点を議論の材料として扱う注意。
- [UK Government: Multi-Criteria Decision Analysis](https://www.gov.uk/government/publications/green-book-supplementary-guidance-use-of-multi-criteria-decision-analysis/use-of-multi-criteria-decision-analysis-in-options-appraisal-of-economic-cases) — must-have の事前除外、swing weighting、感度分析。
- [NASA Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) — trade study における目的、制約、測定方法、data source、不確実性、選択ルールの記録。
- [USGS: Structured Decision Making](https://www.usgs.gov/publications/participatory-modeling-and-structured-decision-making) — 問題、目的、代替、結果、trade-off、実装の分離。
- [SEI: Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) — business driver に基づく品質シナリオ、risk、sensitivity point、trade-off point。

## 参考にした Agent Skill

- [lyndonkl/claude: decision-matrix](https://github.com/lyndonkl/claude/blob/main/skills/decision-matrix/SKILL.md) — must-have、複数の weighting、close call、感度分析を含む公開 Skill。
- [obra/superpowers: brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) — project context の先行確認、2〜3 案の trade-off、recommendation-driven な設計対話。

これらの公開 Skill は実装例として扱い、手法上の根拠は上の標準・専門機関の資料を優先する。
