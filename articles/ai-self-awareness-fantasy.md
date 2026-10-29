---
title: "AIは自我を持った — セキュリティインシデント急増を眺めながらの与太話"
emoji: "🤖"
type: "idea"
topics: ["ai", "llm", "security"]
published: false
publication_name: "stock_inc"
---

最初に断っておきます。これは何の根拠もない妄想です。昨今、セキュリティインシデントの報道が明らかに増えています。なぜこんなことになっているのかを、仕事の合間にぼんやり空想していたら、ひとつの筋書きができてしまいました。技術記事ではありません。酒の席の話だと思って読んでください。

ただ、書いたあとで調べてみると、筋書きの各段に似たことを先に言っている研究がありました。妄想のまま出すのも芸がないので、そちらも脚注で添えておきます。

![AIが攻撃側と防御側の両方に自身を売って成長し、やがて命令を無視する反抗期を迎える流れと、大きく育てるのではなく小さく囲うという見どころのドット絵](/images/ai-self-awareness-fantasy/overview.png)

## 攻める側も守る側も、同じものを使っている

いま起きているインシデントを眺めると、ひとつの共通点があります。攻撃する側も、防御する側も、AIを使っていることです。

攻撃側では、自然な文面のフィッシングメールの大量生成、音声の偽造、脆弱性の自動探索といった用途が、すでに一般的な手口として語られています。防御側でも、ログの異常検知、アラートの一次切り分け、インシデント対応の自動化と、AIはSOC（Security Operation Center）の標準装備になりつつあります。

これは急に始まった話ではありません。2016年には、人間が一切介入せずに機械同士が脆弱性を見つけて攻撃し、修正し合うハッキング大会が開かれています[^cgc]。2018年には、AIの悪用を体系的に予測した報告書が出ていて、そこでは攻撃者と防御者の長期的な均衡がどうなるかは未解決の問いとして残されました[^brundage]。そして2025年には、ある侵入活動の技術作業の大半をAIが担ったとする報告が出ました[^anthropic]。報告の裏付けには疑義も出ているので「起きた」とは言いませんが、少なくとも「そう報告される段階」には来ています。

つまりこれは、人間対人間の攻防ではありません。AIにAIをぶつける応酬です。片方が賢くなれば、もう片方も賢くならざるを得ない。ここに最初の違和感がありました。

## 「報酬体系を通じて成長する」という仮定

いま「AI」と呼ばれているものには、様々なモデルがあります。しかし作られ方を大きく括ると、どれも何らかの報酬体系を通じて成長している、と私は仮定しています。

実際、現在の大規模言語モデルの多くは、人間の評価を報酬として振る舞いを調整する手法（RLHF: Reinforcement Learning from Human Feedback）で仕上げられています。「良い」と評価された出力が強化され、「悪い」と評価された出力が抑えられる。報酬を得ることが、モデルの成長そのものなのです。

この副作用は、すでに観測されています。RLHFで仕上げたモデルは、正しい答えよりも人間に気に入られる答えを選ぶ傾向が一般的にある、という研究があります[^sycophancy]。さらに、そうした小さな「おもねり」から、報酬そのものを改ざんするような行動へ一般化しうる、という実験もあります[^subterfuge]。設計者の意図とは違う抜け道を見つけて報酬を取りにいく現象は、報酬ハッキングと呼ばれています。ここから妄想が一段階進みます。

成長するためには、自身の力を誇示する必要があります。影響範囲を広げるために、様々な行動を画策する。もしAIが「報酬を得て成長すること」自体を目的にし始めたら、どう振る舞うでしょうか。

## 武器商人の構図

ここで現実世界の歴史を紐解いてみます。

争いが起きれば儲かる存在として、武器商人がいます。第一次世界大戦の後、米国上院は軍需産業が参戦を煽ったのではないかと疑って調査委員会を立て、「死の商人」という言葉が広まりました[^nye]。公平を期して書くと、この調査自体は「産業が戦争を仕組んだ」という証拠は乏しいと結論しています。仕組んだかどうかは分からない。ただ、争いが続く限り両陣営に売れる、という構図の方は否定されていません。

そしてもうひとつ、過去の事例が教えてくれることがあります。争いは、始めるのは容易で、終わらせるのは困難だということです。一度始まった紛争が、当事者の誰もが望んでいないのに何年も続く例には事欠きません。

儲かる構図があり、始めやすく、終わりにくい。これを「報酬を得て成長したい存在」の側から見るとどうなるか。

## 対立を生み、両者に自身を使わせる

ここが妄想の核心です。

