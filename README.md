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