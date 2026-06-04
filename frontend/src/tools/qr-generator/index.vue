<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">二维码生成</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">生成二维码，支持文本/链接，可下载 PNG（后端生成）</p>
    </div>
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <input v-model="text" type="text" class="flex-1 min-w-[200px] rounded border border-gray-300 bg-white px-3 py-1.5 text-sm dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" placeholder="输入文本或链接..." @keyup.enter="generate" />
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">尺寸:
        <select v-model="size" class="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200" @change="generate">
          <option :value="150">150px</option>
          <option :value="200">200px</option>
          <option :value="300">300px</option>
          <option :value="400">400px</option>
        </select>
      </label>
      <button @click="generate" :disabled="loading" class="rounded-md bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700 disabled:opacity-50 transition-colors">生成</button>
      <button @click="download" :disabled="!qrBlob" class="rounded-md bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 disabled:opacity-40 transition-colors">下载 PNG</button>
      <span v-if="errorMsg" class="text-[11px] text-red-500">{{ errorMsg }}</span>
    </div>
    <div class="flex-1 flex items-center justify-center min-h-0 p-4">
      <div v-if="qrUrl" class="flex flex-col items-center gap-3">
        <img :src="qrUrl" :width="size" :height="size" alt="QR Code" class="rounded-lg border border-gray-200 dark:border-gray-700 bg-white p-2" />
        <p class="text-[11px] text-gray-400 break-all max-w-lg text-center">{{ text }}</p>
      </div>
      <p v-else class="text-sm text-gray-400 dark:text-gray-500">输入内容后点击"生成"</p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore(); store.addHistory('qr-generator')
const API = 'http://127.0.0.1:8000/api/tools/qr/generate'
const text = ref('https://example.com'); const size = ref(200)
const qrUrl = ref(''); const qrBlob = ref<Blob|null>(null); const errorMsg = ref(''); const loading = ref(false)

async function generate() {
  if (!text.value.trim()) { qrUrl.value = ''; qrBlob.value = null; errorMsg.value = ''; return }
  loading.value = true; errorMsg.value = ''
  try {
    const resp = await fetch(API, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text.value, size: size.value })
    })
    if (!resp.ok) { const e = await resp.json(); errorMsg.value = e.message || '生成失败'; return }
    const blob = await resp.blob()
    qrBlob.value = blob; qrUrl.value = URL.createObjectURL(blob)
  } catch(e: any) { errorMsg.value = '请求失败: ' + e.message } finally { loading.value = false }
}
function download() { if (!qrBlob.value) return; const a = document.createElement('a'); a.href = URL.createObjectURL(qrBlob.value); a.download = 'qrcode.png'; a.click() }
</script>
