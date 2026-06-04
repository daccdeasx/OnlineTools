<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">JWT 解析</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">解码 JWT Token 的 Header 与 Payload</p>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="JWT Token" :rows="6" placeholder="粘贴 JWT Token (xxxxx.yyyyy.zzzzz)..." show-copy @update:model-value="decode" />
      <div class="flex min-w-0 flex-1 flex-col gap-3">
        <div class="tool-panel flex-1">
          <div class="tool-panel-header text-xs font-medium" :class="headerErr ? 'text-red-500' : 'text-gray-500 dark:text-gray-400'">{{ headerErr ? 'Header Error' : 'Header' }}</div>
          <pre class="p-3 font-mono text-xs text-gray-900 dark:text-gray-100 overflow-auto flex-1 whitespace-pre-wrap" :class="headerErr ? 'text-red-500' : ''">{{ headerErr || headerOut || '--' }}</pre>
        </div>
        <div class="tool-panel flex-1">
          <div class="tool-panel-header text-xs font-medium" :class="payloadErr ? 'text-red-500' : 'text-gray-500 dark:text-gray-400'">{{ payloadErr ? 'Payload Error' : 'Payload' }}</div>
          <pre class="p-3 font-mono text-xs text-gray-900 dark:text-gray-100 overflow-auto flex-1 whitespace-pre-wrap" :class="payloadErr ? 'text-red-500' : ''">{{ payloadErr || payloadOut || '--' }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('jwt-parser')
const input = ref(''); const headerOut = ref(''); const payloadOut = ref('')
const headerErr = ref(''); const payloadErr = ref('')
function safeB64(s: string): string { try { let b64 = s.replace(/-/g, '+').replace(/_/g, '/'); while (b64.length % 4 !== 0) b64 += '='; return decodeURIComponent(atob(b64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')) } catch(e) { throw new Error('Base64 解码失败') } }
function decode() {
  const v = input.value.trim()
  if (!v) { headerOut.value = ''; payloadOut.value = ''; headerErr.value = ''; payloadErr.value = ''; return }
  try {
    const parts = v.split('.')
    if (parts.length < 2) { headerErr.value = '无效的 JWT 格式'; payloadOut.value = ''; return }
    try { const h = JSON.parse(safeB64(parts[0])); headerOut.value = JSON.stringify(h, null, 2); headerErr.value = '' } catch(e:any) { headerOut.value = ''; headerErr.value = 'Header: ' + e.message }
    try { const p = JSON.parse(safeB64(parts[1])); if (p.exp) { const d=new Date(p.exp*1000); p._expired = p.exp < Date.now()/1000; p._exp_date = d.toISOString() }; if (p.iat) p._iat_date = new Date(p.iat*1000).toISOString(); payloadOut.value = JSON.stringify(p, null, 2); payloadErr.value = '' } catch(e:any) { payloadOut.value = ''; payloadErr.value = 'Payload: ' + e.message }
  } catch(e:any) { headerErr.value = e.message }
}
</script>
