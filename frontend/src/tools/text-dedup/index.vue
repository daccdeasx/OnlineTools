<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4"><h1 class="text-lg font-semibold text-gray-900 dark:text-white">文本去重 & 排序</h1><p class="mt-1 text-xs text-gray-500 dark:text-gray-400">按行去重、排序、反转，支持忽略空行</p></div>
    <div class="mb-3 flex flex-wrap gap-1.5">
      <button @click="dedup" class="btn-secondary text-xs px-3 py-1.5">去重</button>
      <button @click="sortAsc" class="btn-secondary text-xs px-3 py-1.5">升序排序</button>
      <button @click="sortDesc" class="btn-secondary text-xs px-3 py-1.5">降序排序</button>
      <button @click="reverseLines" class="btn-secondary text-xs px-3 py-1.5">反转顺序</button>
      <button @click="shuffleLines" class="btn-secondary text-xs px-3 py-1.5">随机打乱</button>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 ml-auto"><input v-model="skipEmpty" type="checkbox" class="rounded accent-primary-600" @change="process" /> 忽略空行</label>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入" :rows="10" placeholder="每行一个条目..." show-count show-lines show-copy @update:model-value="process" />
      <ToolTextarea :model-value="output" label="输出" :rows="10" readonly show-count show-lines show-copy />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('text-dedup')
const input = ref(''); const output = ref(''); const skipEmpty = ref(true)
function getLines(): string[] { let lines = input.value.split('\n'); if (skipEmpty.value) lines = lines.filter(l => l.trim() !== ''); return lines }
function joinLines(lines: string[]) { output.value = lines.join('\n') }
function process() { dedup() }
function dedup() { const seen = new Set<string>(); const lines = getLines(); joinLines(lines.filter(l => { const k = l.trim(); if (seen.has(k)) return false; seen.add(k); return true })) }
function sortAsc() { joinLines([...getLines()].sort((a, b) => a.localeCompare(b, 'zh-CN'))) }
function sortDesc() { joinLines([...getLines()].sort((a, b) => b.localeCompare(a, 'zh-CN'))) }
function reverseLines() { joinLines([...getLines()].reverse()) }
function shuffleLines() { const arr = [...getLines()]; for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [arr[i], arr[j]] = [arr[j], arr[i]] }; joinLines(arr) }
</script>