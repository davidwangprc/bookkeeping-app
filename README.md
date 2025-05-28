# 🔬 科研经费管理系统（Streamlit + Google Sheets）

一个支持多人协作、可实时记录和统计的科研经费报销管理系统。基于 [Streamlit](https://streamlit.io) 和 [Google Sheets API]() 构建，数据云端同步，界面清晰易用，适合教师/科研人员团队使用。

***

## ✨ 功能特性

* 📝 报销记录快速录入（项目、金额、科目、备注）

* 📊 自动统计报销金额（按项目、用户、科目分类汇总）

* 📋 明细筛选 + 导出 CSV 报表

* 👥 支持多用户身份

* ☁️ 实时保存至 Google Sheets，无需本地数据库

***

## 📁 项目结构

```
bash
复制编辑
bookkeeping-app/
├── app.py                  # 主应用程序
├── requirements.txt        # 依赖列表
├── .gitignore              # 忽略私钥等敏感文件
└── gcp_credentials.json    # Google Cloud 服务凭证（仅部署时用）
```

***

## 🚀 快速开始

### ✅ 1. 克隆项目

```
bash
复制编辑
git clone https://github.com/your-username/bookkeeping-app.git
cd bookkeeping-app
```

### ✅ 2. 安装依赖

建议创建虚拟环境：

```
bash
复制编辑
pip install -r requirements.txt
```

***

## ☁️ 使用 Google Sheets 存储数据

### 🧾 1. 创建 Google Sheet

* 创建名为 `bookkeeping` 的 Google 表格

* 新建工作表名为 `报销记录`

* 设置第一行为表头：

```
text
复制编辑
项目代码, 日期, 科目名称, 报销到账, 用户, 备注
```

***

### 🔐 2. 创建 Google 服务帐号并授权

1. 登录 [Google Cloud Console]()

2. 创建项目并启用以下 API：

   * Google Sheets API

   * Google Drive API

3. 创建服务帐号，生成 JSON 密钥

4. 将服务帐号的邮箱地址添加为 Google 表格的“编辑者”

***

### 🔐 3. 使用方式一：本地 secrets.toml（本地调试用）

在 `.streamlit/secrets.toml` 添加如下内容：

```
toml
复制编辑
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key = "..."
client_email = "..."
...
```

> ⚠️ 建议将 `.streamlit/secrets.toml` 添加到 `.gitignore`，避免提交至 GitHub。

***

### ☁️ 4. 使用方式二：部署到 Streamlit Cloud

1. 上传代码至 GitHub（推荐设置为私有仓库）

2. 打开 [Streamlit Cloud](https://share.streamlit.io) → 创建 App

3. 在 “Secrets” 配置中粘贴你的 JSON 内容：

```
toml
复制编辑
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key = "..."
client_email = "..."
...
```

***

## 🖥️ 本地运行

```
bash
复制编辑
streamlit run app.py
```

***

## 📦 依赖说明

```
txt
复制编辑
streamlit
gspread
google-auth
pandas
```

***

## 📤 部署建议

* 私钥文件（`gcp_credentials.json`）仅限部署调试时使用，推荐使用 secrets 管理

* 若多人协作，可提供 `.example.secrets.toml` 模板说明字段结构

* 若长期使用，建议启用表格备份防止误删

***

## 📷 截图预览（可选）

可添加：

* 新增记录界面

* 统计图表（项目、用户、科目）

* 数据筛选与导出功能界面

***

## 📄 License

MIT License

***

如需，我可以生成 `.gitignore`、`.example.secrets.toml`、部署模板文件或自动推送到你的 GitHub 仓库。是否继续？
