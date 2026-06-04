<template>
  <div :class="['relative flex flex-col rounded-lg border transition-all duration-150', containerClass]" @click="focusTextarea">
    <div v-if="label || $slots.header" class="flex items-center justify-between border-b px-3 py-2" :class="headerClass">
      <div class="flex items-center gap-2">
        <span v-if="label" class="text-[11px] font-medium uppercase tracking-wider text-gray-400 dark:text-gray-500">{{ label }}</span>
        <slot name="header" />
        <span v-if="validationState === 'valid'" class="text-[11px] font-medium text-green-500">✓</span>
        <span v-else-if="validationState === 'invalid'" class="text-[11px] font-medium text-red-500">✗ {{ validationMessage }}</span>
      </div>
      <div class="flex items-center gap-1">
        <span v-if="showCount && modelValue" class="text-[10px] tabular-nums text-gray-400 dark:text-gray-500">{{ modelValue.length.toLocaleString() }} 字符<template v-if="showLines"> · {{ lineCount }} 行</template></span>
        <button v-if="showCopy && modelValue" @click.stop="copy" class="rounded px-1.5 py-0.5 text-[11px] transition-colors text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-500 dark:hover:text-gray-300 dark:hover:bg-gray-800">{{ copied ? '已复制' : '复制' }}</button>
        <slot name="actions" />
      </div>
    </div>
    <textarea ref="textareaRef" :value="modelValue" @input="onInput" @keydown="onKeydown" :placeholder="placeholder" :readonly="readonly" :disabled="disabled" :spellcheck="spellcheck" :rows="rows" class="w-full flex-1 resize-none bg-transparent px-3 py-2.5 font-mono text-[13px] leading-relaxed placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none disabled:cursor-not-allowed disabled:opacity-40" :class="[textClass, readonly ? 'cursor-default' : '']" />
  </div>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
const props = withDefaults(defineProps<{ modelValue: string; label?: string; placeholder?: string; readonly?: boolean; disabled?: boolean; spellcheck?: boolean; rows?: number; showCount?: boolean; showLines?: boolean; showCopy?: boolean; validationState?: 'none' | 'valid' | 'invalid'; validationMessage?: string; containerClass?: string; headerClass?: string; textClass?: string }>(), { placeholder: '', readonly: false, disabled: false, spellcheck: false, rows: 6, showCount: false, showLines: false, showCopy: false, validationState: 'none', validationMessage: '', containerClass: 'border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900 focus-within:border-primary-400 dark:focus-within:border-primary-600 focus-within:ring-1 focus-within:ring-primary-400/30 dark:focus-within:ring-primary-600/20', headerClass: 'border-gray-100 bg-gray-50/50 dark:border-gray-800 dark:bg-gray-900/50', textClass: 'text-gray-900 dark:text-gray-100' })
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const copied = ref(false)
const lineCount = computed(() => { if (!props.modelValue) return 0; return props.modelValue.split('\n').length })
function focusTextarea() { textareaRef.value?.focus() }
function onInput(e: Event) { const target = e.target as HTMLTextAreaElement; emit('update:modelValue', target.value) }
function onKeydown(e: KeyboardEvent) { if (e.key === 'Tab') { e.preventDefault(); const ta = textareaRef.value; if (!ta) return; const start = ta.selectionStart; const end = ta.selectionEnd; const val = props.modelValue; if (e.shiftKey) { const lineStart = val.lastIndexOf('\n', start - 1) + 1; const line = val.substring(lineStart, start); const match = line.match(/^ {2,4}|\t/); if (match) { const newVal = val.substring(0, lineStart) + line.slice(match[0].length) + val.substring(start); emit('update:modelValue', newVal); requestAnimationFrame(() => { ta.selectionStart = ta.selectionEnd = start - match[0].length }) } } else { const newVal = val.substring(0, start) + '  ' + val.substring(end); emit('update:modelValue', newVal); requestAnimationFrame(() => { ta.selectionStart = ta.selectionEnd = start + 2 }) } } }
function copy() { if (!props.modelValue) return; navigator.clipboard.writeText(props.modelValue); copied.value = true; setTimeout(() => (copied.value = false), 1500) }
defineExpose({ focus: focusTextarea, textareaRef })
</script>