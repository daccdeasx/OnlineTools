<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4"><h1 class="text-lg font-semibold text-gray-900 dark:text-white">大小写转换</h1><p class="mt-1 text-xs text-gray-500 dark:text-gray-400">快速转换文本大小写格式</p></div>
    <div class="mb-3 flex flex-wrap gap-1.5">
      <button @click="convert('lower')" class="btn-secondary text-xs px-3 py-1.5">全小写</button>
      <button @click="convert('upper')" class="btn-secondary text-xs px-3 py-1.5">全大写</button>
      <button @click="convert('title')" class="btn-secondary text-xs px-3 py-1.5">首字母大写</button>
      <button @click="convert('camel')" class="btn-secondary text-xs px-3 py-1.5">驼峰命名</button>
      <button @click="convert('snake')" class="btn-secondary text-xs px-3 py-1.5">蛇形命名</button>
      <button @click="convert('kebab')" class="btn-secondary text-xs px-3 py-1.5">短横命名</button>
      <button @click="convert('constant')" class="btn-secondary text-xs px-3 py-1.5">常量命名</button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入" :rows="10" placeholder="输入要转换的文本..." show-count show-lines show-copy />
      <ToolTextarea :model-value="output" label="输出" :rows="10" readonly show-count show-lines show-copy />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('case-convert')
const input = ref(''); const output = ref('')
function getWords(): string[] { return input.value.replace(/[_-]/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2').split(/[\s]+/).filter(Boolean) }
function convert(type: string) { if (!input.value.trim()) { output.value = ''; return }; const words = getWords(); if (!words.length) { output.value = ''; return }; switch (type) { case 'lower': output.value = input.value.toLowerCase(); break; case 'upper': output.value = input.value.toUpperCase(); break; case 'title': output.value = words.map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' '); break; case 'camel': output.value = words.map((w, i) => i === 0 ? w.toLowerCase() : w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(''); break; case 'snake': output.value = words.map(w => w.toLowerCase()).join('_'); break; case 'kebab': output.value = words.map(w => w.toLowerCase()).join('-'); break; case 'constant': output.value = words.map(w => w.toUpperCase()).join('_'); break } }
</script>