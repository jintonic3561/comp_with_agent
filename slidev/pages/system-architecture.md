---
layout: default
---

# システム構成

<div class="grid grid-cols-2 gap-8 mt-8">
  <div class="text-center">
    <h3 class="text-2xl font-bold mb-4">AIエージェント</h3>
    <img src="/work/assets/claude_logo.webp" class="w-32 mx-auto mb-4" />
    <p class="text-lg">メインのAIエージェント</p>
  </div>
  
  <div>
    <h3 class="text-2xl font-bold mb-4">ツール（MCPサーバ）</h3>
    <div class="text-xs">
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-100">
            <th class="border p-2 text-left">カテゴリ</th>
            <th class="border p-2 text-left">ツール名 (関数名)</th>
            <th class="border p-2 text-left">役割・説明</th>
          </tr>
        </thead>
        <tbody>
          <tr v-click>
            <td class="border p-2 align-top" rowspan="4"><strong>データ情報取得</strong><br>(Data Information)</td>
            <td class="border p-2"><code>list_available_data</code></td>
            <td class="border p-2">利用可能なデータファイルの一覧を取得</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>get_data_description</code></td>
            <td class="border p-2">各データの概要、スキーマ、列定義をmdで取得</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>get_join_keys_info</code></td>
            <td class="border p-2">データの結合キーに関する情報をmdで取得</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>get_problem_formulation</code></td>
            <td class="border p-2">コンペの問題設計（背景、目的、評価指標など）をmdで取得</td>
          </tr>
          <tr v-click>
            <td class="border p-2 align-top" rowspan="5"><strong>分析実行</strong><br>(Analysis Executor)</td>
            <td class="border p-2"><code>get_data_sample</code></td>
            <td class="border p-2">データのheadとtailを取得</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>get_data_summary</code></td>
            <td class="border p-2">データの統計要約情報を取得</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>execute_timeseries_analysis</code></td>
            <td class="border p-2"><strong>メインデータ</strong>に対し、渡された関数を実行して結果を返す</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>execute_soil_analysis</code></td>
            <td class="border p-2"><strong>土壌データ</strong>に対し、渡された関数を実行して結果を返す</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><code>execute_all_data_analysis</code></td>
            <td class="border p-2"><strong>全データ</strong>に対し、渡された関数を実行して結果を返す</td>
          </tr>
          <tr v-click>
            <td class="border p-2"><strong>レポート作成</strong><br>(Notebook Writer)</td>
            <td class="border p-2"><code>add_cell_to_notebook</code></td>
            <td class="border p-2">Jupyter Notebookにコードや考察を記録</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<style>
table {
  font-size: 0.7rem;
}
td, th {
  padding: 0.3rem;
}
</style>