<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">HTML 实体编解码</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">HTML 实体编码（&amp;lt;）与解码</p>
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
        :placeholder="mode === 'encode' ? '输入含特殊字符的文本...' : '输入HTML实体字符串...'"
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
store.addHistory('html-entity')
const modes = [{ id: 'encode' as const, label: '编码' }, { id: 'decode' as const, label: '解码' }]
const mode = ref<'encode' | 'decode'>('encode')
const input = ref('')
const output = ref('')
const entityMap: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;', '`': '&#96;' }
const decodeMap = Object.fromEntries(Object.entries(entityMap).map(([k, v]) => [v, k]))
function process() { if (!input.value.trim()) { output.value = ''; return }; if (mode.value === 'encode') { output.value = input.value.replace(/[&<>"'`]/g, ch => entityMap[ch] || ch) } else { output.value = input.value.replace(/&[#\w]+;/g, ent => decodeMap[ent] || ent).replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n))).replace(/&#x([0-9A-Fa-f]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16))) } }
</script>