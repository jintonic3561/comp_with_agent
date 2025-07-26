---
layout: default
---

# チャットLLMとの対話における「3つの壁」

<div class="grid grid-cols-3 gap-6 mt-8">
  <div v-click class="bg-gray-50 p-6 rounded-lg">
    <h3 class="text-xl font-bold mb-4 text-red-600">(1) コンテキストの壁</h3>
    <ul class="space-y-2 text-sm">
      <li class="flex items-start gap-2">
        <span>•</span>
        <span>巨大なデータはそもそも読み込んでもらえない</span>
      </li>
    </ul>
    <div class="mt-4 text-center">
      <img src="/work/assets/huge_data.png" class="w-32 mx-auto" />
    </div>
  </div>

  <div v-click class="bg-gray-50 p-6 rounded-lg">
    <h3 class="text-xl font-bold mb-4 text-orange-600">(2) 作業の壁</h3>
    <ul class="space-y-2 text-sm">
      <li class="flex items-start gap-2">
        <span>•</span>
        <span>LLMが生成したコードを、人間がコピペして実行</span>
      </li>
      <li class="flex items-start gap-2">
        <span>•</span>
        <span>実行結果のファイル（CSVや画像）を、人間が確認</span>
      </li>
      <li class="flex items-start gap-2">
        <span>•</span>
        <span>その結果やファイルを、人間がLLMに再入力</span>
      </li>
    </ul>
    <div class="mt-4 text-center">
      <img src="/work/assets/manual_work.png" class="w-32 mx-auto" />
    </div>
  </div>

  <div v-click class="bg-gray-50 p-6 rounded-lg">
    <h3 class="text-xl font-bold mb-4 text-purple-600">(3) 思考の壁</h3>
    <ul class="space-y-2 text-sm">
      <li class="flex items-start gap-2">
        <span>•</span>
        <span>分析の「気づき」は、データを多角的に<strong>眺める</strong>中で生まれる</span>
      </li>
      <li class="flex items-start gap-2">
        <span>•</span>
        <span>LLMは人間が与えた断片的な結果しか見ることができない？</span>
      </li>
    </ul>
    <div class="mt-4 text-center">
      <img src="/work/assets/interrupted_thought.png" class="w-32 mx-auto" />
    </div>
  </div>
</div>