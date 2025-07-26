---
layout: image-right
image: /work/assets/drought.png
---

# 題材紹介: U.S. Drought Prediction

<p class="text-lg text-gray-600 mb-6">
気象・土壌データから、専門家が作成する「干ばつマップ」の自動化を目指す予測タスクです。
</p>

<div class="grid grid-cols-2 gap-6">
  <div>
    <h3 class="text-xl font-bold mb-3 text-blue-600">入力データ</h3>
    <div class="text-sm space-y-1">
      <p class="font-semibold">時系列データ (気象):</p>
      <ul class="ml-4 space-y-1">
        <li>• 日々の気温、降水量、風速など</li>
        <li>• 期間で訓練/検証/テストに分割</li>
      </ul>
      <p class="font-semibold mt-3">静的データ (地理・土壌):</p>
      <ul class="ml-4 space-y-1">
        <li>• 郡ごとの標高、傾斜、土地の種類など</li>
      </ul>
      <p class="mt-3">両データは <strong>fips</strong> (郡ID) で結合</p>
    </div>
  </div>
  
  <div>
    <h3 class="text-xl font-bold mb-3 text-green-600">予測タスク</h3>
    <div class="text-sm space-y-1">
      <p class="font-semibold">目的変数 (score):</p>
      <ul class="ml-4 space-y-1">
        <li>• 干ばつの深刻度を表す <strong>0〜5</strong> の6段階カテゴリ</li>
      </ul>
      <p class="font-semibold mt-3">評価指標:</p>
      <ul class="ml-4 space-y-1">
        <li>• <strong>Macro F1 Score</strong> (分類精度)</li>
        <li>• <strong>MAE</strong> (回帰誤差)</li>
      </ul>
    </div>
  </div>
</div>