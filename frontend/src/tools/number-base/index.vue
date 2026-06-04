<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">进制转换</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">在二进制、八进制、十进制、十六进制间快速转换</p>
    </div>
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">输入: <input v-model="input" type="text" class="w-64 rounded border border-gray-300 bg-white px-2 py-1 text-xs text-gray-900 font-mono dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" placeholder="输入数字" @input="convert" /></label>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">进制:
        <select v-model="fromBase" class="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200" @change="convert">
          <option v-for="b in bases" :key="'f'+b" :value="b">{{ b }} 进制</option>
        </select>
      </label>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 flex-1 min-h-0">
      <div v-for="b in bases" :key="b" class="tool-panel">
        <div class="tool-panel-header text-xs font-medium text-gray-500 dark:text-gray-400">{{ b }} 进制</div>
        <div class="p-3 font-mono text-sm break-all select-all text-gray-900 dark:text-gray-100">{{ results[b] || '-' }}</div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore(); store.addHistory('number-base')
const bases = [2, 8, 10, 16, 32, 36]
const input = ref('255'); const fromBase = ref(10)
const results = reactive<Record<number,string>>({})
function convert() { const v = input.value.trim(); if (!v) { for (const b of bases) results[b] = ''; return }; for (const b of bases) results[b] = ''; try { const num = parseInt(v, fromBase.value); if (isNaN(num)) return; for (const b of bases) { if (b === 10) results[b] = String(num); else results[b] = num.toString(b).toUpperCase() } } catch(e) {} }
convert()
</script>
