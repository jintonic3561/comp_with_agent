---
layout: default
---

# ツール① `Data Information`

<p class="text-xl text-gray-600 mb-6">
問題設計、データの列定義等に立ち返るためのツール
</p>

```python {2,5-13,14|all}
def get_data_description(
    data_type: Literal["timeseries", "soil_data"]
) -> str:
    if data_type == "timeseries":
        return """
        # データ概要
        ...
        # 列の説明
        | 列名 | データ型 | 説明 |
        |:---|:---|:---|
        | fips | int | 米国郡のFIPSコード |
        ...
        """
    ...
```

<div v-click class="mt-8 bg-blue-50 p-4 rounded-lg">
  <p class="text-lg">
    💡 LLMが分析中に問題設定やデータ構造を確認できるようにするためのツール
  </p>
</div>