<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">Base64 编解码</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">在线 Base64 编码与解码，支持 UTF-8 文本</p>
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
        :placeholder="mode === 'encode' ? '输入文本进行 Base64 编码...' : '输入 Base64 字符串进行解码...'"
        show-count show-copy
        @update:model-value="process" />
      <ToolTextarea :model-value="output" :label="error ? '错误' : '输出'" :rows="8" readonly show-count show-copy
        :placeholder="error || '结果将显示在这里'"
        :validation-state="error ? 'invalid' : 'none'"
        :validation-message="error"
        :container-class="error ? 'border-red-200 dark:border-red-800' : ''"
        :text-class="error ? 'text-red-500' : ''" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore()
store.addHistory('base64')
const modes = [
  { id: 'encode' as const, label: '编码' },
  { id: 'decode' as const, label: '解码' },
]
const mode = ref<'encode' | 'decode'>('encode')
const input = ref('')
const output = ref('')
const error = ref('')
function process() {
  if (!input.value.trim()) { output.value = ''; error.value = ''; return }
  try {
    if (mode.value === 'encode') {
      output.value = btoa(unescape(encodeURIComponent(input.value)))
    } else {
      output.value = decodeURIComponent(escape(atob(input.value.trim())))
    }
    error.value = ''
  } catch (e: any) {
    output.value = ''
    error.value = mode.value === 'decode'
      ? '解码失败：请输入有效的 Base64 字符串'
      : '编码失败：' + e.message
  }
}
watch(mode, () => { if (input.value) process() })
</script>