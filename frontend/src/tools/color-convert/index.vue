<template>
  <div class="flex h-full flex-col p-4 sm:p-6">
    <div class="mb-4"><h1 class="text-lg font-semibold text-gray-900 dark:text-white">颜色转换</h1><p class="mt-1 text-xs text-gray-500 dark:text-gray-400">HEX / RGB / HSL 颜色格式互转</p></div>
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <div class="flex gap-1 rounded-lg bg-gray-100 p-1 dark:bg-gray-800">
        <button v-for="f in formats" :key="f" @click="inputFormat = f; convert()"
          :class="['rounded-md px-3 py-1.5 text-xs font-medium transition-all', inputFormat === f ? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200']">{{ f }}</button>
      </div>
      <input v-model="input" type="text" :placeholder="placeholders[inputFormat]" class="tool-input flex-1 font-mono text-xs" @input="convert" />
      <div class="h-9 w-9 rounded-lg border border-gray-200 shrink-0" :style="{ background: currentColor }"></div>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <div v-for="f in formats" :key="f" class="tool-panel">
        <div class="tool-panel-header flex items-center justify-between">
          <span class="text-xs font-medium text-gray-500 dark:text-gray-400">{{ f }}</span>
          <button @click="copyVal(results[f] || '')" class="rounded px-1.5 py-0.5 text-[11px] text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors">复制</button>
        </div>
        <div class="p-3 font-mono text-[13px] min-h-[42px] flex items-center text-gray-900 dark:text-gray-100 select-all">{{ results[f] || '-' }}</div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore(); store.addHistory('color-convert')
const formats = ['HEX', 'RGB', 'HSL']; const inputFormat = ref('HEX'); const input = ref('#3B82F6')
const results = reactive<Record<string, string>>({ HEX: '', RGB: '', HSL: '' })
const currentColor = ref('#3B82F6')
const placeholders: Record<string, string> = { HEX: '#3B82F6 或 3B82F6', RGB: 'rgb(59,130,246) 或 59,130,246', HSL: 'hsl(217,91%,60%) 或 217,91,60' }

function parseHEX(s: string): [number, number, number] | null {
  s = s.replace('#', '').trim()
  if (s.length === 3) s = s[0]+s[0]+s[1]+s[1]+s[2]+s[2]
  if (!/^[0-9A-Fa-f]{6}$/.test(s)) return null
  return [parseInt(s.slice(0,2),16), parseInt(s.slice(2,4),16), parseInt(s.slice(4,6),16)]
}

function parseRGB(s: string): [number, number, number] | null {
  const m = s.match(/[\d.]+/g); if (!m || m.length < 3) return null
  return [Math.min(255, Math.max(0, Number(m[0])|0)), Math.min(255, Math.max(0, Number(m[1])|0)), Math.min(255, Math.max(0, Number(m[2])|0))]
}

function parseHSL(s: string): [number, number, number] | null {
  const m = s.match(/[\d.]+/g); if (!m || m.length < 3) return null
  return [Number(m[0]) % 360, Math.min(100, Math.max(0, Number(m[1]))), Math.min(100, Math.max(0, Number(m[2])))]
}

function rgbToHsl(r: number, g: number, b: number): [number, number, number] {
  r /= 255; g /= 255; b /= 255; const mx = Math.max(r,g,b), mn = Math.min(r,g,b); const d = mx - mn; let h = 0, s = 0; const l = (mx + mn) / 2
  if (d !== 0) { s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); if (mx === r) h = ((g-b)/d+(g<b?6:0))/6; else if (mx === g) h = ((b-r)/d+2)/6; else h = ((r-g)/d+4)/6 }
  return [Math.round(h*360), Math.round(s*100), Math.round(l*100)]
}

function hslToRgb(h: number, s: number, l: number): [number, number, number] {
  h /= 360; s /= 100; l /= 100; if (s === 0) { const v = Math.round(l*255); return [v,v,v] }
  const q = l < 0.5 ? l*(1+s) : l+s-l*s; const p = 2*l - q
  const hueToRgb = (t: number) => { if (t < 0) t += 1; if (t > 1) t -= 1; if (t < 1/6) return p+(q-p)*6*t; if (t < 1/2) return q; if (t < 2/3) return p+(q-p)*(2/3-t)*6; return p }
  return [Math.round(hueToRgb(h+1/3)*255), Math.round(hueToRgb(h)*255), Math.round(hueToRgb(h-1/3)*255)]
}

function convert() {
  let rgb: [number, number, number] | null = null
  if (inputFormat.value === 'HEX') rgb = parseHEX(input.value)
  else if (inputFormat.value === 'RGB') rgb = parseRGB(input.value)
  else { const h = parseHSL(input.value); if (h) rgb = hslToRgb(h[0], h[1], h[2]) }
  if (!rgb) { results.HEX = results.RGB = results.HSL = ''; return }
  const [r, g, b] = rgb
  results.HEX = '#' + [r,g,b].map(x=>x.toString(16).padStart(2,'0').toUpperCase()).join('')
  results.RGB = `rgb(${r}, ${g}, ${b})`
  const [hh, ss, ll] = rgbToHsl(r,g,b); results.HSL = `hsl(${hh}, ${ss}%, ${ll}%)`
  currentColor.value = results.HEX
}

function copyVal(v: string) { if (v) navigator.clipboard.writeText(v) }

convert()
</script>