<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">Unicode 转换</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">文本与 Unicode 转义序列（\uXXXX）互相转换</p>
    </div>
    <div class="mb-4 flex gap-1 rounded-lg bg-gray-100 p-1 w-fit dark:bg-gray-800">
      <button v-for="m in modes" :key="m.id" @click="mode = m.id; process()"
        :class="['rounded-md px-3 py-1.5 text-xs font-medium transition-all',
          mode === m.id ? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white'
            : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200']">
        {{ m.label }}
      </button>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入" :rows="8"
        :placeholder="mode === 'encode' ? '输入文本，如: 你好世界' : '输入Unicode转义序列，如: \\u4f60\\u597d\\u4e16\\u754c'"
        show-count show-copy @update:model-value="process" />
      <ToolTextarea :model-value="output" label="输出" :rows="8" readonly show-count show-copy />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore()
store.addHistory('unicode')
const modes = [{ id: 'encode' as const, label: '文本 → Unicode' }, { id: 'decode' as const, label: 'Unicode → 文本' }]
const mode = ref<'encode' | 'decode'>('encode')
const input = ref('')
const output = ref('')
function process() { if (!input.value.trim()) { output.value = ''; return }; if (mode.value === 'encode') { output.value = Array.from(input.value).map(ch => { const cp = ch.codePointAt(0)!; if (cp > 0xFFFF) { return '\\u{' + cp.toString(16).toUpperCase() + '}' }; return '\\u' + cp.toString(16).toUpperCase().padStart(4, '0') }).join('') } else { output.value = input.value.replace(/\\u\{([0-9A-Fa-f]+)\}|\\u([0-9A-Fa-f]{4})/g, (_, hi, lo) => { const cp = hi ? parseInt(hi, 16) : parseInt(lo, 16); return String.fromCodePoint(cp) }) } }
</script>