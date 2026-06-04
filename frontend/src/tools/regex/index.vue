<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4"><h1 class="text-lg font-semibold text-gray-900 dark:text-white">正则表达式测试</h1><p class="mt-1 text-xs text-gray-500 dark:text-gray-400">在线正则测试工具，支持标志位与替换</p></div>
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-2"><span class="text-sm text-gray-500 dark:text-gray-400">/</span><input v-model="pattern" type="text" placeholder="正则表达式" class="w-48 rounded border border-gray-300 bg-white px-2.5 py-1.5 font-mono text-[13px] text-gray-900 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" /><span class="text-sm text-gray-500 dark:text-gray-400">/</span></div>
      <div class="flex gap-0.5 rounded-md bg-gray-100 p-0.5 dark:bg-gray-800"><button v-for="flag in flags" :key="flag" @click="toggleFlag(flag)" :class="['rounded px-2 py-1 text-xs font-mono transition-colors', activeFlags.has(flag) ? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white' : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300']">{{ flag }}</button></div>
      <button @click="test" class="btn-primary text-xs px-3 py-1.5 ml-auto">匹配</button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入文本" :rows="10" placeholder="输入要测试的文本..." show-count show-lines show-copy @update:model-value="test" />
      <div class="flex flex-col gap-3 flex-1 min-h-0">
        <div class="tool-panel flex-1">
          <div class="tool-panel-header"><span class="text-xs font-medium text-gray-500 dark:text-gray-400">匹配结果 <span v-if="results.length" class="ml-1 text-[11px] font-normal text-green-500">{{ results.length }} 处匹配</span></span></div>
          <div class="p-3 font-mono text-[13px] leading-relaxed overflow-auto flex-1 text-gray-900 dark:text-gray-100">
            <template v-if="pattern && input"><div v-if="results.length" class="space-y-1.5"><div v-for="(r, i) in results" :key="i" class="rounded border border-gray-100 bg-gray-50 p-2 dark:border-gray-800 dark:bg-gray-900/50"><span class="text-[10px] text-gray-400 dark:text-gray-500">匹配 {{ i + 1 }} ({{ r.position }})</span><span class="ml-2 break-all text-gray-900 dark:text-white">{{ r.match }}</span><div v-if="r.groups.length" class="mt-1 space-y-0.5"><div v-for="(g, gi) in r.groups" :key="gi" class="flex gap-2 text-[12px]"><span class="text-gray-400 dark:text-gray-500 shrink-0">${{ gi + 1 }}:</span><span class="text-gray-600 dark:text-gray-300">{{ g || '(空)' }}</span></div></div></div></div><div v-else-if="error" class="text-red-500 text-sm">{{ error }}</div><div v-else class="text-gray-400 dark:text-gray-500">无匹配</div></template>
            <div v-else class="text-gray-400 dark:text-gray-500">输入正则和文本后点击匹配</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('regex')
const pattern = ref(''); const input = ref('')
const activeFlags = reactive(new Set<string>(['g'])); const flags = ['g', 'i', 'm', 's']
const results = ref<{ match: string; position: number; groups: string[] }[]>([]); const error = ref('')
function toggleFlag(f: string) { if (activeFlags.has(f)) activeFlags.delete(f); else activeFlags.add(f); if (input.value) test() }
function test() { results.value = []; error.value = ''; if (!pattern.value || !input.value) return; try { const flagStr = [...activeFlags].join(''); const re = new RegExp(pattern.value, flagStr); if (flagStr.includes('g')) { let m: RegExpExecArray | null; while ((m = re.exec(input.value)) !== null) { results.value.push({ match: m[0], position: m.index, groups: m.slice(1) }); if (m[0].length === 0) re.lastIndex++ } } else { const m = re.exec(input.value); if (m) { results.value.push({ match: m[0], position: m.index, groups: m.slice(1) }) } } } catch (e: any) { error.value = e.message } }
</script>