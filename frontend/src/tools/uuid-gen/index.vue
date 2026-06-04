<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">UUID 生成器</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">批量生成 UUID v4（随机）唯一标识符</p>
    </div>
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">数量: <input v-model.number="count" type="number" min="1" max="100" class="w-16 rounded border border-gray-300 bg-white px-2 py-1 text-xs text-gray-900 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" /></label>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400"><input v-model="uppercase" type="checkbox" class="rounded accent-primary-600" /> 大写</label>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400"><input v-model="noDashes" type="checkbox" class="rounded accent-primary-600" /> 无连字符</label>
      <button @click="generate" class="btn-primary text-xs px-3 py-1.5">生成</button>
      <button @click="clear" class="btn-ghost text-xs px-3 py-1.5 ml-auto">清空</button>
    </div>
    <div class="flex-1 min-h-0">
      <div class="tool-panel h-full">
        <div class="tool-panel-header">
          <span class="text-xs font-medium text-gray-500 dark:text-gray-400">结果 ({{ uuids.length }} 个)</span>
          <button v-if="uuids.length" @click="copyAll" class="rounded px-1.5 py-0.5 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors">{{ copied ? '已复制' : '复制全部' }}</button>
        </div>
        <div class="p-3 font-mono text-[13px] leading-relaxed overflow-auto flex-1 text-gray-900 dark:text-gray-100">
          <div v-if="uuids.length" class="space-y-0.5">
            <div v-for="(uuid, i) in uuids" :key="i" class="group flex items-center gap-2 rounded px-2 py-1 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
              <span class="text-[10px] tabular-nums text-gray-300 dark:text-gray-600 w-6 shrink-0 text-right">{{ i + 1 }}</span>
              <span class="flex-1 break-all select-all">{{ uuid }}</span>
              <button @click="copyOne(uuid)" class="opacity-0 group-hover:opacity-100 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 shrink-0 transition-all">复制</button>
            </div>
          </div>
          <div v-else class="flex items-center justify-center h-full text-gray-400 dark:text-gray-500">点击"生成"按钮创建 UUID</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore()
store.addHistory('uuid-gen')
const count = ref(5)
const uppercase = ref(false)
const noDashes = ref(false)
const uuids = ref<string[]>([])
const copied = ref(false)
function genUUID(): string { return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => { const r = Math.random() * 16 | 0; const v = c === 'x' ? r : (r & 0x3 | 0x8); return v.toString(16) }) }
function generate() { const n = Math.min(100, Math.max(1, count.value || 1)); const result: string[] = []; for (let i = 0; i < n; i++) { let uuid = genUUID(); if (noDashes.value) uuid = uuid.replace(/-/g, ''); if (uppercase.value) uuid = uuid.toUpperCase(); result.push(uuid) }; uuids.value = result }
function clear() { uuids.value = [] }
function copyOne(uuid: string) { navigator.clipboard.writeText(uuid) }
function copyAll() { navigator.clipboard.writeText(uuids.value.join('\n')); copied.value = true; setTimeout(() => (copied.value = false), 1500) }
</script>