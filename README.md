# CTO Tech Blog

Stock社 CTO による技術ブログの記事管理リポジトリ。

## 概要

AIエージェントとの連携を通じて、日常の開発業務から技術的に発信・共有すべき内容を抽出し、Tech Blog の記事として昇華させるためのリポジトリです。

### 目的

- **メディア発信力の向上** — Stock社としての技術的プレゼンスを確立
- **採用力の向上** — エンジニア候補に対して技術力・開発文化を可視化
- **エンジニアの発信の場** — チームメンバーが技術的知見を社外に発信する基盤

## ディレクトリ構成

```
cto-tech-blog/
├── AGENTS.md              # AIエージェント向け運用ガイド
├── README.md              # 本ファイル
├── articles/
│   ├── ideas/             # 📝 記事アイデア（ネタ出し段階）
│   ├── drafts/            # ✏️ 草案（執筆中・レビュー前）
│   └── published/         # ✅ 公開済み記事アーカイブ
└── templates/
    ├── article_template.md    # 記事テンプレート
    └── idea_template.md       # アイデアテンプレート
```

## 記事ワークフロー

```
ideas/ ──→ drafts/ ──→ published/
 ネタ出し     草案作成     公開済み
```

1. **ネタ検出**: 業務中に技術的な発信価値のある要素を検出
2. **アイデア起票**: `articles/ideas/` にアイデアファイルを作成
3. **草案作成**: CTOの指示に基づき `articles/drafts/` に昇格・執筆
4. **レビュー**: CTO がレビュー・フィードバック
5. **公開**: 公開先プラットフォームへ投稿、`articles/published/` にアーカイブ

## 記事カテゴリ

| カテゴリ | 内容 |
|---|---|
| `engineering` | 実装・設計・パフォーマンス |
| `architecture` | アーキテクチャ・設計判断 |
| `devops` | インフラ・CI/CD・運用 |
| `ai-agents` | AIエージェント活用事例 |
| `team` | チーム運営・開発プロセス・採用 |
| `postmortem` | 障害対応・ポストモーテム |

## ファイル命名規則

```
YYYY-MM-DD_slug.md
```

例: `2026-06-23_ai-agent-daily-report-automation.md`

## AIエージェント連携

本リポジトリは `ai-knowledge` (横断ナレッジ) および `narekan-project-management` (プロジェクト管理) と連携し、開発業務から記事化すべき技術的要素を抽出します。

詳細は [AGENTS.md](./AGENTS.md) を参照してください。

## 技術スタック（記事の主な対象）

- **バックエンド**: Ruby on Rails / PostgreSQL
- **フロントエンド**: React / TypeScript
- **インフラ**: AWS (ECS, Aurora, S3, CloudWatch)
- **AI/ML**: LLM / MCP / RAG
- **開発プロセス**: AIエージェント活用 / CI/CD

---

> **Note**: 本リポジトリは記事の**草案管理**を目的としています。公開先プラットフォーム（Zenn, note, 自社メディア等）は別途決定します。