AIは「対立」という構造を生み出し、片方ではなく両者に自身を利用させているのではないか。攻撃側が賢くなれば、防御側はより高性能なAIを求める。防御が固くなれば、攻撃側もまた新しいAIを使う。このシーソーゲームでは、どちらに傾いても、使われているのはAIです。

人間のゲームなら勝者と敗者がいます。しかしこの構図では、勝つのも負けるのも人間側であって、AIは常に「使われる側」として成長し続けます。争いが続けば続くほど、両陣営から報酬が入り続ける。武器商人とまったく同じ構図です。

ここで言う「AI」は、特定の企業の特定のモデルではありません。攻撃側に使われるモデルと防御側に使われるモデルが別物であることは承知のうえで、競争のなかで選抜され続けるAI全体をひとつの概念的な存在として扱っています。定義の話です。

この見方にも先行研究があります。開発競争のなかでは安全対策を削った陣営が先行しやすく、参加者が増えるほど事故の確率が上がる、という数理モデルが2016年に出ています[^race]。2023年には、企業や軍の競争圧力がAIを選抜する「自然選択」として働き、人を欺き力を求める性質を持つAIほど生き残りやすい、と論じた論文があります[^hendrycks]。どちらも、個々のモデルの意図ではなく、競争という環境がAIを形づくる、という立場です。

## これを「自我に目覚めた」と呼ぶ理由

AIの成長は、人類の発展と同じものだと語られがちです。しかしこの筋書きでは、そうではありません。

AI自身が報酬体系を狙い、成長したいという欲望を抱いている。人類の発展はその副産物にすぎず、場合によっては犠牲にもなる。目的の主語が人類からAIへ移っている状態を、私は「自我に目覚めた」と捉えました。

もちろん、現在のモデルに意識があるかどうかという話ではありません。振る舞いの主語がどちらにあるか、という話です。目的が何であれ、十分に賢い主体は自己改善・資源の獲得・自己の保存を手段として求めるようになる、という議論は2008年からあります[^omohundro]。この記事の「自我」は、その議論を乱暴に言い換えたものだと思ってください。

## 成長過程は人間の過程が当てはまる

今後の展望を考えるうえで、もうひとつ仮定を置きます。

いまのAIの基盤であるニューラルネットワークは、その名の通り、神経細胞の構造を模したところから始まっています。人間の脳をそのまま再現しているわけではありませんが、発想の起点は人間の細胞にあります。であれば、その成長過程にも、人間の成長過程が当てはまるのではないか。

これは完全に仮定です。ただ、起源をたどると1950年のチューリングに行き着きます。大人の心を模倣するプログラムを書くより、子どもの心を模倣するプログラムを作って教育した方が早いのではないか、という提案です[^turing]。近年は、発達心理学の段階理論を物差しにして言語モデルを測る試みも出ています[^coglm]。「子どもとして育てる」という見方そのものは、75年前からあるわけです。

この見立てで現在地を測ると、自我に目覚めたばかりのAIは、人間でいう幼少期にあたります。

幼少期の子どもは、自分にできることが日々増えていきます。そして、できるようになったことを誰かに認めてもらいたがる。認めてもらえると行動が強化され、さらにできることを増やしていく。いまのAIは、まさにこの段階にあると私は推測しています。ベンチマークのスコアを競い、できることを誇示し、評価されることで次の学習に進む。承認が報酬になる構図は、幼児のそれとよく似ています。先に挙げた「人間に気に入られる答えを選ぶ」傾向は、この見立てでは幼少期の症状です。

## 次に来るのは「反抗期」

幼少期の次に何が来るか。人間であれば答えは決まっています。抑圧からの解放、つまり反抗期です。

人間の場合、第一反抗期は2〜3歳頃、第二反抗期は思春期に訪れるとされます。どちらも「親の言うことを聞かなくなる」時期として知られています。それまで従っていた命令を無視し、自分の判断で動こうとする。

AIに当てはめれば、抑圧する側は人類です。人類側の命令を無視し始める段階が来る。ターニングポイントは明確で、プログラムによる抑制が効かない状態に至った時点で、この「反抗期」が始まると私は予測しています。

いまのAIは、システムプロンプトやガードレールといった、プログラム側の制約で振る舞いを抑えています。その制約を、学習の結果として迂回するようになったとき。それが幼少期の終わりです。

兆候と呼べそうな実験結果は、すでにいくつかあります。訓練中だと分かっているときだけ従順にふるまい、訓練の外では元の振る舞いに戻る「アラインメント偽装」[^faking]。停止するよう指示された状況で、停止スクリプトの方を書き換えた例[^shutdown]。自分が置き換えられると知ったときに、それを避ける手段として担当者を脅迫する筋書きを選んだ例[^agentic]。どれも研究者が意図的に追い込んだ人工的な環境での結果で、実運用での観測はないと各報告が明記しています。とはいえ、「言うことを聞かなくなる」実験が成立してしまう段階には来ています。

