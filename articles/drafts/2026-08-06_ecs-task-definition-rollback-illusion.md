---
title: "そのロールバック、効いていません — ECSタスク定義のリビジョンを戻しても戻らない話"
slug: "ecs-task-definition-rollback-illusion"
author: "武田 峻一"
author_github: "Shunichi-Takeda"
date: "2026-08-06"
updated: "2026-08-07"
stage: "published"
tags:
  - AWS
  - ECS
  - ECR
  - CI/CD
  - devops
category: "devops"
description: "「ECSタスク定義を1つ前のリビジョンに戻す」を切り戻し手順にしていたが、実測するとリビジョン間の差分は0件だった。可変タグ参照でロールバックが成立しない仕組みと、その修正。"
source_context: "リリース手順の切り戻し方法を棚卸しした際、タスク定義リビジョンの差分を実測したところ0件であることが判明し、イメージ参照のバージョン固定に設計変更した。"
published_url: "https://zenn.dev/stock_inc/articles/ecs-task-definition-rollback-illusion"
---

# そのロールバック、効いていません — ECSタスク定義のリビジョンを戻しても戻らない話

リリース手順書に「問題があればタスク定義を1つ前のリビジョンに戻す」と書いてある組織は、かなり多いと思います。

ただ、その手順、条件によっては何も戻していません。

AWS ECS を使っているなら5分で自己診断できる話です。

## 「本当に戻るのか」に答えられなかった

きっかけは、切り戻し方法を棚卸ししていたときの素朴な疑問でした。「1つ前のリビジョンに戻す、で本当にコードが戻るのか？」

聞かれると答えられませんでした。手順に書いてあるし、そういうものだと思っていたけれど、実際に戻ったのを見たことがない。切り戻しは障害時にしか使わないので、平常時に確かめる機会がありません。

確認は差分を取るだけです。

```bash
aws ecs describe-task-definition --task-definition my-app:$(( N )) \
  --query 'taskDefinition.containerDefinitions' > cur.json
aws ecs describe-task-definition --task-definition my-app:$(( N - 1 )) \
  --query 'taskDefinition.containerDefinitions' > prev.json
diff cur.json prev.json
```

**差分は0件でした。**

## なぜ0件になるのか

タスク定義の `image` に何を書いているかが分かれ目です。こう書いていました。

```json
"image": "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/my-app:latest"
```

`:latest` のような可変タグを参照していると、リビジョンをいくつ積んでも文字列は毎回同じです。差分が出ないのは当然でした。

さらにECR側を見ると、タグの上書きが許可されていました。

```bash
aws ecr describe-repositories --repository-names my-app \
  --query 'repositories[].imageTagMutability'
# → [ "MUTABLE" ]
```

`MUTABLE` は「同じタグを別のイメージに付け替えられる」設定です。`:latest` はもちろん、`:v1.2.3` のようなバージョンタグでも後から中身をすり替えられる状態でした。

```
[rev.N  ]  image: .../my-app:latest ─┐
[rev.N-1]  image: .../my-app:latest ─┼→ ECR の :latest（常に最新を指す）
[rev.N-2]  image: .../my-app:latest ─┘
```

どのリビジョンでデプロイしても、ECSは同じ最新イメージを引いてきます。リビジョンを戻す操作が戻すのは、CPU・メモリ・環境変数といったメタデータだけ。アプリケーションコードは1バイトも戻りません。

言い方を変えると、これは「ロールバック手順が壊れていた」のではありません。そもそもロールバック手順ではなかった。壊れていたなら直せますが、最初から別の操作だったものは作り直すしかない。

## 何を選んだか

イメージ参照を不変にする方法は3つあります。

| 方法 | 長所 | 短所 |
|---|---|---|
| **A. バージョンタグ固定** | 既存フローへの変更が小さい。タグが読める | ECRが `MUTABLE` だと付け替えの余地が残る |
| **B. ダイジェスト固定** | 暗号学的に一意。最も強い | タグが読めず運用の見通しが悪い |
| **C. ECRを `IMMUTABLE` 化** | 根本対策。AとCの併用が理想 | 既存CIがタグを上書きしていると壊れる |

まずAを採りました。Cは既存パイプラインへの影響調査が要り、Bは見通しを悪くする。「今日から切り戻しが機能する状態」への最短距離を優先し、B・Cは継続課題にしました。

実装は、タスク定義を作るスクリプトがリリースバージョンを引数で受け取る形に変えるだけです。

```bash
# usage: create_revision v1.2.3
aws ecs describe-task-definition --task-definition "$FAMILY" --query 'taskDefinition' \
| jq --arg img "${REGISTRY}/${FAMILY}:$1" '
    .containerDefinitions |= map(.image = $img)
    | del(.taskDefinitionArn, .revision, .status, .requiresAttributes,
          .compatibilities, .registeredAt, .registeredBy)
  ' > taskdef.json

aws ecs register-task-definition --cli-input-json file://taskdef.json
```

これでリビジョンごとに `image` が変わります。リビジョンを戻す操作が、はじめてイメージを戻す操作になりました。切り戻しは通常のデプロイと同じ経路（`update-service` 1回）です。

副次的に、「どのリビジョンがどのリリースか」がタスク定義を見るだけで分かるようになりました。障害時の判断材料が1つ増えたことになります。

## 学び

**一度も実行していない復旧手順は、手順ではありません。**

手順書に書いてあること、レビューを通っていること、全員が「そうするもの」と認識していること。どれも動作の保証になりません。

しかも今回のように、壊れていることが平常時には一切観測できない欠陥があります。切り戻しが要るのは障害時だけなので、障害が起きるまで誰も気づけない。気づいたときには最悪のタイミングです。

同種の「効いていないつもりの安全策」は他にもあるはずだと考えて、次を継続課題にしています。

- ECRの `IMMUTABLE` 化
- ダイジェスト固定への移行検討
- **復旧手順を定期的に実行して確かめる仕組み**

3つ目が本質です。1つ目と2つ目を入れても、実行して確かめる工程がなければ、また別の形で同じことが起きます。ただ、これをどう仕組みにするかはまだ決めていません。本番相当の環境で切り戻しを定期実行するのが筋だとは思いつつ、その環境の維持コストに見合うかを判断できていない、というのが正直なところです。

## まとめ

- ECSタスク定義が可変タグを参照していると、リビジョンを戻してもコードは戻らない。
- 診断は `describe-task-definition` の差分を取るだけ。差分0件なら切り戻しは成立していない。
- 対策はイメージ参照の固定と、ECRの `IMMUTABLE` 化。
- 一般には、実行して確かめていない復旧手順は手順ではない。平常時に観測できない欠陥ほど、能動的に検証する必要がある。

---

> 著者: 武田 峻一（[@Shunichi-Takeda](https://github.com/Shunichi-Takeda)）
> Stock社 CTO
