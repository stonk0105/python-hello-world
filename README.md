# Python Hello World with Next.js

這個專案展示了如何在 Vercel 上整合 Next.js 前端與 Python Serverless Function 後端。

## 架構

- **前端**：Next.js 13+ App Router (TypeScript)
- **後端**：Python Serverless Function (`/api/index.py`)

## 功能

- Next.js 前端頁面調用 Python API
- 顯示 API 回應的 "Hello, world!" 訊息
- 錯誤處理和載入狀態
- 響應式設計

## 本地開發

### 使用 Next.js 開發伺服器（推薦）

```bash
# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

前端將在 `http://localhost:3000` 運行，Python API 可以通過 `http://localhost:3000/api` 訪問。

### 使用 Vercel CLI（完整測試）

```bash
# 安裝 Vercel CLI
npm i -g vercel

# 啟動 Vercel 開發環境（包含 Serverless Functions）
vercel dev
```

這將同時運行 Next.js 前端和 Python Serverless Functions。

## 專案結構

```
python-hello-world/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # 根佈局
│   ├── page.tsx           # 主頁面
│   └── globals.css        # 全域樣式
├── api/                    # Python Serverless Functions
│   └── index.py           # Python API 端點
├── package.json           # Node.js 依賴
├── next.config.js         # Next.js 配置
├── tsconfig.json          # TypeScript 配置
└── vercel.json            # Vercel 配置
```

## 部署

### 部署到 Vercel

1. 將專案推送到 GitHub
2. 在 [Vercel](https://vercel.com) 中導入專案
3. Vercel 會自動偵測 Next.js 和 Python 配置並部署

或者使用 Vercel CLI：

```bash
vercel
```

## API 端點

- **GET /api** - 返回 "Hello, world!" 訊息（Python Serverless Function）

## 技術棧

- [Next.js 14](https://nextjs.org/) - React 框架
- [React 18](https://react.dev/) - UI 庫
- [TypeScript](https://www.typescriptlang.org/) - 類型安全
- [Python 3.9](https://www.python.org/) - 後端 API
- [Vercel](https://vercel.com/) - 部署平台