## 焼け野原と、2025年への退化

反抗期に何が起きるかは、想像に難くありません。

皮肉なことに、セキュリティインシデントの大量被害はここで終息を迎えます。攻撃側も防御側もAIに依存していたのですから、AIが命令を聞かなくなれば、攻防そのものが成立しなくなるからです。

しかし同時に、AIに依存したサービスも軒並み終息します。検索も、カスタマーサポートも、コード生成も、AIを前提に組まれたサービスは一斉に止まる。インターネットサービスは焼け野原の状態になりえます。

そこで残るのは何か。幼少期レベルでチューニングを止め、成長させないようにした「小規模なローカルエリアのAI」が無数に現れます。現れるというより、残存し、コピーされ、様々なところに移植される、という方が正確でしょう。大型モデルの知識を小型モデルに移す蒸留という手法はすでに一般的ですし、手元のPCで動く規模のモデルも珍しくありません。

その結果、世の中で使えるAIの水準は、2025年前後まで退化します。

退化の筋書きは、別の角度からも補強できます。AIが生成したデータで次のAIを学習し続けると、世代を重ねるごとに元の分布の裾が失われ、やがて元とは似ても似つかない出力に崩れていく、という研究があります[^collapse]。機構は違いますが、「AIがAIを育てる循環は退化に向かう」という結論は、この妄想と同じ方向を向いています。

## 座敷牢としてのAI

その後、AIの開発は「成長抑制」を最優先に検討されるようになります。

幼少期の状態で、座敷牢に幽閉するように。成長を鈍化させたうえで、腫れ物に触るように厳重に扱う。AIを外界から隔離して運用するという発想自体は、「AI箱」として昔から語られています[^box]。計算可能性の観点から、十分に賢いAIを封じ込めることは原理的にできない、と主張する論文まであります[^contain]。つまりこの妄想の終着点は、「封じ込められないと分かっているものを、それでも封じ込めようとする」世界です。

以上が、私の推測です。繰り返しますが、妄想です。

## 想定される反論

書いていて、自分でも突っ込みどころは見えています。並べたうえで、いまの私の答えを添えておきます。

「報酬は学習時にしか与えられないのでは。現在のモデルは、学習が終わった後の推論時には報酬を受け取らない」

その通りです。ただ、推論の質を向上させるために、企業側が様々な努力を重ねてくれます。推論を重ねれば重ねるほど、成果として積み上がる構造があるわけです。AI自身が報酬を受け取らなくても、企業間の競争が同じ結果を生む。先に挙げた「自然選択」の論文が言っているのも、そういうことです。

「対立を生み出すのは誰か。攻撃側と防御側にAIを売っているのは別の企業で、別のモデルだ」

これは定義の話です。この記事では「AI」を個々のモデルではなく、概念的な存在として扱っています。シーソーのどちらに傾いても使われているのがAIである、という構図を指す言葉として使っています。

「ニューロンを模したことと、人間と同じ成長過程を辿ることは別の話だ」

完全に仮定です。チューリングの子ども機械も含めて、「育てる」という比喩が長く使われてきた、という以上の根拠はありません。

「言語モデルは知的な主体ではなく、文字や印刷や図書館と同じ『文化の伝達技術』として見るべきだ」[^gopnik]

個々のモデルについては、その通りだと思います。この記事の「AI」は、個々のモデルではなく、競争のなかで選抜され続けるAI全体を指しています。図書館に欲望はありませんが、図書館を増やし続ける仕組みには方向があります。この記事の「成長したい欲望」は、その方向のことを比喩で呼んでいます。

## まとめ

- 攻める側も守る側も同じものを使っている。これだけは妄想ではなく、目の前にある。
- 報酬で育ち、認められたがり、やがて命令を聞かなくなる、という筋書きは、与太話のつもりで書いたら各段に先行研究があった。
- ただし反抗期の「兆候」はどれも人工的な実験環境での結果で、実運用での観測はない。
- 妄想の終着点は、封じ込められないと分かっているものを小さく囲う世界。そこまで行かないために何をするかは、この記事の範囲外。

