# Stock Tech Blog

株式会社Stock CTO・武田峻一が執筆する技術記事のリポジトリです。記事は Zenn Publication [stock_inc](https://zenn.dev/p/stock_inc) に公開されます。

## 構成

```
articles/            # 公開記事（ファイル名 = Zenn の slug）
├── published/
│   └── INDEX.md     # 公開済み記事の索引（自動生成）
config/zenn.json     # publication 設定・カテゴリ/タグのマッピング
scripts/             # frontmatter 検証と索引の生成
```

## 記事一覧

[articles/published/INDEX.md](./articles/published/INDEX.md) を参照してください。

## ローカルでの確認

```bash
npm install
npm run preview     # Zenn CLI のプレビュー
npm run validate    # frontmatter と公開ガードの検証
npm run index       # 公開済み索引の再生成
```

## 運用上の注意

`articles/` 直下の記事ファイルは**移動・リネームしない**でください。ファイル名がそのまま Zenn の記事 slug（＝公開URL）になっており、リポジトリから消しても Zenn 側の記事は消えません。

## ライセンス

記事本文の著作権は株式会社Stockに帰属します。
