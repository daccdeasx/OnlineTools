<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">哈希计算</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">MD5 / SHA-1 / SHA-256 / SHA-512 哈希值计算</p>
    </div>
    <div class="mb-4 flex flex-wrap gap-1 rounded-lg bg-gray-100 p-1 dark:bg-gray-800">
      <button v-for="algo in algorithms" :key="algo" @click="algorithm = algo; process()"
        :class="['rounded-md px-2.5 py-1.5 text-xs font-medium transition-all',
          algorithm === algo ? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white'
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200']">{{ algo }}</button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3">
      <ToolTextarea v-model="input" label="输入文本" :rows="4" placeholder="输入任意文本进行哈希计算..." show-count show-copy @update:model-value="process" />
      <div class="tool-panel">
        <div class="tool-panel-header"><span class="text-xs font-medium text-gray-500 dark:text-gray-400">结果 ({{ algorithm }})</span>
          <button v-if="output" @click="copyOutput" class="rounded px-1.5 py-0.5 text-[11px] text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-500 dark:hover:text-gray-300 dark:hover:bg-gray-800">{{ copied ? '已复制' : '复制' }}</button>
        </div>
        <div class="p-3 font-mono text-sm break-all min-h-[48px] flex items-center" :class="output ? 'text-gray-900 dark:text-white' : 'text-gray-400 dark:text-gray-500'">{{ output || '输入文本后自动生成哈希值' }}</div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore()