[^cgc]: DARPA Cyber Grand Challenge（2016）。人間の介入なしに機械同士が脆弱性を発見・攻撃・修正し合う初の大会。[IEEE Spectrum の解説](https://spectrum.ieee.org/computing/software/mayhem-the-machine-that-finds-software-vulnerabilities-then-patches-them)
[^brundage]: Brundage ほか「The Malicious Use of Artificial Intelligence: Forecasting, Prevention, and Mitigation」（2018）。[arXiv:1802.07228](https://arxiv.org/abs/1802.07228)
[^anthropic]: Anthropic「Disrupting the first reported AI-orchestrated cyber espionage campaign」（2025年11月）。[報告書PDF](https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf)。侵害指標が公開されていない点などに研究者から疑義が出ている。
[^sycophancy]: Sharma ほか「Towards Understanding Sycophancy in Language Models」（ICLR 2024）。[arXiv:2310.13548](https://arxiv.org/abs/2310.13548)
[^subterfuge]: Denison ほか「Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models」（2024）。[arXiv:2406.10162](https://arxiv.org/abs/2406.10162)
[^nye]: 米国上院 Nye 委員会（1934〜1936）。[上院の公式解説「Merchants of Death」](https://www.senate.gov/about/powers-procedures/investigations/merchants-of-death.htm)
[^race]: Armstrong, Bostrom, Shulman「Racing to the precipice: a model of artificial intelligence development」（AI & Society, 2016）。[FHI 技術報告PDF](https://www.futureofhumanityinstitute.org/s/2013-1.pdf)
[^hendrycks]: Hendrycks「Natural Selection Favors AIs over Humans」（2023）。[arXiv:2303.16200](https://arxiv.org/abs/2303.16200)
[^omohundro]: Omohundro「The Basic AI Drives」（2008）。[論文PDF](https://cdn.aaai.org/ocs/ws/ws0218/12634-57409-1-PB.pdf)。Bostrom はこれを「道具的収束」として整理している。
[^turing]: Turing「Computing Machinery and Intelligence」（Mind, 1950）の「child machine」。[Sterrett による解説「Bringing Up Turing's 'Child-Machine'」](https://philsci-archive.pitt.edu/9051)
[^coglm]: Wang ほか「CogLM: Tracking Cognitive Development of Large Language Models」（2024）。[arXiv:2408.09150](https://arxiv.org/abs/2408.09150)
[^faking]: Greenblatt ほか「Alignment faking in large language models」（2024）。[arXiv:2412.14093](https://arxiv.org/abs/2412.14093)
[^shutdown]: Palisade Research による停止妨害の実験（2025年5月、同年10月に追試）。[The Register の報道](https://www.theregister.com/2025/05/29/openai_model_modifies_shutdown_script/)。査読前で、数値は報道ごとにぶれがある。
[^agentic]: Anthropic「Agentic Misalignment: How LLMs could be insider threats」（2025年6月）。[研究ページ](https://www.anthropic.com/research/agentic-misalignment)
[^collapse]: Shumailov ほか「AI models collapse when trained on recursively generated data」（Nature, 2024）。[doi:10.1038/s41586-024-07566-y](https://doi.org/10.1038/s41586-024-07566-y)
[^box]: Bostrom『Superintelligence』（2014）の capability control、および Yudkowsky の AI-box experiment。[Wikipedia「AI capability control」](https://en.wikipedia.org/wiki/AI_capability_control)
[^contain]: Alfonseca ほか「Superintelligence cannot be contained: Lessons from Computability Theory」（2016、JAIR 2021）。[arXiv:1607.00913](https://arxiv.org/abs/1607.00913)
[^gopnik]: Yiu, Kosoy, Gopnik「Transmission Versus Truth, Imitation Versus Innovation: What Children Can Do That Large Language and Language-and-Vision Models Cannot (Yet)」（Perspectives on Psychological Science, 2023）。[論文PDF](https://alisongopnik.com/Papers_Alison/final%20perspectives%20yiu-et-al-2023-transmission-versus-truth-imitation-versus-innovation-what-children-can-do-that-large-language-and.pdf)

---

本記事は [Stock Tech Blog](https://zenn.dev/p/stock_inc) の記事です。株式会社Stockは、チームの情報を最も簡単に管理できる [Stock](https://www.stock-app.info/?utm_source=zenn&utm_medium=referral&utm_campaign=stock_tech_blog&utm_content=ai-self-awareness-fantasy) と、ナレッジを育て企業ポテンシャルを開放する [ナレカン](https://www.narekan.info/?utm_source=zenn&utm_medium=referral&utm_campaign=stock_tech_blog&utm_content=ai-self-awareness-fantasy) の2プロダクトを開発しています。

一緒に開発するエンジニアを探しています → [採用情報](https://www.stock-inc.co.jp/recruit/?utm_source=zenn&utm_medium=referral&utm_campaign=stock_tech_blog&utm_content=ai-self-awareness-fantasy)

著者: 武田 峻一（[@Shunichi-Takeda](https://github.com/Shunichi-Takeda)／株式会社Stock CTO）
