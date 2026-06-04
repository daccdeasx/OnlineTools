<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">随机密码生成</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">生成强密码，支持自定义长度与字符集</p>
    </div>
    <div class="mb-5 grid grid-cols-2 sm:grid-cols-4 gap-3">
      <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-300"><input v-model="options.lowercase" type="checkbox" class="rounded accent-primary-600" :disabled="lockCharSet" /> 小写 a-z</label>
      <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-300"><input v-model="options.uppercase" type="checkbox" class="rounded accent-primary-600" :disabled="lockCharSet" /> 大写 A-Z</label>
      <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-300"><input v-model="options.numbers" type="checkbox" class="rounded accent-primary-600" :disabled="lockCharSet" /> 数字 0-9</label>
      <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-300"><input v-model="options.symbols" type="checkbox" class="rounded accent-primary-600" :disabled="lockCharSet" /> 符号 !@#$</label>
    </div>
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">长度: <input v-model.number="options.length" type="number" min="4" max="128" class="w-16 rounded border border-gray-300 bg-white px-2 py-1 text-xs text-gray-900 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" /></label>
      <label class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">数量: <input v-model.number="count" type="number" min="1" max="50" class="w-14 rounded border border-gray-300 bg-white px-2 py-1 text-xs text-gray-900 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400" /></label>
      <button @click="generate" class="btn-primary text-xs px-3 py-1.5">生成</button>
      <button @click="clear" class="btn-ghost text-xs px-3 py-1.5 ml-auto">清空</button>
    </div>
    <div class="flex-1 min-h-0">
      <div class="tool-panel h-full">
        <div class="tool-panel-header"><span class="text-xs font-medium text-gray-500 dark:text-gray-400">结果 ({{ passwords.length }} 个) <span v-if="entropyBps > 0" class="ml-2 text-[11px] font-normal text-gray-400">强度: {{ entropyText }}</span></span>
          <button v-if="passwords.length" @click="copyAll" class="rounded px-1.5 py-0.5 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors">{{ copied ? '已复制' : '复制全部' }}</button>
        </div>
        <div class="p-3 font-mono text-[13px] leading-relaxed overflow-auto flex-1 text-gray-900 dark:text-gray-100">
          <div v-if="passwords.length" class="space-y-1">
            <div v-for="(pw, i) in passwords" :key="i" class="group flex items-center gap-2 rounded px-2 py-1.5 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
              <span class="text-[10px] text-gray-300 dark:text-gray-600 w-5 shrink-0 text-right">{{ i + 1 }}</span>
              <span class="flex-1 break-all select-all font-medium tracking-wide">{{ pw }}</span>
              <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all shrink-0">
                <span class="h-1.5 rounded-full" :class="pwStrength(pw).color" :style="{ width: pwStrength(pw).width }" />
                <button @click="copyOne(pw)" class="text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">复制</button>
              </div>
            </div>
          </div>
          <div v-else class="flex items-center justify-center h-full text-gray-400 dark:text-gray-500">点击"生成"按钮创建密码</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore()
store.addHistory('password-gen')
const options = reactive({ length: 16, lowercase: true, uppercase: true, numbers: true, symbols: true })
const count = ref(3)
const passwords = ref<string[]>([])
const copied = ref(false)
const lockCharSet = computed(() => { const selected = [options.lowercase, options.uppercase, options.numbers, options.symbols].filter(Boolean).length; return selected === 1 })
const charset = computed(() => { let cs = ''; if (options.lowercase) cs += 'abcdefghijklmnopqrstuvwxyz'; if (options.uppercase) cs += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; if (options.numbers) cs += '0123456789'; if (options.symbols) cs += '!@#$%^&*()_+-=[]{}|;:,.<>?'; return cs })
const entropyBps = computed(() => { if (!charset.value.length) return 0; return Math.log2(charset.value.length) * options.length })
const entropyText = computed(() => { const b = entropyBps.value; if (b >= 128) return '非常强'; if (b >= 80) return '强'; if (b >= 60) return '中等'; return '弱' })
function pwStrength(pw: string) { const b = Math.log2(charset.value.length) * pw.length; if (b >= 128) return { width: '40px', color: 'bg-green-500' }; if (b >= 80) return { width: '28px', color: 'bg-lime-500' }; if (b >= 60) return { width: '18px', color: 'bg-yellow-500' }; return { width: '10px', color: 'bg-red-400' } }
function generate() { if (!charset.value.length) return; const n = Math.min(50, Math.max(1, count.value || 1)); const len = Math.min(128, Math.max(4, options.length || 16)); const result: string[] = []; const getRandomValues = () => { const arr = new Uint32Array(len); crypto.getRandomValues(arr); return arr }; for (let i = 0; i < n; i++) { const rng = getRandomValues(); const cs = charset.value; let pw = ''; for (let j = 0; j < len; j++) { pw += cs[rng[j] % cs.length] }; if (!validateCharset(pw)) { pw = fixCharset(pw) }; result.push(pw) }; passwords.value = result }
function validateCharset(pw: string): boolean { if (options.lowercase && !/[a-z]/.test(pw)) return false; if (options.uppercase && !/[A-Z]/.test(pw)) return false; if (options.numbers && !/[0-9]/.test(pw)) return false; if (options.symbols && !/[^a-zA-Z0-9]/.test(pw)) return false; return true }
function fixCharset(pw: string): string { const arr = pw.split(''); const replacements: [boolean, string, RegExp][] = [[options.lowercase, 'abcdefghijklmnopqrstuvwxyz', /[a-z]/], [options.uppercase, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', /[A-Z]/], [options.numbers, '0123456789', /[0-9]/], [options.symbols, '!@#$%^&*', /[^a-zA-Z0-9]/]]; for (const [enabled, cs, re] of replacements) { if (enabled && !re.test(pw)) { arr[0] = cs[Math.floor(Math.random() * cs.length)] } }; return arr.join('') }
function clear() { passwords.value = [] }
function copyOne(pw: string) { navigator.clipboard.writeText(pw) }
function copyAll() { navigator.clipboard.writeText(passwords.value.join('\n')); copied.value = true; setTimeout(() => (copied.value = false), 1500) }
</script>