store.addHistory('hash')
type Algo = 'MD5' | 'SHA-1' | 'SHA-256' | 'SHA-512'
const algorithms: Algo[] = ['MD5', 'SHA-1', 'SHA-256', 'SHA-512']
const algorithm = ref<Algo>('SHA-256')
const input = ref('')
const output = ref('')
const copied = ref(false)
async function process() { if (!input.value) { output.value = ''; return }; if (algorithm.value === 'MD5') { output.value = md5(input.value); return }; const algoMap: Record<string, string> = { 'SHA-1': 'SHA-1', 'SHA-256': 'SHA-256', 'SHA-512': 'SHA-512' }; const buf = await crypto.subtle.digest(algoMap[algorithm.value], new TextEncoder().encode(input.value)); output.value = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('') }
function copyOutput() { if (!output.value) return; navigator.clipboard.writeText(output.value); copied.value = true; setTimeout(() => (copied.value = false), 1500) }
function md5(str: string): string { function cmn(q: number, a: number, b: number, x: number, s: number, t: number) { const aa = (a + q + x + t) >>> 0; return ((aa << s) | (aa >>> (32 - s))) + b }; const ff = (a: number, b: number, c: number, d: number, x: number, s: number, t: number) => cmn((b & c) | ((~b) & d), a, b, x, s, t); const gg = (a: number, b: number, c: number, d: number, x: number, s: number, t: number) => cmn((b & d) | (c & (~d)), a, b, x, s, t); const hh = (a: number, b: number, c: number, d: number, x: number, s: number, t: number) => cmn(b ^ c ^ d, a, b, x, s, t); const ii = (a: number, b: number, c: number, d: number, x: number, s: number, t: number) => cmn(c ^ (b | (~d)), a, b, x, s, t); const bytes: number[] = []; for (let i = 0; i < str.length; i++) { const code = str.charCodeAt(i); if (code < 0x80) bytes.push(code); else if (code < 0x800) { bytes.push(0xc0 | (code >> 6)); bytes.push(0x80 | (code & 0x3f)) } else if (code < 0xd800 || code >= 0xe000) { bytes.push(0xe0 | (code >> 12)); bytes.push(0x80 | ((code >> 6) & 0x3f)); bytes.push(0x80 | (code & 0x3f)) } else { i++; const cp = 0x10000 + ((code & 0x03ff) << 10) + (str.charCodeAt(i) & 0x03ff); bytes.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 0x3f), 0x80 | ((cp >> 6) & 0x3f), 0x80 | (cp & 0x3f)) } }; const origLen = bytes.length; bytes.push(0x80); while (bytes.length % 64 !== 56) bytes.push(0); const lenBits = origLen * 8; for (let i = 0; i < 8; i++) bytes.push((lenBits >>> (i * 8)) & 0xff); let [a, b, c, d] = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]; for (let k = 0; k < bytes.length; k += 64) { const block = bytes.slice(k, k + 64); const x: number[] = []; for (let i = 0; i < 16; i++) x[i] = (block[i * 4] | (block[i * 4 + 1] << 8) | (block[i * 4 + 2] << 16) | (block[i * 4 + 3] << 24)) >>> 0; let [aa, bb, cc, dd] = [a, b, c, d]; a = ff(a, b, c, d, x[0], 7, 0xd76aa478); d = ff(d, a, b, c, x[1], 12, 0xe8c7b756); c = ff(c, d, a, b, x[2], 17, 0x242070db); b = ff(b, c, d, a, x[3], 22, 0xc1bdceee); a = ff(a, b, c, d, x[4], 7, 0xf57c0faf); d = ff(d, a, b, c, x[5], 12, 0x4787c62a); c = ff(c, d, a, b, x[6], 17, 0xa8304613); b = ff(b, c, d, a, x[7], 22, 0xfd469501); a = ff(a, b, c, d, x[8], 7, 0x698098d8); d = ff(d, a, b, c, x[9], 12, 0x8b44f7af); c = ff(c, d, a, b, x[10], 17, 0xffff5bb1); b = ff(b, c, d, a, x[11], 22, 0x895cd7be); a = ff(a, b, c, d, x[12], 7, 0x6b901122); d = ff(d, a, b, c, x[13], 12, 0xfd987193); c = ff(c, d, a, b, x[14], 17, 0xa679438e); b = ff(b, c, d, a, x[15], 22, 0x49b40821); a = gg(a, b, c, d, x[1], 5, 0xf61e2562); d = gg(d, a, b, c, x[6], 9, 0xc040b340); c = gg(c, d, a, b, x[11], 14, 0x265e5a51); b = gg(b, c, d, a, x[0], 20, 0xe9b6c7aa); a = gg(a, b, c, d, x[5], 5, 0xd62f105d); d = gg(d, a, b, c, x[10], 9, 0x2441453); c = gg(c, d, a, b, x[15], 14, 0xd8a1e681); b = gg(b, c, d, a, x[4], 20, 0xe7d3fbc8); a = gg(a, b, c, d, x[9], 5, 0x21e1cde6); d = gg(d, a, b, c, x[14], 9, 0xc33707d6); c = gg(c, d, a, b, x[3], 14, 0xf4d50d87); b = gg(b, c, d, a, x[8], 20, 0x455a14ed); a = gg(a, b, c, d, x[13], 5, 0xa9e3e905); d = gg(d, a, b, c, x[2], 9, 0xfcefa3f8); c = gg(c, d, a, b, x[7], 14, 0x676f02d9); b = gg(b, c, d, a, x[12], 20, 0x8d2a4c8a); a = hh(a, b, c, d, x[5], 4, 0xfffa3942); d = hh(d, a, b, c, x[8], 11, 0x8771f681); c = hh(c, d, a, b, x[11], 16, 0x6d9d6122); b = hh(b, c, d, a, x[14], 23, 0xfde5380c); a = hh(a, b, c, d, x[1], 4, 0xa4beea44); d = hh(d, a, b, c, x[4], 11, 0x4bdecfa9); c = hh(c, d, a, b, x[7], 16, 0xf6bb4b60); b = hh(b, c, d, a, x[10], 23, 0xbebfbc70); a = hh(a, b, c, d, x[13], 4, 0x289b7ec6); d = hh(d, a, b, c, x[0], 11, 0xeaa127fa); c = hh(c, d, a, b, x[3], 16, 0xd4ef3085); b = hh(b, c, d, a, x[6], 23, 0x4881d05); a = hh(a, b, c, d, x[9], 4, 0xd9d4d039); d = hh(d, a, b, c, x[12], 11, 0xe6db99e5); c = hh(c, d, a, b, x[15], 16, 0x1fa27cf8); b = hh(b, c, d, a, x[2], 23, 0xc4ac5665); a = ii(a, b, c, d, x[0], 6, 0xf4292244); d = ii(d, a, b, c, x[7], 10, 0x432aff97); c = ii(c, d, a, b, x[14], 15, 0xab9423a7); b = ii(b, c, d, a, x[5], 21, 0xfc93a039); a = ii(a, b, c, d, x[12], 6, 0x655b59c3); d = ii(d, a, b, c, x[3], 10, 0x8f0ccc92); c = ii(c, d, a, b, x[10], 15, 0xffeff47d); b = ii(b, c, d, a, x[1], 21, 0x85845dd1); a = ii(a, b, c, d, x[8], 6, 0x6fa87e4f); d = ii(d, a, b, c, x[15], 10, 0xfe2ce6e0); c = ii(c, d, a, b, x[6], 15, 0xa3014314); b = ii(b, c, d, a, x[13], 21, 0x4e0811a1); a = ii(a, b, c, d, x[4], 6, 0xf7537e82); d = ii(d, a, b, c, x[11], 10, 0xbd3af235); c = ii(c, d, a, b, x[2], 15, 0x2ad7d2bb); b = ii(b, c, d, a, x[9], 21, 0xeb86d391); a = (a + aa) >>> 0; b = (b + bb) >>> 0; c = (c + cc) >>> 0; d = (d + dd) >>> 0 }; return [a, b, c, d].map(x => (x >>> 0).toString(16).padStart(8, '0')).join('') }
</script>