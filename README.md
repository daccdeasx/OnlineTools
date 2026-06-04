# OnlineTools - 在线工具箱

> 轻量级、高性能的在线工具箱，**打开即用、本地处理、隐私优先**。  
> 适合开发者、运维人员和日常办公用户。

[![Vue 3](https://img.shields.io/badge/Vue-3.5-42b883?logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![PWA](https://img.shields.io/badge/PWA-Enabled-5A0FC8?logo=pwa)](https://web.dev/progressive-web-apps/)

---

## ✨ 特点

- 🔒 **隐私优先** – 大部分工具在浏览器本地完成计算，不上传用户数据
- ⚡ **极致性能** – 按需加载 + Web Worker 计算，首屏 < 1.5s
- 📱 **PWA 支持** – 可安装为桌面应用，离线使用核心工具
- 🎨 **暗色模式** – 跟随系统或手动切换
- 🧩 **插件化架构** – 每个工具独立开发、独立加载

---

## 🛠️ 工具列表

### 编解码工具
- Base64 编解码
- URL 编解码
- Unicode 转换
- HTML 实体编解码

### 格式化工具
- JSON 格式化 & 校验
- XML 格式化
- SQL 格式化

### 加解密 & 签名
- MD5 / SHA 系列哈希
- AES 加解密
- JWT 解析调试

### 转换工具
- 时间戳转换
- 进制转换 (2/8/10/16/32/64)
- 颜色转换 (HEX/RGB/HSL)
- 字符编码转换 (UTF-8/GBK/ISO)

### 生成器
- UUID 生成 (v1/v4)
- 随机密码生成
- 二维码生成

### 文本处理
- 文本去重 / 排序
- 大小写转换
- 正则表达式测试

> 更多工具持续添加中……

---

## 🧰 技术栈

### 前端

| 技术 | 用途 |
|------|------|
| Vue 3 | 核心框架 (Composition API) |
| TypeScript | 类型安全 |
| Vite | 构建工具，极速 HMR |
| Vue Router | SPA 路由 |
| Pinia | 全局 UI 状态管理 |
| Tailwind CSS | 原子化样式 |
| CodeMirror 6 | 代码编辑器 |
| Web Worker | 计算线程，避免 UI 卡顿 |
| PWA | vite-plugin-pwa，离线缓存 |

### 后端（轻量辅助，仅必要场景）

| 技术 | 用途 |
|------|------|
| FastAPI | 高性能异步 API 框架 |
| Uvicorn | ASGI 服务器 |
| Pydantic | 数据校验 |
| Pillow | 图片处理 |
| slowapi | 限流 |
| Docker | 容器化部署 |

### 部署

- Nginx (反向代理 + 静态资源缓存)
- CDN (静态资源加速)
- Docker Compose (一键启动)

---

## 🚀 快速体验

### 在线使用

> 待部署后补充链接

### 本地运行

```bash
# 前端
cd frontend
npm install
npm run dev

# 后端 (可选，仅高级功能需要)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
