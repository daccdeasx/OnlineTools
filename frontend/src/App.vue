<template>
  <DefaultLayout />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const store = useAppStore()

onMounted(() => {
  // 检测系统暗色模式
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  if (prefersDark) {
    store.isDark = true
  }
  store.applyTheme()
})
</script>
