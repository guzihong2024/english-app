# 🎧 AI 英语动态学习平台 (AI English Learning Platform)

这是一个基于 Flask 和 Google Gemini AI 的英语辅助学习工具。它允许用户上传英语课文（PDF）和配套音频（MP3），自动生成双语对照阅读界面，并提供深度的语法分析。

## ✨ 核心功能

* **双语对照阅读**：
    * 支持 **Google 免费翻译** (默认，无限制)。
    * 支持 **DeepL** 和 **百度翻译** (需配置 API Key)。
    * 智能分段，英文在上，中文在下，阅读体验极佳。
* **AI 智能语法分析**：
    * 集成 **Gemini 2.5 Flash** 模型。
    * 自动拆解长难句，分析主语、谓语、宾语结构。
    * 提供时态分析和核心词汇讲解。
* **多媒体学习**：
    * 内嵌音频播放器，边听边读。
* **响应式设计**：
    * 基于 Bootstrap 5，手机和电脑端完美适配。
    * 后台管理界面，方便老师/管理员上传课件。

## 🛠️ 技术栈

* **后端**：Python 3.10+, Flask
* **数据库**：SQLite
* **AI 模型**：Google Gemini 2.5 Flash
* **翻译引擎**：Deep-translator (Google), DeepL API, Baidu Fanyi API
* **文件处理**：pypdf (PDF解析)
* **前端**：HTML5, CSS3, Bootstrap 5

## 🚀 快速开始 (本地运行)

### 1. 克隆项目
```bash
git clone [https://github.com/你的用户名/english-app.git](https://github.com/你的用户名/english-app.git)
cd english-app