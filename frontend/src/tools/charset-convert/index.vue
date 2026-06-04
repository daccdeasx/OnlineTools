<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">字符编码转换</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">UTF-8 / GBK / ISO-8859-1 / UTF-16 等编码互转（后端 API）</p>
    </div>
    <div class="mb-3 flex flex-wrap items-center gap-3">
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">源编码:
        <select v-model="fromEncoding" class="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200" @change="convert">
          <option v-for="e in encodings" :key="'f'+e" :value="e">{{ e }}</option>
        </select>
      </label>
      <span class="text-xs text-gray-400">→</span>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">目标编码:
        <select v-model="toEncoding" class="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200" @change="convert">
          <option v-for="e in encodings" :key="'t'+e" :value="e">{{ e }}</option>
        </select>
      </label>
      <button @click="convert" :disabled="loading" class="rounded-md bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700 disabled:opacity-50 transition-colors">{{ loading ? '转换中...' : '转换' }}</button>
      <button @click="swap" class="rounded bg-gray-100 px-2 py-1.5 text-xs text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700">⇄</button>
      <span v-if="errorMsg" class="text-[11px] text-red-500">{{ errorMsg }}</span>
      <button @click="clear" class="ml-auto rounded px-2 py-1 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">清空</button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" :label="'输入 (' + fromEncoding + ')'" :rows="8" placeholder="输入要转换的文本..." show-count show-copy />
      <ToolTextarea :model-value="output" :label="'输出 (' + toEncoding + ')'" :rows="8" readonly show-count show-copy :placeholder="errorMsg || '转换结果'" :validation-state="errorMsg ? 'invalid' : 'none'" :validation-message="errorMsg" :container-class="errorMsg ? 'border-red-200 dark:border-red-800' : ''" :text-class="errorMsg ? 'text-red-500' : ''" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('charset-convert')
const API = 'http://127.0.0.1:8000/api/tools/charset'
const encodings = ref<string[]>(['utf-8','gbk','gb18030','big5','iso-8859-1','utf-16','shift_jis','euc-kr','ascii','windows-1252'])
const fromEncoding = ref('gbk'); const toEncoding = ref('utf-8')
const input = ref(''); const output = ref(''); const errorMsg = ref(''); const loading = ref(false)

onMounted(async () => {
  try { const r = await fetch(API+'/encodings'); const d = await r.json(); if(d.code===0) encodings.value = d.data.encodings } catch(e) {}
})

async function convert() {
  const v = input.value.trim()
  if (!v) { output.value = ''; errorMsg.value = ''; return }
  loading.value = true; errorMsg.value = ''
  try {
    const resp = await fetch(API+'/convert', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ text: v, from_encoding: fromEncoding.value, to_encoding: toEncoding.value })
    })
    const d = await resp.json()
    if (d.code === 0) { output.value = d.data.result; errorMsg.value = '' }
    else { output.value = ''; errorMsg.value = d.message }
  } catch(e: any) { output.value = ''; errorMsg.value = '请求失败: ' + e.message }
  finally { loading.value = false }
}
function swap() { const t = fromEncoding.value; fromEncoding.value = toEncoding.value; toEncoding.value = t; convert() }
function clear() { input.value = ''; output.value = ''; errorMsg.value = '' }
</script>
