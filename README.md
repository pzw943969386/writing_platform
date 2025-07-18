# 文章拉取 (Rewrite Spider)

一个用于抓取、存储和展示网络文章的全栈 Web 应用。后端基于 FastAPI 构建，前端则采用 Vue.js。

## ✨ 功能特性

-   从目标网站抓取文章标题和链接。
-   使用 SQLite 数据库对文章数据进行持久化存储。
-   在用户需要时，懒加载并显示文章全文内容。
-   提供一个现代化的、响应式的前端界面来浏览文章。
-   通过 RESTful API 对文章数据进行管理。

## 🛠️ 技术栈

-   **后端**: Python, FastAPI, SQLAlchemy, aiosqlite
-   **前端**: Vue 3, Vite, TypeScript, Element Plus, Axios
-   **数据库**: SQLite

## 🚀 快速开始

请遵循以下步骤，在您的本地机器上获取并运行一个开发和测试环境。

### 环境准备

在开始之前，请确保您的系统上已经安装了以下软件：

-   [Python](https://www.python.org/downloads/) (推荐 3.8+ 版本)
-   [Node.js](https://nodejs.org/) (推荐 v18+ 版本) 和 npm

### 安装步骤

1.  **克隆代码仓库:**
    ```sh
    git clone <你的代码仓库链接>
    cd rewrite-spider
    ```

2.  **配置后端环境:**
    我们强烈建议使用虚拟环境来管理依赖。
    ```sh
    # 进入后端目录
    cd backend

    # 创建并激活虚拟环境
    python -m venv .venv
    # 在 Windows 上激活
    .\.venv\Scripts\activate
    # 在 macOS/Linux 上激活
    # source .venv/bin/activate

    # 从项目根目录安装 Python 依赖
    pip install -r ../requirements.txt

    # 返回项目根目录
    cd ..
    ```

3.  **配置前端环境:**
    ```sh
    # 进入前端目录
    cd frontend

    # 安装 Node.js 依赖
    npm install
    ```

### 运行项目 (开发模式)

我们提供了一个便捷的脚本，可以一键同时启动后端和前端的开发服务器。

**在 Windows 系统上:**

1.  在项目的根目录 (`rewrite-spider`) 打开一个 PowerShell 终端。

2.  如果您是首次运行 `.ps1` 脚本，可能需要为当前进程设置执行策略。每个终端会话只需设置一次。
    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```

3.  运行启动脚本：
    ```powershell
    .\start-dev.ps1
    ```

这个命令会打开两个新的终端窗口：
-   一个用于 **FastAPI 后端服务**，它会运行在 `http://localhost:8888` 并开启自动重载。
-   一个用于 **Vite 前端服务**，它会运行在 `http://localhost:5173` (或其它可用端口) 并支持热模块替换 (HMR)。

现在，您的应用应该已经在浏览器中成功运行起来了。

## 📁 项目结构
rewrite-spider/
├── backend/ # FastAPI 后端源代码
│ ├── api/ # API 接口路由
│ ├── models/ # Pydantic 和 SQLAlchemy 模型
│ ├── services/ # 核心业务逻辑和服务
│ ├── utils/ # 工具模块 (如数据库连接)
│ └── application.py # FastAPI 应用主实例
├── frontend/ # Vue.js 前端源代码
│ ├── public/
│ └── src/
│ ├── api/ # API 请求定义
│ ├── components/ # 可复用的 Vue 组件
│ ├── views/ # 页面组件
│ ├── service/ # Axios 请求配置
│ └── main.ts # 前端入口文件
├── requirements.txt # Python 依赖清单
├── start-dev.ps1 # Windows 开发环境启动脚本
└── README.md