export interface ToolCategory {
  id: string
  name: string
  icon: string
}

export interface ToolMeta {
  id: string
  name: string
  description: string
  category: string
  keywords: string[]
  icon: string
}

export interface ToolAction {
  label: string
  icon?: string
  onClick: (input: string) => string | Promise<string>
}

export interface ToolResult {
  success: boolean
  data?: string
  error?: string
}
