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

### 使用 Vercel CLI（推薦 - 包含 Python Serverless Functions）

**重要**：Python Serverless Functions 需要使用 `vercel dev` 才能正常運行。

```bash
# 安裝 Vercel CLI（如果尚未安裝）
npm i -g vercel

# 安裝依賴
npm install

# 啟動 Vercel 開發環境（包含 Next.js 和 Python Serverless Functions）
vercel dev
# 或使用：npm run dev:vercel
```

這將同時運行 Next.js 前端和 Python Serverless Functions，前端在 `http://localhost:3000` 運行。

### 僅使用 Next.js 開發伺服器（不包含 Python API）

如果只想測試前端部分（Python API 將無法訪問）：

```bash
npm run dev
```

**注意**：使用 `npm run dev` 時，`/api` 端點將返回 404，因為 Python Serverless Functions 不會運行。要同時運行 Python API，必須使用 `vercel dev`。

## 專案結構

```
python-hello-world/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # 根佈局
│   ├── page.tsx           # 主頁面
│   └── globals.css        # 全域樣式
├── api/                    # Python Serverless Functions
│   ├── index.py           # Python API 端點
│   └── download-report.py # 圖片下載端點
├── Label_Data/            # 圖片資料目錄
│   └── pitcher1.jpg       # 情蒐報告圖片
├── package.json           # Node.js 依賴
├── requirements.txt       # Python 依賴（Vercel 自動安裝）
├── next.config.js         # Next.js 配置
├── tsconfig.json          # TypeScript 配置
└── vercel.json            # Vercel 配置
```

## Python 依賴管理

### 添加 Python 庫

在 Vercel 上使用 Python Serverless Functions 時，需要通過 `requirements.txt` 文件來指定依賴：

1. **編輯 `requirements.txt`**：
```txt
# 添加需要的庫
Pillow>=10.0.0
pandas>=2.0.0
```

2. **部署時自動安裝**：
   - Vercel 會在部署時自動檢測 `requirements.txt`
   - 自動安裝所有列出的 Python 庫
   - 無需手動配置

3. **常用的圖片處理庫**：
```txt
# 生成圖片
Pillow>=10.0.0

# 數據處理
pandas>=2.0.0
numpy>=1.24.0

# 繪圖
matplotlib>=3.7.0
```

### 本地測試 Python 庫

在本地開發時，如果使用了第三方庫，需要先安裝：

```bash
# 創建虛擬環境（可選）
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
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
- **GET /api/download-report** - 下載情蒐報告圖片（Python Serverless Function）

## 技術棧

- [Next.js 14](https://nextjs.org/) - React 框架
- [React 18](https://react.dev/) - UI 庫
- [TypeScript](https://www.typescriptlang.org/) - 類型安全
- [Python 3.9](https://www.python.org/) - 後端 API
- [Vercel](https://vercel.com/) - 部署平台

1
