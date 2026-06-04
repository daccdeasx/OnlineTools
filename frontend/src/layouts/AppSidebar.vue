<template>
  <aside
    :class="[
      'flex flex-col border-r border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900 transition-all duration-200',
      sidebarCollapsed ? 'w-16' : 'w-60'
    ]"
  >
    <!-- Logo -->
    <div class="flex h-14 items-center gap-3 border-b border-gray-200 px-4 dark:border-gray-800">
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white font-bold text-sm shrink-0">
        OT
      </div>
      <span
        v-show="!sidebarCollapsed"
        class="text-sm font-semibold text-gray-900 dark:text-white whitespace-nowrap"
      >
        OnlineTools
      </span>
    </div>

    <!-- 导航区域 -->
    <nav class="flex flex-1 flex-col gap-1 overflow-y-auto p-2">
      <router-link
        to="/"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors
               text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800"
        :class="{ 'justify-center': sidebarCollapsed }"
        active-class="!bg-primary-50 !text-primary-700 dark:!bg-primary-950 dark:!text-primary-400"
      >
        <span class="flex h-5 w-5 items-center justify-center shrink-0">🏠</span>
        <span v-show="!sidebarCollapsed" class="truncate">首页</span>
      </router-link>

      <!-- 分类 + 工具 -->
      <template v-for="cat in categories" :key="cat.id">
        <div
          v-show="!sidebarCollapsed"
          class="mt-3 mb-1 px-3 text-[11px] font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500"
        >
          {{ cat.name }}
        </div>
        <router-link
          v-for="tool in getToolsByCategory(cat.id)"
          :key="tool.id"
          :to="`/tool/${tool.id}`"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors
                 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800"
          :class="{ 'justify-center': sidebarCollapsed }"
          active-class="!bg-primary-50 !text-primary-700 dark:!bg-primary-950 dark:!text-primary-400"
          :title="sidebarCollapsed ? tool.name : ''"
        >
          <span class="flex h-5 w-5 items-center justify-center shrink-0 text-xs">{{ tool.iconText ?? '🔧' }}</span>
          <span v-show="!sidebarCollapsed" class="truncate">{{ tool.name }}</span>
        </router-link>
      </template>
    </nav>

    <!-- 底部按钮 -->
    <div class="border-t border-gray-200 p-2 dark:border-gray-800">
      <button
        @click="toggleSidebar"
        class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-gray-400
               hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        :class="{ 'justify-center': sidebarCollapsed }"
      >
        <span class="flex h-5 w-5 items-center justify-center shrink-0">
          {{ sidebarCollapsed ? '▶' : '◀' }}
        </span>
        <span v-show="!sidebarCollapsed">收起侧栏</span>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { toolRegistry, toolCategories, getToolsByCategory } from '@/plugin-system/tool-registry'

const store = useAppStore()
const sidebarCollapsed = computed(() => store.sidebarCollapsed)
const categories = toolCategories
const { toggleSidebar } = store
</script>
