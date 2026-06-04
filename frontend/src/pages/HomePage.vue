<template>
  <div class="flex-1 overflow-y-auto">
    <div class="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <!-- 欢迎区域 -->
      <div class="mb-10">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">
          OnlineTools
        </h1>
        <p class="mt-2 text-sm text-gray-500 dark:text-gray-400 max-w-xl">
          轻量级在线工具箱，所有计算在浏览器端完成，保护你的数据隐私。打开即用，无需注册。
        </p>
      </div>

      <!-- 按分类展示工具 -->
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="mb-10"
      >
        <h2 class="mb-4 flex items-center gap-2 text-base font-semibold text-gray-700 dark:text-gray-200">
          <span class="text-lg">{{ cat.icon }}</span>
          {{ cat.name }}
        </h2>
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <router-link
            v-for="tool in getToolsByCategory(cat.id)"
            :key="tool.id"
            :to="`/tool/${tool.id}`"
            class="group flex flex-col gap-2 rounded-xl border border-gray-200 bg-white p-4
                   transition-all hover:border-primary-300 hover:shadow-md hover:-translate-y-0.5
                   dark:border-gray-800 dark:bg-gray-900 dark:hover:border-primary-700"
          >
            <div class="flex items-center gap-3">
              <span class="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-50
                           text-xl dark:bg-primary-950">
                {{ tool.icon }}
              </span>
              <div class="min-w-0">
                <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {{ tool.name }}
                </div>
                <div class="mt-0.5 text-xs text-gray-400 line-clamp-2">
                  {{ tool.description }}
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 空状态 -->
      <div
        v-if="toolRegistry.length === 0"
        class="flex flex-col items-center justify-center py-20 text-gray-400"
      >
        <span class="text-6xl mb-4">🧰</span>
        <p class="text-sm">工具箱正在搭建中，敬请期待...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toolRegistry, toolCategories, getToolsByCategory } from '@/plugin-system/tool-registry'

const categories = toolCategories
</script>
