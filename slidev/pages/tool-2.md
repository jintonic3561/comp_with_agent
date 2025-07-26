---
layout: default
---

# ツール② `Analysis Executor`

<p class="text-xl text-gray-600 mb-6">
LLMが生成した関数を実行し、結果を返すためのツール
</p>

<div class="grid grid-cols-2 gap-4">
  <div>
    ```python {2-3,9-10,12-13|all}
    def execute_timeseries_analysis(
        func_string: str, 
        data_type: Literal["train", "validation", "test"]
    ) -> List[str]:
        """
        ...
        """
        
        # 実行する関数に渡すデータを読み込む
        df = load_data(data_type)

        # LLMが生成した関数を実行
        return _execute_function(func_string, df)
    ```
  </div>
  
  <div v-click>
    ```python {6-11|all}
    def execute_timeseries_analysis(
        func_string: str, 
        data_type: Literal["train", "validation", "test"]
    ) -> List[str]:
        """
        関数定義は以下の要件を満たすように実装すること：
          - 引数として `df: pd.DataFrame` のみを取ること
          - dfには `{data_type}_timeseries.csv` の内容が格納される
          - csvまたはpng形式の分析結果を関数内でファイル保存すること
          - 関数の返り値は保存した分析結果のpath、またはそのリストとすること
        このツールを呼び出した後は、分析結果を必ず読み込んで考察を行うこと
        """
        ...
    ```
  </div>
</div>

<div v-click class="mt-6 bg-orange-50 p-4 rounded-lg">
  <p class="text-lg">
    💡 LLMが生成したコードを安全に実行し、結果をファイルとして保存するツール
  </p>
</div>