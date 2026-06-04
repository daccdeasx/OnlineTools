<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4"><h1 class="text-lg font-semibold text-gray-900 dark:text-white">XML 格式化</h1><p class="mt-1 text-xs text-gray-500 dark:text-gray-400">XML 格式化、压缩与校验</p></div>
    <div class="mb-3 flex flex-wrap gap-1.5">
      <button @click="doFormat" class="btn-primary text-xs px-3 py-1.5">格式化</button>
      <button @click="doMinify" class="btn-secondary text-xs px-3 py-1.5">压缩</button>
      <select v-model="indentSize" class="ml-auto rounded border border-gray-300 bg-white px-2 py-1.5 text-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 focus:border-primary-400 focus:outline-none focus:ring-1 focus:ring-primary-400">
        <option :value="2">缩进: 2 空格</option><option :value="4">缩进: 4 空格</option><option :value="0">缩进: Tab</option>
      </select>
    </div>
    <div class="flex min-h-0 flex-1 flex-col gap-3 lg:flex-row">
      <ToolTextarea v-model="input" label="输入 XML" :rows="10" placeholder="粘贴 XML 文本..." show-count show-copy @update:model-value="doFormat" />
      <ToolTextarea :model-value="error || output" :label="error ? '错误' : '输出'" :rows="10" readonly show-count show-copy :validation-state="error ? 'invalid' : output ? 'valid' : 'none'" :validation-message="error" :container-class="error ? 'border-red-200 dark:border-red-800' : ''" :text-class="error ? 'text-red-500' : ''" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import ToolTextarea from '@/components/ToolTextarea.vue'
const store = useAppStore()
store.addHistory('xml-formatter')
const input = ref('')
const output = ref('')
const error = ref('')
const indentSize = ref(2)
function getIndent(): string { return indentSize.value === 0 ? '\t' : ' '.repeat(indentSize.value) }
function doFormat() {
  error.value = ''
  output.value = ''
  if (!input.value.trim()) return
  try {
    const parser = new DOMParser()
    const doc = parser.parseFromString(input.value, 'text/xml')
    const errNode = doc.querySelector('parsererror')
    if (errNode) { error.value = errNode.textContent || 'XML 解析错误'; return }
    output.value = formatNode(doc.documentElement, getIndent(), 0)
  } catch (e: any) { error.value = e.message }
}
function doMinify() {
  error.value = ''
  output.value = ''
  if (!input.value.trim()) return
  try {
    const parser = new DOMParser()
    const doc = parser.parseFromString(input.value, 'text/xml')
    const errNode = doc.querySelector('parsererror')
    if (errNode) { error.value = errNode.textContent || 'XML 解析错误'; return }
    output.value = new XMLSerializer().serializeToString(doc)
  } catch (e: any) { error.value = e.message }
}
function formatNode(node: Element, indent: string, depth: number): string {
  const sp = indent.repeat(depth)
  const sp1 = indent.repeat(depth + 1)
  let result = sp + '<' + node.nodeName
  const attrs = node.attributes
  for (let i = 0; i < attrs.length; i++) {
    result += ' ' + attrs[i].name + '="' + escXml(attrs[i].value) + '"'
  }
  const children = Array.from(node.childNodes)
  const elemChildren = children.filter(c => c.nodeType === 1)
  const textContent = children.filter(c => c.nodeType === 3).map(c => c.textContent || '').join('').trim()
  if (!elemChildren.length && !textContent && !node.hasChildNodes()) {
    return result + ' />'
  }
  result += '>'
  if (elemChildren.length) {
    result += '\n'
    for (const child of elemChildren) { result += formatNode(child as Element, indent, depth + 1) + '\n' }
    result += sp
  } else if (textContent) {
    result += escXml(textContent)
  }
  result += '</' + node.nodeName + '>'
  return result
}
function escXml(s: string): string { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;') }
</script>