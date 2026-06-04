<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">图片处理</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">图片压缩、缩放、格式转换（调用后端 API）</p>
    </div>

    <div v-if="!uploadedFile" class="flex-1 flex items-center justify-center min-h-0">
      <label class="flex flex-col items-center gap-3 cursor-pointer rounded-xl border-2 border-dashed border-gray-300 p-12 transition-colors hover:border-primary-400 dark:border-gray-600 dark:hover:border-primary-500">
        <svg class="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
        <span class="text-sm text-gray-500 dark:text-gray-400">点击或拖拽上传图片</span>
        <span class="text-[11px] text-gray-400">支持 PNG / JPEG / WebP / GIF，最大 10MB</span>
        <input type="file" accept="image/*" class="hidden" @change="onFileSelect" />
      </label>
    </div>

    <template v-else>
      <div class="mb-3 flex flex-wrap items-center gap-2">
        <button v-for="tab in tabs" :key="tab.id" @click="mode = tab.id"
          :class="['rounded-md px-3 py-1.5 text-xs font-medium transition-all', mode === tab.id ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700']">{{ tab.label }}</button>
        <span class="ml-2 text-[11px] text-gray-400">{{ uploadedFile.name }} ({{ formatSize(uploadedFile.size) }})</span>
        <button @click="reset" class="ml-auto rounded px-2 py-1 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">重新选择</button>
      </div>

      <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
        <!-- Original preview -->
        <div class="flex flex-1 flex-col items-center justify-center min-h-0 rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800/50">
          <p class="mb-2 text-[11px] text-gray-400">原图 ({{ info.originalSize }})</p>
          <img :src="originalUrl" class="max-h-full max-w-full rounded object-contain" alt="original" />
        </div>

        <!-- Controls -->
        <div class="flex w-full flex-col gap-3 lg:w-56">
          <!-- Compress controls -->
          <template v-if="mode === 'compress'">
            <label class="text-[11px] text-gray-500 dark:text-gray-400">质量: {{ quality }}%</label>
            <input v-model.number="quality" type="range" min="10" max="100" class="accent-primary-600" />
            <label class="text-[11px] text-gray-500 dark:text-gray-400">输出格式:</label>
            <select v-model="outFormat" class="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200">
              <option value="jpeg">JPEG</option>
              <option value="png">PNG</option>
              <option value="webp">WebP</option>
            </select>
          </template>
          <!-- Resize controls -->
          <template v-if="mode === 'resize'">
            <label class="text-[11px] text-gray-500 dark:text-gray-400">宽度: <input v-model.number="resizeW" type="number" min="1" max="4096" class="w-20 rounded border border-gray-300 bg-white px-1 py-0.5 text-xs text-right dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200" /></label>
            <label class="text-[11px] text-gray-500 dark:text-gray-400">高度: <input v-model.number="resizeH" type="number" min="1" max="4096" class="w-20 rounded border border-gray-300 bg-white px-1 py-0.5 text-xs text-right dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200" /></label>
            <label class="flex items-center gap-1.5 text-[11px] text-gray-500 dark:text-gray-400"><input v-model="keepRatio" type="checkbox" class="accent-primary-600" /> 保持比例</label>
          </template>
          <!-- Convert controls -->
          <template v-if="mode === 'convert'">
            <label class="text-[11px] text-gray-500 dark:text-gray-400">目标格式:</label>
            <select v-model="outFormat" class="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200">
              <option value="jpeg">JPEG</option>
              <option value="png">PNG</option>
              <option value="webp">WebP</option>
              <option value="gif">GIF</option>
            </select>
          </template>
          <button @click="process" :disabled="processing" class="mt-2 rounded-md bg-primary-600 px-3 py-2 text-xs font-medium text-white hover:bg-primary-700 disabled:opacity-50 transition-colors">{{ processing ? '处理中...' : '开始处理' }}</button>
          <span v-if="errorMsg" class="text-[11px] text-red-500">{{ errorMsg }}</span>
        </div>

        <!-- Result preview -->
        <div class="flex flex-1 flex-col items-center justify-center min-h-0 rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800/50">
          <p class="mb-2 text-[11px] text-gray-400">{{ resultInfo }}</p>
          <img v-if="resultUrl" :src="resultUrl" class="max-h-full max-w-full rounded object-contain" alt="result" />
          <p v-else class="text-xs text-gray-400">点击"开始处理"查看结果</p>
          <button v-if="resultBlob" @click="download" class="mt-3 rounded bg-gray-100 px-3 py-1 text-[11px] text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">下载结果</button>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore(); store.addHistory('image-processor')
