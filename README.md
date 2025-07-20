# セットアップ
[Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)をダウンロードし、`{project_root}/data/`配下に展開してください。

以下のスクリプトで、mcpサーバをclaude codeに追加します。
```
uv run fastmcp install claude-code /work/agent/mcp/servers/data_information.py
uv run fastmcp install claude-code /work/agent/mcp/servers/function_executor.py
uv run fastmcp install claude-code /work/agent/mcp/servers/notebook_writer.py
 ```