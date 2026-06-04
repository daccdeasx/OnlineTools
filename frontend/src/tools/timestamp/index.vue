<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">时间戳转换</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Unix 时间戳与可读日期互相转换，支持秒和毫秒</p>
    </div>
    <div class="mb-4 rounded-lg border border-gray-200 bg-gray-50 p-3 dark:border-gray-800 dark:bg-gray-900 flex items-center gap-3 flex-wrap">
      <span class="text-xs text-gray-500 dark:text-gray-400">当前时间戳（秒）:</span>
      <span class="font-mono text-sm font-semibold text-gray-900 dark:text-white tabular-nums">{{ currentTs }}</span>
      <button @click="copyTs" class="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium transition-colors">{{ tsCopied ? '已复制' : '复制' }}</button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-4 lg:flex-row">
      <div class="tool-panel min-h-[200px] flex-1">
        <div class="tool-panel-header"><span class="text-xs font-medium text-gray-500 dark:text-gray-400">时间戳 → 日期</span></div>
        <div class="flex flex-col gap-3 p-4">
          <div><label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Unix 时间戳</label>
            <div class="flex gap-2"><input v-model="tsInput" type="text" placeholder="例如 1717507200" class="tool-input flex-1" @input="convertTsToDate" />
              <select v-model="tsUnit" class="rounded-lg border border-gray-300 bg-white px-2 py-2 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400"><option value="s">秒</option><option value="ms">毫秒</option></select>
            </div></div>
          <div><label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">转换结果</label>
            <div class="rounded-lg border border-gray-200 bg-gray-50 p-3 font-mono text-sm min-h-[40px] dark:border-gray-800 dark:bg-gray-900">
              <template v-if="tsResult"><div class="text-gray-900 dark:text-white font-medium">{{ tsResult.local }}</div><div class="text-xs text-gray-400 mt-0.5">UTC: {{ tsResult.utc }}</div><div class="text-xs text-gray-400">ISO: {{ tsResult.iso }}</div></template>
              <span v-else class="text-gray-400">输入时间戳查看结果</span></div></div></div></div>
      <div class="tool-panel min-h-[200px] flex-1">
        <div class="tool-panel-header"><span class="text-xs font-medium text-gray-500 dark:text-gray-400">日期 → 时间戳</span></div>
        <div class="flex flex-col gap-3 p-4">
          <div><label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">日期时间</label><input v-model="dateInput" type="datetime-local" class="tool-input" @input="convertDateToTs" /></div>
          <div><label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">时间戳结果</label>
            <div class="flex gap-2">
              <div class="flex-1 rounded-lg border border-gray-200 bg-gray-50 p-3 font-mono text-sm dark:border-gray-800 dark:bg-gray-900"><span v-if="dateResult" class="text-gray-900 dark:text-white font-medium tabular-nums">{{ dateResult.s }}</span><span v-else class="text-gray-400">选择日期查看结果</span><div class="text-xs text-gray-400 mt-0.5">秒</div></div>
              <div class="flex-1 rounded-lg border border-gray-200 bg-gray-50 p-3 font-mono text-sm dark:border-gray-800 dark:bg-gray-900"><span v-if="dateResult" class="text-gray-900 dark:text-white font-medium tabular-nums">{{ dateResult.ms }}</span><span v-else class="text-gray-400">选择日期查看结果</span><div class="text-xs text-gray-400 mt-0.5">毫秒</div></div>
            </div></div></div></div></div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore()
store.addHistory('timestamp')
const currentTs = ref(Math.floor(Date.now() / 1000))
let timer: ReturnType<typeof setInterval>
onMounted(() => { timer = setInterval(() => { currentTs.value = Math.floor(Date.now() / 1000) }, 1000) })
onUnmounted(() => { clearInterval(timer) })
const tsCopied = ref(false)
function copyTs() { navigator.clipboard.writeText(String(currentTs.value)); tsCopied.value = true; setTimeout(() => (tsCopied.value = false), 1500) }
const tsInput = ref('')
const tsUnit = ref<'s' | 'ms'>('s')
const tsResult = ref<{ local: string; utc: string; iso: string } | null>(null)
function convertTsToDate() { const raw = tsInput.value.trim(); if (!raw) { tsResult.value = null; return }; let ms = Number(raw); if (isNaN(ms)) { tsResult.value = null; return }; if (tsUnit.value === 's') ms *= 1000; const d = new Date(ms); tsResult.value = { local: d.toLocaleString('zh-CN'), utc: d.toUTCString(), iso: d.toISOString() } }
const dateInput = ref('')
const dateResult = ref<{ s: number; ms: number } | null>(null)
function convertDateToTs() { if (!dateInput.value) { dateResult.value = null; return }; const d = new Date(dateInput.value); const ms = d.getTime(); dateResult.value = { s: Math.floor(ms / 1000), ms } }
</script>