# 公開済み記事の索引

Zenn へ公開した記事の一覧。**記事ファイル本体は `articles/` 直下から移動しない**（移動・削除しても Zenn 側の記事は消えず、運用が壊れるため）。

**公開日が未来日の記事は予約投稿である**（`published_at` の日時に公開される）。それまで公開URLは開けない。

**この表は手で編集しない。** 公開PRを並行させると衝突するため、merge 後に main で次を実行して再生成する。

```bash
python3 scripts/update_index.py
```

| 公開日 | タイトル | 記事ファイル | 公開URL |
|---|---|---|---|
| 2026-08-27 | PostgreSQLメジャーアップグレードの手順書に、ANALYZEを書き忘れない | [articles/postgres-major-upgrade-checklist.md](../postgres-major-upgrade-checklist.md) | https://zenn.dev/stock_inc/articles/postgres-major-upgrade-checklist |
| 2026-08-27 | そのロールバック、効いていません — ECSタスク定義のリビジョンを戻しても戻らない話 | [articles/ecs-task-definition-rollback-illusion.md](../ecs-task-definition-rollback-illusion.md) | https://zenn.dev/stock_inc/articles/ecs-task-definition-rollback-illusion |
| 2026-09-02 | 完成版を学習させても精度は上がらない — 暗黙知は「作り方」で渡す | [articles/transferring-tacit-knowledge-to-ai.md](../transferring-tacit-knowledge-to-ai.md) | https://zenn.dev/stock_inc/articles/transferring-tacit-knowledge-to-ai |
| 2026-09-09 | 検索ヒット率をLLMで底上げしつつコストを抑える『安価モデル事前スクリーニング』設計 | [articles/cheap-model-prescreening-search.md](../cheap-model-prescreening-search.md) | https://zenn.dev/stock_inc/articles/cheap-model-prescreening-search |
| 2026-09-16 | AIで採用スクリーニングする前に — 個人情報を守る匿名化前処理パイプライン | [articles/anonymization-pipeline-before-ai-screening.md](../anonymization-pipeline-before-ai-screening.md) | https://zenn.dev/stock_inc/articles/anonymization-pipeline-before-ai-screening |
| 2026-09-23 | スキャンPDFのOCRが「読めない」3つの理由 — エンジンを変えても直らない話 | [articles/scanned-pdf-ocr-blind-spots.md](../scanned-pdf-ocr-blind-spots.md) | https://zenn.dev/stock_inc/articles/scanned-pdf-ocr-blind-spots |
| 2026-09-30 | LLMにもEOLがある — モデルを依存ライブラリとして管理する | [articles/llm-model-eol-lifecycle-management.md](../llm-model-eol-lifecycle-management.md) | https://zenn.dev/stock_inc/articles/llm-model-eol-lifecycle-management |
| 2026-10-07 | AI活用の知見をClaude内に閉じ込めない — Claude Codeと実Chromeを『相乗り』させる | [articles/claude-code-chrome-extension-web-output.md](../claude-code-chrome-extension-web-output.md) | https://zenn.dev/stock_inc/articles/claude-code-chrome-extension-web-output |
| 2026-10-14 | AIエージェントが「見えない不具合」をどう見つけたか — PDFの透明テキストレイヤーを可視化で解決した話 | [articles/ai-agent-invisible-ocr-debug.md](../ai-agent-invisible-ocr-debug.md) | https://zenn.dev/stock_inc/articles/ai-agent-invisible-ocr-debug |
| 2026-10-21 | AIエージェントで「報告の手間ゼロ」のデイリーレポートを実現した話 | [articles/ai-agent-daily-report-zero-overhead.md](../ai-agent-daily-report-zero-overhead.md) | https://zenn.dev/stock_inc/articles/ai-agent-daily-report-zero-overhead |