const API = 'http://127.0.0.1:8000/api/tools/image'

const tabs = [{ id: 'compress' as const, label: '压缩' }, { id: 'resize' as const, label: '缩放' }, { id: 'convert' as const, label: '转格式' }]
const mode = ref<'compress'|'resize'|'convert'>('compress')
const uploadedFile = ref<File|null>(null)
const originalUrl = ref('')
const resultUrl = ref('')
const resultBlob = ref<Blob|null>(null)
const resultInfo = ref('')
const errorMsg = ref('')
const processing = ref(false)
const quality = ref(85); const outFormat = ref('jpeg')
const resizeW = ref(800); const resizeH = ref(600); const keepRatio = ref(true)
const info = ref({ originalSize: '' })
const formatSize = (b: number) => b < 1024*1024 ? (b/1024).toFixed(1)+'KB' : (b/(1024*1024)).toFixed(1)+'MB'

function onFileSelect(e: Event) { const f = (e.target as HTMLInputElement).files?.[0]; if (f) { uploadedFile.value = f; info.value.originalSize = formatSize(f.size); originalUrl.value = URL.createObjectURL(f); resultUrl.value = ''; resultBlob.value = null; errorMsg.value = '' } }
function reset() { uploadedFile.value = null; originalUrl.value = ''; resultUrl.value = ''; resultBlob.value = null; errorMsg.value = '' }
async function process() {
  if (!uploadedFile.value) return
  processing.value = true; errorMsg.value = ''
  try {
    const fd = new FormData(); fd.append('file', uploadedFile.value)
    let url = API + '/'
    if (mode.value === 'compress') { url += 'compress?quality='+quality.value+'&output_format='+outFormat.value+'&return_type=file' }
    else if (mode.value === 'resize') { url += 'resize?width='+resizeW.value+'&height='+resizeH.value+'&keep_aspect_ratio='+keepRatio.value+'&return_type=file' }
    else { url += 'convert?target_format='+outFormat.value+'&return_type=file' }
    const resp = await fetch(url, { method: 'POST', body: fd })
    if (!resp.ok) { const err = await resp.json(); errorMsg.value = err.message || '处理失败'; return }
    const blob = await resp.blob()
    resultBlob.value = blob; resultUrl.value = URL.createObjectURL(blob)
    resultInfo.value = '结果 (' + formatSize(blob.size) + ')'
    if (resp.headers.get('X-Compressed-Size')) { resultInfo.value += ' | 原始:' + info.value.originalSize + ', 压缩率:' + (Number(resp.headers.get('X-Compressed-Size'))/uploadedFile.value.size*100).toFixed(1) + '%' }
    if (resp.headers.get('X-Resized-Width')) { resultInfo.value = resp.headers.get('X-Resized-Width') + 'x' + resp.headers.get('X-Resized-Height') + ' (' + formatSize(blob.size) + ')' }
  } catch(e:any) { errorMsg.value = '请求失败: '+e.message } finally { processing.value = false }
}
function download() { if (!resultBlob.value) return; const a = document.createElement('a'); a.href = URL.createObjectURL(resultBlob.value); a.download = 'processed.' + (outFormat.value === 'jpeg' ? 'jpg' : outFormat.value); a.click() }
</script>
