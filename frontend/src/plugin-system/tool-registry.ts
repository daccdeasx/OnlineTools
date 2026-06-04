import type { ToolMeta, ToolCategory } from '@/types/tool'

export const toolCategories: ToolCategory[] = [
  { id: 'codec', name: '编解码', icon: 'ArrowLeftRight' },
  { id: 'format', name: '格式化', icon: 'AlignLeft' },
  { id: 'crypto', name: '加解密', icon: 'Shield' },
  { id: 'convert', name: '转换', icon: 'Repeat' },
  { id: 'generate', name: '生成器', icon: 'Sparkles' },
  { id: 'text', name: '文本处理', icon: 'FileText' },
  { id: 'image', name: '图片处理', icon: 'Image' },
]

export const toolRegistry: ToolMeta[] = [
  { id: 'base64', name: 'Base64 编解码', description: 'Base64 编码与解码，支持中文', category: 'codec', keywords: ['base64', '编码', '解码', 'encode', 'decode'], icon: '🔤' },
  { id: 'url-codec', name: 'URL 编解码', description: 'URL 编码（encodeURIComponent）与解码', category: 'codec', keywords: ['url', '编码', '解码', 'percent', 'encodeURIComponent'], icon: '🔗' },
  { id: 'unicode', name: 'Unicode 转换', description: '文本与 Unicode 转义序列互转', category: 'codec', keywords: ['unicode', '转义', 'escape'], icon: '🌐' },
  { id: 'html-entity', name: 'HTML 实体编解码', description: 'HTML 实体编码（&amp;lt;）与解码', category: 'codec', keywords: ['html', '实体', 'entity', '转义'], icon: '📄' },
  { id: 'json-formatter', name: 'JSON 格式化', description: 'JSON 格式化、压缩与校验', category: 'format', keywords: ['json', '格式化', 'format', '美化', '压缩', '校验'], icon: '📋' },
  { id: 'xml-formatter', name: 'XML 格式化', description: 'XML 格式化、压缩与校验', category: 'format', keywords: ['xml', '格式化', 'format', '美化', '压缩'], icon: '📰' },
  { id: 'sql-formatter', name: 'SQL 格式化', description: 'SQL 语句格式化与压缩', category: 'format', keywords: ['sql', '格式化', 'format', 'select', 'insert'], icon: '📊' },
  { id: 'hash', name: '哈希计算', description: 'MD5 / SHA-1 / SHA-256 / SHA-512 哈希值计算', category: 'crypto', keywords: ['md5', 'sha1', 'sha256', 'sha512', 'hash', '哈希'], icon: '🔐' },
  { id: 'aes-crypto', name: 'AES 加解密', description: '基于 Web Crypto API 的 AES-CBC 加解密', category: 'crypto', keywords: ['aes', '加密', '解密', 'cbc', 'crypto'], icon: '🔒' },
  { id: 'jwt-parser', name: 'JWT 解析', description: '解码 JWT Token 的 Header 与 Payload', category: 'crypto', keywords: ['jwt', 'token', '解析', 'decode', 'jsonwebtoken'], icon: '🎫' },
  { id: 'timestamp', name: '时间戳转换', description: 'Unix 时间戳与日期相互转换', category: 'convert', keywords: ['时间戳', 'timestamp', 'unix', '日期', '转换'], icon: '🕐' },
  { id: 'number-base', name: '进制转换', description: '二进制、八进制、十进制、十六进制等互转', category: 'convert', keywords: ['进制', '二进制', '十六进制', 'hex', '转换'], icon: '🔢' },
  { id: 'charset-convert', name: '字符编码转换', description: 'UTF-8 / GBK / ISO-8859-1 / UTF-16 等编码互转', category: 'convert', keywords: ['编码', 'gbk', 'utf-8', 'utf-16', 'big5', 'charset', '转换'], icon: '📝' },
  { id: 'color-convert', name: '颜色转换', description: 'HEX / RGB / HSL 颜色格式互转', category: 'convert', keywords: ['颜色', 'hex', 'rgb', 'hsl', 'color', '转换'], icon: '🎨' },
  { id: 'uuid-gen', name: 'UUID 生成器', description: '批量生成 UUID v4 唯一标识符', category: 'generate', keywords: ['uuid', 'guid', '唯一标识', '随机', 'v4'], icon: '🎲' },
  { id: 'password-gen', name: '随机密码生成', description: '生成强密码，支持自定义长度与字符集', category: 'generate', keywords: ['密码', 'password', '随机', '强密码', '生成'], icon: '🔑' },
  { id: 'qr-generator', name: '二维码生成', description: '在线生成二维码，支持 URL、文本，可下载 PNG', category: 'generate', keywords: ['二维码', 'qr', 'qrcode', '生成', '条形码', '链接'], icon: '📷' },
  { id: 'regex', name: '正则表达式测试', description: '在线正则测试工具，支持标志位与捕获组', category: 'text', keywords: ['regex', '正则', '正则表达式', 'match', '匹配', 'grep'], icon: '🔍' },
  { id: 'text-dedup', name: '文本去重 & 排序', description: '按行去重、排序、反转、随机打乱', category: 'text', keywords: ['去重', '排序', 'dedup', 'sort', 'unique', '行'], icon: '📑' },
  { id: 'case-convert', name: '大小写转换', description: '快速转换文本大小写与命名格式', category: 'text', keywords: ['大小写', '驼峰', '蛇形', 'camelCase', 'snake_case', 'upper', 'lower'], icon: '🔠' },
  { id: 'image-processor', name: '图片处理', description: '图片压缩、格式转换与尺寸调整', category: 'image', keywords: ['图片', '压缩', 'image', 'resize', 'png', 'jpg', 'webp'], icon: '🖼️' },
]

export function getToolsByCategory(categoryId: string): ToolMeta[] { return toolRegistry.filter(t => t.category === categoryId) }

export function searchTools(query: string): ToolMeta[] {
  const q = query.toLowerCase().trim()
  if (!q) return toolRegistry
  return toolRegistry.filter(t => t.name.toLowerCase().includes(q) || t.description.toLowerCase().includes(q) || t.keywords.some(k => k.toLowerCase().includes(q)))
}

export function getToolMeta(toolId: string): ToolMeta | undefined { return toolRegistry.find(t => t.id === toolId) }