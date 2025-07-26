---
layout: default
---

# ツール③ `Notebook Writer`

<p class="text-xl text-gray-600 mb-6">
分析のコードや結果をJupyter Notebookに逐次記録するツール
</p>

```python {2-4,6-8,10-17|all}
def add_cell_to_notebook(
    content: str,
    cell_type: Literal["code", "markdown"],
    artifact_paths: List[str]
):
    # セルを追加する
    cell = create_cell(content, cell_type)
    nb.cells.append(cell)

    # 出力ファイルを表示する
    for path in artifact_paths:
        # テキストを表示
        if path.endswith(".csv"):
            display_csv(path)
        # 画像を表示
        elif path.endswith(".png"):
            display_image(path)
```

<div v-click class="mt-8 bg-green-50 p-4 rounded-lg">
  <p class="text-lg">
    💡 分析過程を自動的にNotebook形式で記録し、後から見返せるようにするツール
  </p>
</div>