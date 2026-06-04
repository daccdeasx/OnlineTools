<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">SQL 格式化</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">在线 SQL 语句格式化、压缩与美化</p>
    </div>
    <div class="mb-3 flex items-center gap-1.5">
      <button @click="format" class="rounded-md bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700 transition-colors">格式化</button>
      <button @click="minify" class="rounded-md bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">压缩</button>
      <button @click="clear" class="ml-auto rounded px-2 py-1 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">清空</button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入" :rows="12" placeholder="粘贴 SQL 语句..." show-count show-copy />
      <ToolTextarea :model-value="output" label="输出" :rows="12" readonly show-count show-copy placeholder="格式化结果" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('sql-formatter')
const input = ref(''); const output = ref('')

const KEYWORDS = ['SELECT','FROM','WHERE','AND','OR','NOT','IN','EXISTS','BETWEEN','LIKE','IS','NULL','JOIN','INNER','LEFT','RIGHT','OUTER','FULL','CROSS','ON','AS','GROUP','BY','HAVING','ORDER','ASC','DESC','LIMIT','OFFSET','UNION','ALL','INSERT','INTO','VALUES','UPDATE','SET','DELETE','CREATE','TABLE','IF','INDEX','VIEW','DROP','ALTER','ADD','COLUMN','PRIMARY','KEY','FOREIGN','REFERENCES','DEFAULT','AUTO_INCREMENT','DISTINCT','COUNT','SUM','AVG','MAX','MIN','CASE','WHEN','THEN','ELSE','END','CAST','CONVERT','COALESCE','NULLIF','WITH','RECURSIVE','RETURNING','EXCEPT','INTERSECT','TRUNCATE','BEGIN','COMMIT','ROLLBACK','TRANSACTION','GRANT','REVOKE']

function format() {
  const sql = input.value.trim(); if (!sql) { output.value = ''; return }
  try {
    let result = sql
    // collapse whitespace
    result = result.replace(/\s+/g, ' ').trim()
    // newline before major keywords
    for (const kw of KEYWORDS) {
      const re = new RegExp(`\\b(${kw})\\b`, 'gi')
      result = result.replace(re, '\n$1')
    }
    // indent after specific keywords
    result = result.split('\n').map(line => line.trim()).filter(l => l).join('\n')
    // fix: SELECT, FROM, WHERE etc. shouldn't be indented
    const lines = result.split('\n')
    const out: string[] = []
    let indent = 0
    const indentAfter = new Set(['SELECT','FROM','WHERE','AND','OR','JOIN','INNER','LEFT','RIGHT','OUTER','FULL','CROSS','ON','SET','HAVING','CASE','WHEN','WITH','UNION','EXCEPT','INTERSECT','GROUP','ORDER'])
    const dedentBefore = new Set(['UNION','EXCEPT','INTERSECT'])
    for (const line of lines) {
      const firstWord = line.split(/\s+/)[0].toUpperCase().replace(/[^A-Z]/g,'')
      if (dedentBefore.has(firstWord)) indent = Math.max(0, indent)
      out.push('  '.repeat(indent) + line)
      if (indentAfter.has(firstWord)) indent = Math.min(4, indent + 1)
      if (firstWord === 'SELECT' && line.includes(',')) continue
    }
    output.value = out.join('\n')
  } catch(e) { output.value = input.value }
}
function minify() { const sql = input.value.trim(); if (!sql) { output.value = ''; return }; output.value = sql.replace(/\s+/g, ' ').replace(/\s*([,()])\s*/g, '$1').replace(/;\s*/g, ';').trim() }
function clear() { input.value = ''; output.value = '' }
</script>
