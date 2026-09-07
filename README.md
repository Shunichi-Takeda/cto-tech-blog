# Stock Tech Blog

株式会社Stock CTO・武田峻一が執筆する技術記事のリポジトリです。記事は Zenn Publication [stock_inc](https://zenn.dev/p/stock_inc) に公開されます。

## 構成

```
articles/
├── <slug>.md        # 公開記事（ファイル名 = Zenn の slug）
├── drafts/          # 執筆中の草案（Zenn からは無視される）
└── published/
    └── INDEX.md     # 公開済み記事の索引（自動生成）
config/zenn.json     # publication 設定・カテゴリ/タグのマッピング・著者フッタ
scripts/             # 草案の変換、frontmatter 検証、索引の生成
templates/           # 記事テンプレート
```

## 記事一覧

[articles/published/INDEX.md](./articles/published/INDEX.md) を参照してください。

## ワークフロー

```
articles/drafts/ ─→ articles/<slug>.md ─→ PR ─→ Zennの下書き ─→ レビュー ─→ published: true で merge ─→ 公開
     草案作成      Zenn形式へ変換      push時点で自動デプロイ            体裁・校正        CTOが判断
```

```bash
npm install                                                  # 初回のみ（zenn-cli）
python3 scripts/draft_to_zenn.py articles/drafts/<草案>.md   # 草案 → Zenn形式へ変換
python3 scripts/validate_zenn.py                             # frontmatter・公開ガードの検証
npm run preview                                              # http://localhost:8000 で表示確認
python3 scripts/sync_stage.py                                # 草案の stage を実態に同期
python3 scripts/update_index.py                              # 公開済み索引の再生成（merge後にmainで）
```

手順の詳細は [PUBLISHING.md](./PUBLISHING.md)、執筆規約は [AGENTS.md](./AGENTS.md) を参照してください。

## 運用上の注意

**`articles/` 直下の記事ファイルは移動・リネームしない。** ファイル名がそのまま Zenn の記事 slug（＝公開URL）になっており、リポジトリから消しても Zenn 側の記事は消えません。

**`articles/drafts/` に置いてよいのは「公開すると決めたもの」だけ。** 本リポジトリは public なので、Draft PR であっても草案は誰でも読めます。書くと決めていないネタ、公開留保がかかったもの、取り下げたものは非公開リポジトリで別管理しています（[AGENTS.md](./AGENTS.md) §2）。

**まとめて予約投稿しない。** Zenn には投稿数のレートリミットがあり、超過分はデプロイ失敗にならず下書きのまま残るため気づけません（[PUBLISHING.md](./PUBLISHING.md) §5.1）。

## ライセンス

記事本文の著作権は株式会社Stockに帰属します。
