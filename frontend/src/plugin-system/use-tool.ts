import { toolRegistry, toolCategories } from './tool-registry'
import type { ToolMeta } from '@/types/tool'

export function useTool() {
  function getTool(id: string): ToolMeta | undefined {
    return toolRegistry.find(t => t.id === id)
  }

  function getCategoryName(categoryId: string): string {
    return toolCategories.find(c => c.id === categoryId)?.name ?? categoryId
  }

  return { tools: toolRegistry, getTool, getCategoryName }
}
