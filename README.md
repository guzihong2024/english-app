# 🎧 AI 英语动态学习平台 (AI English Learning Platform)

这是一个基于 Flask 和 Google Gemini AI 的英语辅助学习工具。它允许用户上传英语课文（PDF）和配套音频（MP3），自动生成双语对照阅读界面，并提供深度的语法分析。

## ✨ 核心功能

* **双语对照阅读**：
    * 支持 **Google 免费翻译** (默认，无限制)。
    * 支持 **DeepL** 和 **百度翻译** (需配置 API Key)。
* **AI 智能语法分析**：
    * 集成 **Gemini 2.5 Flash** 模型。
    * 自动拆解长难句，分析主语、谓语、宾语结构。
* **多媒体学习**：
    * 内嵌音频播放器，边听边读。

---

## 🛠️ 技术栈

* **后端**：Python 3.10+, Flask
* **数据库**：SQLite
* **AI 模型**：Google Gemini 2.5 Flash
* **文件处理**：pypdf (PDF解析)
* **前端**：HTML5, CSS3, Bootstrap 5

---

## 🚀 快速开始 (本地运行)

如果你想在自己的电脑上运行这个项目，请按以下步骤操作：

### 1. 克隆项目
```bash
git clone [https://github.com/你的用户名/english-app.git](https://github.com/你的用户名/english-app.git)
cd english-app

# ==========================================================
# 步骤 1: 准备工作 (在你的 WSL/本地终端执行)
# ==========================================================

# 确保进入项目文件夹 (如果刚克隆项目)
cd english-app

# 安装所有依赖 (用于本地运行和开发环境)
pip install -r requirements.txt

# 首次运行程序，自动创建数据库文件 (my_database.db)
# 看到 "Running on..." 后按 Ctrl+C 停止
python app.py 

# ==========================================================
# 步骤 2: 部署到 PythonAnywhere (在 PA 的 Bash 控制台中执行)
# ==========================================================

# 1. 再次安装依赖 (安装到 PA 的特定 Python 版本)
# ⚠️ 注意: 请将 X 替换为你的 Web App Python 版本，例如 pip3.10
pip3.X install -r requirements.txt --user

# 2. 数据库初始化 (如果网站报 no such table 错误，运行此命令)
# 强制让服务器运行建表函数
python3 -c "from app import init_db; init_db()"

# 3. [下一步操作] 完成后，请去 PythonAnywhere 的 Web 标签页点击 "Reload"。