<template>
  <header class="flex h-14 items-center gap-3 border-b border-gray-200 bg-white px-4 dark:border-gray-800 dark:bg-gray-900">
    <!-- 移动端汉堡菜单 -->
    <button
      @click="toggleSidebar"
      class="rounded-lg p-1.5 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden"
    >
      <span class="text-lg">☰</span>
    </button>

    <!-- 面包屑 / 当前工具名 -->
    <div class="flex items-center gap-2 min-w-0">
      <router-link to="/" class="text-sm text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 shrink-0">
        OnlineTools
      </router-link>
      <template v-if="currentTool">
        <span class="text-gray-300 dark:text-gray-600">/</span>
        <span class="text-sm font-medium text-gray-700 dark:text-gray-200 truncate">
          {{ currentTool.name }}
        </span>
      </template>
    </div>

    <div class="flex-1" />

    <!-- 搜索 -->
    <div class="relative max-w-xs flex-1 hidden sm:block">
      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔍</span>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索工具..."
        class="w-full rounded-lg border border-gray-200 bg-gray-50 py-1.5 pl-9 pr-3 text-sm
               placeholder-gray-400 transition-colors
               focus:border-primary-400 focus:bg-white focus:outline-none
               focus:ring-1 focus:ring-primary-400
               dark:border-gray-700 dark:bg-gray-800 dark:placeholder-gray-500
               dark:focus:border-primary-500 dark:focus:bg-gray-800"
        @input="onSearchInput"
      />
      <!-- 搜索结果下拉 -->
      <div
        v-if="searchResults.length > 0 && searchQuery"
        class="absolute left-0 right-0 top-full mt-1 z-50 rounded-lg border border-gray-200
               bg-white shadow-lg dark:border-gray-700 dark:bg-gray-900 overflow-hidden"
      >
        <router-link
          v-for="tool in searchResults"
          :key="tool.id"
          :to="`/tool/${tool.id}`"
          class="flex items-center gap-3 px-4 py-2.5 text-sm hover:bg-gray-50
                 dark:hover:bg-gray-800 transition-colors"
          @click="searchQuery = ''; searchResults = []"
        >
          <span class="shrink-0">{{ tool.icon }}</span>
          <div class="min-w-0">
            <div class="font-medium text-gray-700 dark:text-gray-200 truncate">{{ tool.name }}</div>
            <div class="text-xs text-gray-400 truncate">{{ tool.description }}</div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- 暗色模式切换 -->
    <button
      @click="store.toggleDark()"
      class="rounded-lg p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      :title="isDark ? '切换到亮色模式' : '切换到暗色模式'"
    >
      <span class="text-base">{{ isDark ? '☀️' : '🌙' }}</span>
    </button>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { searchTools } from '@/plugin-system/tool-registry'
import type { ToolMeta } from '@/types/tool'

const store = useAppStore()
const route = useRoute()
const isDark = computed(() => store.isDark)
const sidebarCollapsed = computed(() => store.sidebarCollapsed)
const { toggleSidebar } = store

const currentTool = computed(() => {
  const meta = route.meta?.tool as ToolMeta | undefined
  return meta ?? null
})

const searchQuery = ref('')
const searchResults = ref<ToolMeta[]>([])

function onSearchInput() {
  searchResults.value = searchTools(searchQuery.value).slice(0, 8)
}
</script>
