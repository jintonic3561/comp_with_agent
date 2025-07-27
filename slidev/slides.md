---
theme: seriph
colorSchema: light
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Serif JP'
  mono: 'Fira Code'
aspectRatio: 16/9
background: https://cover.sli.dev
title: 妙だな...をLLMに気付かせる
info: |
  データ分析コンペティションにおけるLLMの活用と、MCPサーバーを使った自律的データ探索の実現方法について
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

# 妙だな...をLLMに気付かせる

### MCPサーバで始めるデータと対話可能なAIの作り方

<div class="abs-br m-6 flex flex-col text-sm text-gray-400">
  <span>データ分析コンペ x コード生成AI 勉強会</span>
  <span>2025/07/27</span>
</div>


---
layout: image-right
image: https://tonic-slidev.s3.ap-northeast-1.amazonaws.com/comp_with_agent/yakushima.JPG
paddingLeft: 4rem
---

# 自己紹介

<div>
  <img src="/work/assets/kaggle_icon.png" class="w-1/2 mb-3">
</div>

## tonic [(@tonic3561)](https://x.com/tonic3561)

<br>

- 所属: 合同会社AlgoSphere 代表
- Kaggle: 万年Expert (5x🥈)
- 専門: 時系列予測


---
layout: default
---

# もくじ

<br>

1. コンペx生成AIの現在地
2. LLMが直面するデータ分析の壁
3. LLMにデータを「触らせる」挑戦
4. デモ: LLMによる自律的データ探索
5. まとめと展望


---
layout: section
---

# 1. コンペ x 生成AIの現在地


---
layout: default
transition: none
---

# LLMは既に優秀なアシスタント

データ分析コンペにおいて、LLMは様々な場面で利用可能


✅ 問題設定やデータの**説明**

✅ 仮説・アイディアの**壁打ち**

✅ 関連論文の**調査**

✅ アイディアの**実装**

✅ バグの**原因特定**

✅ **ベースライン**の構築


---
layout: default
---

# だが…あと一歩届かない！

<br>

✅ 仮説・アイディアの**壁打ち** ← ココ


仮説を立てるためには**データをよく見る**のが一番大切（？）だが、  
チャットベースのLLMではデータを「触る」ことが難しい


---
layout: section
---

# 2. LLMが直面するデータ分析の壁


---
layout: two-cols-header
---

# (人間が) 仮説・アイディアを考えるプロセス

::left::

## (1) EDA型

<br>

```mermaid
graph TD
    A[生データを眺める] --> B[加工・集約]
    B --> C["「妙だな…」"]
    C --> D[深掘り]
    D --> A
    
    style A fill:#ff6b6b,stroke:#333,stroke-width:3px
```

::right::

## (2) 仮説駆動型

<br>

```mermaid
graph TD
    E[仮説を立てる] --> F[分析・可視化]
    F --> G[結果を眺める]
    G --> E
    
    style G fill:#ff6b6b,stroke:#333,stroke-width:3px
```

→ 生データや可視化結果を**眺めながら**思考を回す


---
layout: default
---

# チャットLLMとの対話における「3つの壁」

<div class="grid grid-cols-3 gap-6 mt-8">

<div>

### (1) コンテキストの壁

<br>

- 巨大なデータはそもそも読み込んでもらえない

<img src="/work/assets/huge_data.png" class="w-full mt-4" />

</div>

<div>

### (2) 作業の壁

<br>

- LLMが生成したコードを、人間がコピペして実行
- 実行結果のファイル（CSVや画像）を、人間が確認  
- その結果やファイルを、人間がLLMに再入力

<img src="/work/assets/manual_work.png" class="w-full mt-4" />

</div>

<div>

### (3) 思考の壁

<br>

- 分析の「気づき」は、データを多角的に**眺める**中で生まれる
- LLMは人間が与えた断片的な結果しか見ることができない？

<img src="/work/assets/interrupted_thought.png" class="w-full mt-4" />

</div>

</div>


---
layout: section
---

# 3. LLMにデータを
# 「触らせる」挑戦

---
layout: default
---

# LLMにデータを触ってもらうには？

LLMが自律的に分析を進めるために必要なタスクを分解してみる

<br>

- 問題設計・データ構造を理解する → ✅ **できる**
- 集約・可視化コードを書く → ✅ **できる**
- 結果をファイル出力する → ✅ **できる**
- ファイル (csv, png) を読み込む → ✅ **できる**
- 読み込んだテキストや画像を解釈する → ✅ **できる**
- 上記を繰り返す → ✅ **できる**

<br>

<div class="text-center text-2xl font-bold mt-8">
⇒ 個別のタスクは実現可能。
</div>

<div class="text-center text-2xl font-bold text-red-500 mt-8">
あれれ～？
</div>

---
layout: default
---

# 作ってみました

claude codeとMCPサーバを活用して、自律的にEDAを行うエージェントを作りました

<br>

- **題材：** [Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)
- **Gitリポジトリ：** [https://github.com/jintonic3561/comp_with_agent](https://github.com/jintonic3561/comp_with_agent)

---
layout: two-cols-header
---

# 題材紹介： U.S. Drought Prediction

気象・土壌データから、専門家が作成する「干ばつマップ」の自動化を目指す予測タスク

::left::

## 入力データ

**時系列データ (気象):**
- 日々の気温、降水量、風速など
- 時系列方法に train / valid / test を分割

**静的データ (地理・土壌):**
- 郡ごとの標高、傾斜、土地の種類など
- **fips** (郡ID) で時系列データに左結合

::right::

## 予測タスク

**目的変数:**
- 干ばつの深刻度を表す **0〜5** の6段階カテゴリ

**評価指標:**
- **Macro F1 Score**
- **MAE**

<img src="/work/assets/drought.png" class="w-full mt-4" />

---
layout: default
---

# MCPサーバとは？

<br>

## ざっくり： 簡単に渡せる電卓みたいなもん

<br>

LLM（と人間）は暗算が苦手

→ 人間と同じように、LLMにも電卓とか渡してあげればいいんじゃない？

→ ほかにもいろんなツールを使ってもらおう！

<div class="grid grid-cols-3 gap-2 mt-2">

<div>
<img src="/work/assets/llm_with_tools.png" class="w-1/2 mx-auto mt-8" />
</div>

<div>

<br>

- 電卓
- ファイルアクセス
- Web検索
- ...

</div>

</div>