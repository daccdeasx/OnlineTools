import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 暗色模式
  const isDark = ref(false)

  function toggleDark() {
    isDark.value = !isDark.value
    applyTheme()
  }

  function applyTheme() {
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  // 搜索
  const searchQuery = ref('')

  // 侧边栏折叠
  const sidebarCollapsed = ref(false)
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // 收藏
  const favorites = ref<string[]>([])

  function toggleFavorite(toolId: string) {
    const idx = favorites.value.indexOf(toolId)
    if (idx > -1) {
      favorites.value.splice(idx, 1)
    } else {
      favorites.value.push(toolId)
    }
  }

  function isFavorite(toolId: string): boolean {
    return favorites.value.includes(toolId)
  }

  // 历史记录
  const MAX_HISTORY = 20
  const history = ref<string[]>([])

  function addHistory(toolId: string) {
    const idx = history.value.indexOf(toolId)
    if (idx > -1) {
      history.value.splice(idx, 1)
    }
    history.value.unshift(toolId)
    if (history.value.length > MAX_HISTORY) {
      history.value.pop()
    }
  }

  return {
    isDark,
    toggleDark,
    applyTheme,
    searchQuery,
    sidebarCollapsed,
    toggleSidebar,
    favorites,
    toggleFavorite,
    isFavorite,
    history,
    addHistory,
  }
})
