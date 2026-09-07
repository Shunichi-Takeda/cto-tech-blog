# PUBLISHING.md — Zenn 公開フロー

本リポジトリの草案を **Zenn Publication [`stock_inc`](https://zenn.dev/p/stock_inc)** に公開するための手順書。
マーケティング広報チームとすり合わせた運用体制（草案 → Zenn形式に変換 → `published: false` で PR → 体裁・校正レビュー → 承認後 `published: true` で merge → 公開）をそのまま実行できる形にしたもの。

> ⚠️ **本リポジトリは public である。** `articles/drafts/` に草案を置いた時点で、
> Draft PR であっても誰でも読める。**ここに置いてよいのは「公開すると決めたもの」だけ**である。
> 書くと決めていないネタ・公開留保がかかったもの・取り下げたものは非公開リポジトリで別管理する（AGENTS.md §2）。

---

## 1. ディレクトリの役割（リポジトリ分離後）

```
articles/
├── <slug>.md        ← ★ Zenn が読むのはここだけ。公開/下書き中の記事の正本
├── drafts/          ← 執筆中の草案（Zenn からは完全に無視される）
└── published/       ← 公開済みの索引（INDEX.md）。記事ファイルは移動しない
images/              ← 記事に貼る画像（Zenn の画像置き場）
```

Zenn の GitHub 連携は **`articles/` 直下の `*.md` だけ**を記事として扱う。サブディレクトリは走査されないため、`drafts/` を同じリポジトリに置いても Zenn には出ない（ただし GitHub 上では公開されている）。

判定オントロジー（公開可否の判定基準と文体判定）は非公開リポジトリにある。判定基準そのものが自社の弱点の所在を示すためである。

> ⚠️ **公開後に `articles/<slug>.md` を移動・削除しない。**
> ファイルを消しても Zenn 側の記事は消えず（削除はダッシュボードからのみ）、逆にファイルが残っていると復活しうる。
> したがって従来の「公開したら `published/` に移す」運用は成立しない。**公開済み記事も `articles/` 直下に残し、`articles/published/INDEX.md` に公開URLを追記する**方式に変えている。

## 2. Zenn 側の状態（2026-08-26 時点）

[デプロイ設定](https://zenn.dev/dashboard/deploys) で確認済みの内容。

| 項目 | 状態 |
|---|---|
| 連携アカウント | Zenn アカウント「株式会社Stock」（Publication **Stock Tech Blog** = `stock_inc` に所属） |
| 連携リポジトリ | `Shunichi-Takeda/cto-tech-blog`（本リポジトリ） |
| デプロイ対象ブランチ | `main` — main への merge が公開トリガー |
| PRで下書きデプロイ | **有効**（PRのブランチが下書きとしてデプロイされる。§2.1） |
| プラン | 無料（PRバナー等の Pro 機能は使えない） |

Publication への紐付けは frontmatter の `publication_name: "stock_inc"`（Zenn のダッシュボードが指定する値そのもの）。これが無いと個人アカウントの記事として公開されてしまうため、`scripts/validate_zenn.py` で必須チェックにしている。

過去のデプロイは「デプロイ成功 / 更新されたファイルはありません」で記録されている。`articles/` 直下に記事が無かったため（= `drafts/` は走査されない）で、想定通りの挙動である。

### 2.1 レビューの分担

体裁・校正レビューは **Zenn のレビュー機能**で行う。マーケティング広報チームが Zenn の実画面で確認できるため忠実度が最も高い。

| 役割 | 場所 | 見るもの |
|---|---|---|
| **体裁・校正レビュー** | **Zenn のレビューページ**（`https://zenn.dev/articles/<slug>/review`） | 実際の表示・文章の体裁 |
| 技術・公開ガードのレビュー | GitHub PR | 変換の正しさ、機密情報ガード、CI結果 |

**「PRで下書きデプロイ」が有効なので、merge しなくても PR のブランチが下書きとしてデプロイされる。** レビューのために main へ merge する必要はない（実測確認済み: ブランチ `article/<slug>` のデプロイで下書きが生成された）。

レビュアーは記事ごとに設定する（編集画面右サイドバー → 「レビュアーを追加する」）。**レビュアー設定は GitHub からのデプロイでは消えない。**
レビューページは行番号付きのソースが並び、**行または選択範囲にコメント**を付けられる（GitHub のレビューに近い操作）。「AIレビューを実行」ボタンもある。

> ⚠️ **無料プランではレビューコメントは1記事あたり3件まで。** 校正の指摘が多い記事では足りない。
> 運用としては「**3件に収まらない場合は1コメントにまとめる**」か、指摘だけ GitHub PR のコメントに出す。恒常的に足りなければ Pro プランを検討する。

> PR を merge せずに閉じても、デプロイ済みの下書きは Zenn 側に残る（コンテンツの削除はダッシュボードからのみ）。取り下げる場合はダッシュボードで削除する。

補助手段として GitHub PR の rich diff（Files changed → 「Display the rich diff」）も使えるが、Zenn 独自記法（`:::message` / `:::details` / `@[...]` / 数式 / mermaid）は描画されない。`scripts/validate_zenn.py` がそれらの使用を警告する。

## 3. 記事1本の流れ

### Step 1. 草案を書く

`articles/drafts/YYYY-MM-DD_slug.md` に、これまでの frontmatter 形式のまま書く。Zenn を意識する必要はない。

### Step 2. Zenn 形式に変換

```bash
python3 scripts/draft_to_zenn.py articles/drafts/2026-08-06_ecs-task-definition-rollback-illusion.md
```

このスクリプトが機械的に済ませること:

| 変換 | 内容 |
|---|---|
| frontmatter | `title` / `emoji` / `type` / `topics` / `published` / `publication_name` へ写す |
| emoji | `category` から自動決定（`--emoji 🚢` で上書き） |
| type | `category` から `tech` / `idea` を決定（`team` のみ `idea`） |
| topics | `tags` を `config/zenn.json` の `tag_to_topic` で変換、重複除去、**5件超は切り詰めて警告** |
| published | **常に `false`** で出力（公開は人のレビューを経てから） |
| 本文 | 先頭 H1 を削除（Zenn はタイトルを別に描画するため）、草案テンプレートの著者ブロックを除去 |
| 著者欄 | UTM付きリンクのフッタを付与（文面は `config/zenn.json` の `footer`） |
| 出力先 | `articles/<slug>.md`（`slug` は Zenn 制約 `a-z0-9 - _` の12〜50文字。満たさなければエラー） |
| 草案メタ | `stage` / `source_context` などは**持ち込まない**（Zenn は本文の HTML を解釈しないため、コメントが読者に表示されてしまう。草案との対応は slug で辿る） |

主なオプション: `--dry-run`（標準出力に出すだけ）、`--topics aws,ecs,cicd`、`--emoji`、`--type`、`--slug`、`--force`（上書き）。

### Step 3. 検証とプレビュー

```bash
python3 scripts/validate_zenn.py
npm install   # 初回のみ
npm run preview
```

`validate_zenn.py` が見るもの: slug 制約 / emoji 1文字 / type / topics 1〜5件 / published の真偽値 / `publication_name` の一致 / 社内URL・認証情報らしい文字列 / 本文分量（警告）。
`published: true` の記事には、`TODO` や `〇〇` などの置換漏れが残っていないかも見る。

> PR を出したら `python3 scripts/sync_stage.py` を実行し、草案側の `stage` を `review` にしておく。
> レビュー中の記事は PR ブランチ上にしかないため、これが main から状態を追う唯一の手がかりになる。

### Step 4. `published: false` のまま PR

```bash
git switch -c article/<slug>
git add articles/<slug>.md
git commit -m "article: <タイトル>（published: false）"
git push -u origin article/<slug>
gh pr create --base main --title "Tech Blog: <タイトル>"
```

push した時点で **Zenn がそのブランチを下書きとしてデプロイする**（デプロイ履歴にブランチ名で出る）。CI（`.github/workflows/zenn-validate.yml`）が `validate_zenn.py` を回す。

**この PR で見るのは技術面だけ**（変換が正しいか、機密情報ガードを通ったか、CI が通ったか）。

### Step 5. Zenn でレビュー（merge不要）

1. [記事の管理](https://zenn.dev/dashboard) → 該当記事の ✏️（編集）→ 右サイドバー「レビュアーを追加する」でレビュー担当を設定
2. レビュー担当は `https://zenn.dev/articles/<slug>/review` で行単位にコメント（無料プランは1記事3件まで）
3. 見た目だけ見せたい相手には ▶（プレビュー）→ 「このページを共有」でURLを渡す

| 共有範囲 | 誰が見られるか |
|---|---|
| **Publicationメンバー**（既定） | Stock Tech Blog のメンバーのみ |
| **リンクを知っている全員** | URL を渡した相手（Zenn アカウント不要） |

指摘の反映は **`articles/<slug>.md` を直して PR ブランチに push** する。push ごとに下書きが更新されるので、レビューはそのまま続けられる。

> 本文に手を入れたら、**草案（`articles/drafts/`）にも同じ修正を反映する。** 反映しないと、次に `draft_to_zenn.py` で再変換したときに修正が消える。

> ⚠️ Zenn の編集画面で本文や `published` を直さない。次のデプロイでリポジトリの内容に巻き戻る（画面上にも「この画面での編集は上書きされます」と警告が出る）。

### Step 6. 公開

Zenn レビューで承認が出たら、同じ PR に `published: true` のコミットを積んで merge する。**merge が公開のトリガー**（main のデプロイで初めて公開される）。

```bash
sed -i '' 's/^published: false$/published: true/' articles/<slug>.md
git commit -am "publish: <タイトル>" && git push
```

main に merge された時点で Zenn へデプロイ = 公開。公開後は main で索引を再生成する。

```bash
git switch main && git pull
python3 scripts/update_index.py     # articles/published/INDEX.md を再生成
git commit -am "docs: 公開済み索引を更新" && git push
```

> ⚠️ **`articles/published/INDEX.md` を公開PRの中で書き換えない。**
> 全記事が同じ表に1行ずつ追記するため、公開PRを2本以上並行させると必ず衝突する。
> 索引は公開PRから外し、merge 後に main で再生成する。

公開後、`python3 scripts/sync_stage.py` を実行し、草案の `stage` を `published`、`published_url` を記入する（main の公開状態を読んで自動で書き換える）。

> 公開日時を指定したい場合は frontmatter に `published_at: "2026-09-01 10:00"`（JST）を追加する。未来日時なら予約投稿になる。

## 3.1 公開済み記事を直す

誤字修正、内容の追補、リンク切れの対応。公開後の修正は必ず発生する。

```bash
git switch main && git pull
git switch -c update/<slug>-<内容>          # 例: update/postgres-counterarguments
# articles/<slug>.md と articles/drafts/<草案> の両方を直す
python3 scripts/validate_zenn.py
git commit -am "docs(article): <何を直したか>" && git push -u origin update/<slug>-<内容>
gh pr create --base main --title "📝 更新: <タイトル>（公開済み記事の更新）"
```

merge すると Zenn 上の記事が更新される（新規公開ではない）。`published: true` のままにする。

| 状況 | やり方 |
|---|---|
| **まだ merge していない記事** | 既存の PR にコミットを積む（`article/<slug>` ブランチ） |
| **公開済み記事の更新** | **新しい PR を作る**（`update/<slug>-<内容>` ブランチ） |

> ⚠️ **merge 済みの PR は再オープンできない。** GitHub でできるのは Revert だけである。
> 「Restore branch」でブランチは戻せるが、PR は MERGED のまま。公開済み記事の修正は必ず新しい PR になる。

> ⚠️ `articles/published/INDEX.md` は触らない。公開状態が変わらない更新では索引も変わらない。

**草案も同じ内容に直す。** 直さないと、次に `draft_to_zenn.py` で再変換したときに修正が消える。

## 4. 誰が何を決めるか

| 判断 | 担当 |
|---|---|
| 何を書くか・公開してよいか | CTO（非公開リポジトリのネタ管理と判定オントロジー） |
| 体裁・校正 | マーケティング広報チームのレビュー担当（**Zenn のレビュー機能**で実施） |
| `published: true` への変更 | 承認後に起案者が実施（AIエージェントは行わない） |
| 記事の削除・非公開化 | Zenn ダッシュボードから人が実施（リポジトリからの削除では消えない） |

## 5. 著者欄の UTM 付きリンク

`config/zenn.json` の `footer` が全記事のフッタを決める。現在の設定:

```
?utm_source=zenn&utm_medium=referral&utm_campaign=stock_tech_blog&utm_content=<slug>
```

| パラメータ | 値 | 理由 |
|---|---|---|
| `utm_source` | `zenn` | 流入元のプラットフォーム |
| `utm_medium` | `referral` | **GA4 のチャネル分類に合わせるため。** `techblog` のような独自値を入れると GA4 の既定チャネルグループに一致せず「Unassigned」に落ちる |
| `utm_campaign` | `stock_tech_blog` | 施策単位で固定。Tech Blog 全体の流入をまとめて見られる |
| `utm_content` | `<slug>` | 記事ごとの内訳。どの記事が効いたかを campaign の中で分解できる |

リンク先は2つ。フッタ文面ごと `config/zenn.json` の `footer.template` で管理している。

| リンク | 遷移先 | 備考 |
|---|---|---|
| Stock | `https://www.stock-app.info/` | チームの情報を最も簡単に管理できるツール |
| ナレカン | `https://www.narekan.info/` | ナレッジを育て企業ポテンシャルを開放するツール |
| 採用 | `https://www.stock-inc.co.jp/recruit/` | Tech Blog の目的（採用力向上）に直結する導線 |

> リンク先は `https://www.stock-app.jp/`（アプリ本体）ではなく `.info` のサービスサイトを使う。前者は既ログインユーザーがアプリにリダイレクトされる。

> Pro プランなら Publication の「PRバナー」機能で記事ページ下部にバナーを出せるが、現在は無料プランのため本文フッタで担保している。

## 5.1 予約投稿とレートリミット（まとめて公開しようとすると弾かれる）

frontmatter に `published_at: "YYYY-MM-DD HH:MM"`（JST）を書き、`published: true` で merge すると予約投稿になる。Zenn 側で「公開予約中 / MM/DD HH:MM に公開予定」と表示されれば成立している。

**ただし記事の投稿数には Zenn のレートリミットがある。** 判定は「**直近24時間以内の投稿数（投稿予約中を含む）**」で、上限値は不正防止のため非公開（[FAQ](https://zenn.dev/faq/rate-limit)）。

上限を超えた分は**デプロイが失敗するのではなく、その記事だけ黙って下書きのまま残る**。リポジトリ側は `published: true` なので、GitHub を見ても気づけない。デプロイ履歴に次のお知らせが出る。

> 次の記事は投稿数の上限に達したためデプロイされませんでした: `<slug>`, `<slug>`, ...

実測（2026-09-01）: 8本を同時に merge したところ、通ったのは2本のみで6本が弾かれた。

**運用**

- **まとめて予約しない。** 記事は公開日の数日前に1本ずつ merge する。週1本の頻度ならレートリミットには当たらない
- やむを得ず溜まった場合は、**24時間おきに手動デプロイ**（GitHub連携 → リポジトリ設定 → 手動デプロイ → main）を繰り返す。リポジトリ側は既に `published: true` なので、通った分から順に予約投稿になる
- **merge しただけで安心しない。** [記事の管理](https://zenn.dev/dashboard)で「公開予約中」になっているかを必ず確認する

## 6. その他

- 記事内に画像を使う場合は `images/<slug>/` 配下に置き、`![](/images/<slug>/foo.png)` で参照する。
- `books/.gitkeep` は、Zenn のデプロイ時に出る「booksディレクトリが見つかりませんでした」の通知を止めるためのもの（本は運用しない）。
