import { createRouter, createWebHistory } from 'vue-router'
import { toolRegistry } from '@/plugin-system/tool-registry'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage.vue'),
  },
]

// 动态生成工具路由
for (const tool of toolRegistry) {
  routes.push({
    path: `/tool/${tool.id}`,
    name: `tool-${tool.id}`,
    component: () => import(`@/tools/${tool.id}/index.vue`),
    meta: { tool },
  })
}

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
