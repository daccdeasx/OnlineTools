import type { ToolMeta } from '@/types/tool'
import { toolRegistry } from '@/plugin-system/tool-registry'

export function getToolMeta(): ToolMeta {
  return toolRegistry.find(t => t.id === 'base64')!
}
