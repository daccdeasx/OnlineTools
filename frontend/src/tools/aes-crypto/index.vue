<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">AES 加解密</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">基于 Web Crypto API 的 AES-CBC 加解密，纯浏览器端处理</p>
    </div>
    <div class="mb-3 flex flex-wrap items-center gap-3">
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">密钥: <input v-model="key" type="text" class="w-48 rounded border border-gray-300 bg-white px-2 py-1 text-xs font-mono dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" placeholder="16 字符密钥" /></label>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">IV: <input v-model="iv" type="text" class="w-40 rounded border border-gray-300 bg-white px-2 py-1 text-xs font-mono dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" placeholder="16 字符 IV" /></label>
      <button @click="generateKey" class="rounded bg-gray-100 px-2 py-1 text-[11px] text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">随机生成</button>
      <span v-if="error" class="text-[11px] text-red-500">{{ error }}</span>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" :label="mode==='encrypt'?'明文':'密文 (Base64)'" :rows="8" :placeholder="mode==='encrypt'?'输入要加密的文本...':'输入 Base64 密文...'" show-count show-copy />
      <ToolTextarea :model-value="output" :label="mode==='encrypt'?'密文 (Base64)':'明文'" :rows="8" readonly show-count show-copy :placeholder="mode==='encrypt'?'加密结果...':'解密结果...'" />
    </div>
    <div class="mt-3 flex items-center gap-1.5">
      <button @click="mode='encrypt'; process()" :class="['rounded-md px-4 py-1.5 text-xs font-medium transition-colors', mode==='encrypt' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300']">加密</button>
      <button @click="mode='decrypt'; process()" :class="['rounded-md px-4 py-1.5 text-xs font-medium transition-colors', mode==='decrypt' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300']">解密</button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore(); store.addHistory('aes-crypto')
const mode = ref<'encrypt'|'decrypt'>('encrypt')
const key = ref(''); const iv = ref(''); const input = ref(''); const output = ref(''); const error = ref('')
function randStr(len:number) { const chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'; let r=''; for(let i=0;i<len;i++) r+=chars[Math.floor(Math.random()*chars.length)]; return r }
function generateKey() { key.value = randStr(16); iv.value = randStr(16); process() }
async function strToKey(s:string):Promise<CryptoKey> { const enc = new TextEncoder(); const k = await crypto.subtle.importKey('raw', enc.encode(s.padEnd(16).slice(0,16)), { name: 'AES-CBC' }, false, ['encrypt','decrypt']); return k }
async function process() {
  if(!input.value.trim()||!key.value.trim()||!iv.value.trim()) { output.value=''; error.value=''; return }
  error.value=''
  try {
    const k = await strToKey(key.value); const enc = new TextEncoder()
    if(mode.value==='encrypt') {
      const data = enc.encode(input.value)
      const ct = await crypto.subtle.encrypt({ name:'AES-CBC', iv: enc.encode(iv.value.padEnd(16).slice(0,16)) }, k, data)
      output.value = btoa(String.fromCharCode(...new Uint8Array(ct)))
    } else {
      const data = Uint8Array.from(atob(input.value.trim()), c=>c.charCodeAt(0))
      const pt = await crypto.subtle.decrypt({ name:'AES-CBC', iv: enc.encode(iv.value.padEnd(16).slice(0,16)) }, k, data)
      output.value = new TextDecoder().decode(pt)
    }
  } catch(e:any) { output.value=''; error.value='操作失败: '+e.message }
}
watch([key,iv,mode], ()=>{ if(input.value) process() })
</script>
