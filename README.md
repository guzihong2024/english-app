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

2. 安装依赖
Bash

pip install -r requirements.txt
3. 配置环境变量
在项目根目录创建一个 .env 文件，填入你的密钥：

代码段

GEMINI_API_KEY=你的_Google_Gemini_Key
ADMIN_PASSWORD=123456
FLASK_SECRET_KEY=随便写一个复杂的字符串
4. 运行
Bash

python app.py
访问 http://127.0.0.1:5000 即可使用。

☁️ 部署指南 (PythonAnywhere)
本项目已针对 PythonAnywhere 部署进行路径优化。

1. 上传代码
在 PythonAnywhere 的 Bash 控制台中克隆代码：

Bash

git clone [https://github.com/你的用户名/english-app.git](https://github.com/你的用户名/english-app.git)
2. 安装依赖
在项目文件夹内执行：

Bash

# 请根据你的 Web App 版本选择 pip (如 pip3.10)
pip3.X install -r requirements.txt --user
3. 配置环境变量
在服务器上创建 .env 文件（和 app.py 同一级），并填入密钥。

4. 配置 WSGI 路径
在 Web 选项卡中，修改 WSGI 配置文件，将路径指向项目文件夹：

Python

# 确保路径指向 /home/你的用户名/english-app
path = '/home/你的用户名/english-app' 
# ... (其他代码保持不变) ...
5. 数据库初始化
如果遇到 no such table 错误，请在浏览器中访问以下路由进行自动修复： 访问网址： https://你的域名.pythonanywhere.com/fix-db