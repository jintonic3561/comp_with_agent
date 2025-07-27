# Comp with Agent: 自律的なコンペデータ分析エージェント

このプロジェクトは、[Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)を題材に、MCPを活用して自律的なデータ分析エージェントの構築を試みたものです。

## クイックスタート

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/jintonic3561/comp_with_agent
   cd comp-with-agent
   ```

2. **VSCode Devcontainerで環境起動**
   - VSCodeでプロジェクトフォルダを開く
   - Ctrl+Shift+P → "Dev Containers: Reopen in Container" を選択
   - コンテナが自動的に構築され、必要な依存関係がインストールされます

3. **データをダウンロード**
   - [Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)からデータをダウンロード
   - `data/` ディレクトリに展開

4. CLIエージェントを起動
   ```bash
   claude
   ```
   または
   ```bash
   gemini
   ```

5. 自然言語で分析を依頼！

## 概要

MCPサーバとしてPython関数の実行環境をLLMに提供することで、エージェントがデータを眺めながら分析を深められるようにすることを目指します。

渡される関数の仕様を工夫することで、その出力もエージェントに自律的に利用してもらえるようにします。


詳細は[カレーちゃんのAI道場LT資料](https://github.com/jintonic3561/comp_with_agent/blob/main/document/lt_slides.pdf)をご覧ください。

カレーちゃんのAI道場についての詳細は[こちら](https://currypurin-dojo.connpass.com/)です。


## プロジェクト構成

### `agent/`
MCPサーバーとツールのコンポーネント群

```
agent/
├── mcp/
│   ├── config.json              # MCPサーバー設定
│   ├── servers/                 # MCPサーバー実装
│   │   ├── data_information.py  # データ情報提供サーバー
│   │   ├── analysis_executor.py # 分析実行サーバー
│   │   └── notebook_writer.py   # ノートブック作成サーバー
│   └── components/              # ツール実装
│       ├── data_information/    # データ情報関連ツール
│       ├── analysis_executor/   # 分析実行ツール
│       └── notebook_writer/     # ノートブック操作ツール
```

#### MCPサーバー

1. **data_information**: データセットの構造と内容に関するメタデータを提供
   - `list_available_data()`: 利用可能なデータ一覧
   - `get_data_description()`: データ詳細説明
   - `get_join_keys_info()`: データ結合キー情報
   - `get_problem_formulation()`: 問題設定

2. **analysis_executor**: データ分析関数の実行環境
   - `execute_soil_analysis()`: 土壌データ分析
   - `execute_timeseries_analysis()`: 時系列データ分析
   - `execute_all_data_analysis()`: 全データ統合分析

3. **notebook_writer**: Jupyter Notebookの作成と管理
   - `add_cell_to_notebook()`: ノートブックへのセル追加

### `data/`
分析対象データセット

### `examples/`
サンプル分析の実行結果

## 異なるデータセットでの利用方法

それほど多くない変更で、異なるデータセットをこのプロジェクトで使用することができます。
以下の手順で改修を行ってください：

### 1. データ情報ツールの更新

`agent/mcp/components/data_information/tools.py`を編集します。

ご自身が取り組みたい問題設計やデータの説明をmd形式で返すようにすればOKです。

```python
def list_available_data() -> List[str]:
    # 新しいデータファイル名に更新
    available_data = ["your_data1", "your_data2", "your_data3"]
    return available_data

def get_data_description(data_type: str) -> str:
    # 新しいデータセットの説明を追加
    if data_type == "your_data_type":
        return """
        # あなたのデータセット
        
        ## データ概要
        データの概要説明...
        
        ## 列の説明
        | 列名 | データ型 | 説明 |
        |------|---------|------|
        | column1 | type | 説明 |
        """
...
```

### 2. 分析実行ツールの更新

`agent/mcp/components/analysis_executor/tools.py`を編集します。

- ご自身のそれぞれのデータを読み込んで分析を行えるよう、各関数を修正します。
- 心臓部となる `_execute_function` 関数はこのまま利用できるはずです。 

### 3. サーバスクリプトの更新

`/work/agent/mcp/servers` 配下のpythonスクリプトのうち、前段で編集したツールが含まれるサーバスクリプトを編集します。

`mcp.tool(your_tool_name)` の部分を、ご自身のツールに合わせて変更してください。

### 4. データファイルの配置

新しいデータセットを`data/`ディレクトリに配置します。

### 5. 動作確認

この時点で、Claude CodeやGemini CLIがツールを認識してくれるはずです。
彼らに話しかけて、実装したツールを読み込めているか確認してください。