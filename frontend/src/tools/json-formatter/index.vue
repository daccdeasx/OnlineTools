<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-white">JSON 格式化</h1>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">JSON 格式化、压缩与校验，处理大文本不卡顿</p>
    </div>
    <div class="mb-3 flex flex-wrap gap-1.5">
      <button @click="formatJson" class="btn-primary text-xs px-3 py-1.5">格式化</button>
      <button @click="minifyJson" class="btn-secondary text-xs px-3 py-1.5">压缩</button>
      <button @click="validateJson" class="btn-secondary text-xs px-3 py-1.5">校验</button>
      <select v-model="indent" class="ml-auto rounded border border-gray-300 bg-white px-2 py-1.5 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400">
        <option :value="2">缩进: 2 空格</option>
        <option :value="4">缩进: 4 空格</option>
        <option :value="0">缩进: Tab</option>
      </select>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入 JSON" :rows="10" placeholder='粘贴 JSON 文本，例如 { "hello": "world" }' show-count show-copy @update:model-value="autoFormat" />
      <ToolTextarea :model-value="output" label="输出" :rows="10" readonly show-count show-copy placeholder="格式化结果将显示在这里"
        :validation-state="validationValid ? 'valid' : validationMessage ? 'invalid' : 'none'"
        :validation-message="validationMessage" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore()
store.addHistory('json-formatter')
const input = ref('')
const output = ref('')
const indent = ref(2)
const validationMessage = ref('')
const validationValid = ref(false)
function getIndentStr(): string { if (indent.value === 0) return '\t'; return ' '.repeat(indent.value) }
function formatJson() { if (!input.value.trim()) { output.value = ''; validationMessage.value = ''; return }; try { const obj = JSON.parse(input.value); output.value = JSON.stringify(obj, null, getIndentStr()); validationMessage.value = ''; validationValid.value = true } catch (e: any) { output.value = input.value; validationMessage.value = e.message; validationValid.value = false } }
function minifyJson() { if (!input.value.trim()) { output.value = ''; validationMessage.value = ''; return }; try { const obj = JSON.parse(input.value); output.value = JSON.stringify(obj); validationMessage.value = ''; validationValid.value = true } catch (e: any) { validationMessage.value = e.message; validationValid.value = false } }
function validateJson() { if (!input.value.trim()) { validationMessage.value = ''; return }; try { JSON.parse(input.value); validationMessage.value = ''; validationValid.value = true } catch (e: any) { validationMessage.value = e.message; validationValid.value = false } }
function autoFormat() { if (!input.value.trim()) { output.value = ''; validationMessage.value = ''; return }; try { const obj = JSON.parse(input.value); output.value = JSON.stringify(obj, null, getIndentStr()); validationMessage.value = ''; validationValid.value = true } catch { output.value = input.value; validationMessage.value = ''; validationValid.value = false } }
</script>