import os
import json
import sqlite3
import requests
import hashlib
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# 🔥🔥🔥 核心升级：获取当前文件的绝对路径 (修复云端路径错误) 🔥🔥🔥
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. 加载 .env 文件
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ================= 🔧 代理配置 =================
# 在 PythonAnywhere 服务器上，必须注释掉这两行！
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:10808"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10808"
# ===============================================

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret')

# ================= ⚙️ 配置区域 =================
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '123456')

# 🔥 使用绝对路径设置上传文件夹
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔥 数据库文件的绝对路径
DB_PATH = os.path.join(BASE_DIR, 'my_database.db')

TRANSLATION_SOURCE = 'google_free' 
API_KEY = os.getenv('GEMINI_API_KEY')
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY', '')
BAIDU_APP_ID = os.getenv('BAIDU_APP_ID', '')
BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY', '')

# ===============================================

if not API_KEY:
    print("❌ 严重错误: 未找到 GEMINI API Key！")
    model = None
else:
    genai.configure(api_key=API_KEY)
    try:
        # ⚠️ 修正：目前稳定版是 1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    except Exception as e:
        print(f"⚠️ 模型加载警告: {e}")
        model = None

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    # 🔥 使用绝对路径连接数据库
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dialogues
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  english_text TEXT, 
                  audio_path TEXT, 
                  grammar_json TEXT,
                  source_filename TEXT,
                  translator_source TEXT)''')
    conn.commit()
    conn.close()

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            if i > 5: break 
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF 读取错误: {e}")
        return ""

def external_translate(text, source='google_free'):
    print(f"🔄 正在使用 [{source}] 引擎翻译...")
    try:
        if source == 'google_free':
            translator = GoogleTranslator(source='auto', target='zh-CN')
            return translator.translate(text[:4500])

        elif source == 'deepl':
            url = "https://api-free.deepl.com/v2/translate" 
            params = { "auth_key": DEEPL_AUTH_KEY, "text": text[:2000], "target_lang": "ZH" }
            r = requests.post(url, data=params, timeout=10)
            return r.json()['translations'][0]['text']

        elif source == 'baidu':
            url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
            salt = random.randint(32768, 65536)
            sign_str = BAIDU_APP_ID + text + str(salt) + BAIDU_SECRET_KEY
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
            params = {'q': text, 'from': 'en', 'to': 'zh', 'appid': BAIDU_APP_ID, 'salt': salt, 'sign': sign}
            r = requests.post(url, data=params, timeout=10)
            result = r.json()
            return "\n".join([item['dst'] for item in result['trans_result']])
            
    except Exception as e:
        print(f"❌ 翻译引擎报错: {e}")
        return None
    return None

def analyze_text_with_gemini(text):
    if not model:
        return json.dumps({"translation": "API Key配置错误", "structure": {}})

    short_text = text[:1500] 
    external_trans = external_translate(short_text, source=TRANSLATION_SOURCE)
    
    if external_trans:
        prompt = f"""
        分析这段英语文本: "{short_text}..."
        用户已提供标准翻译: "{external_trans}"
        任务：
        1. 必须直接使用用户提供的翻译作为 'translation' 字段。
        2. 提取第一句的语法结构 (主谓宾)。
        3. 返回纯 JSON:
        {{
            "translation": "{external_trans}",
            "structure": {{ "subject": "...", "verb": "...", "object": "..." }}
        }}
        """
    else:
        prompt = f"""
        分析这段英语文本: "{short_text}..."
        任务：
        1. 翻译成中文。
        2. 提取第一句语法结构。
        3. 返回纯 JSON:
        {{
            "translation": "中文大意...",
            "structure": {{ "subject": "...", "verb": "...", "object": "..." }}
        }}
        """
    
    try:
        print("🔄 正在请求 AI 分析语法...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        safe_fallback = {
            "translation": f"AI 连接失败: {str(e)[:50]}",
            "structure": {"subject": None, "verb": None, "object": None}
        }
        return json.dumps(safe_fallback)

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM dialogues ORDER BY id DESC")
        rows = c.fetchall()
    except sqlite3.OperationalError:
        rows = []
    conn.close()
    
    dialogues = []
    for r in rows:
        try:
            analysis = json.loads(r[3])
            if 'structure' not in analysis: analysis['structure'] = {}
        except:
            analysis = {"translation": "数据解析错误", "structure": {}}
        
        translator = r[5] if len(r) > 5 else 'unknown'
        
        dialogues.append({
            "id": r[0],     # 🔥 关键修复：必须添加 ID，否则无法删除
            "text": r[1],
            "audio": r[2],
            "analysis": analysis,
            "filename": r[4],
            "translator": translator
        })

    return render_template('index.html', dialogues=dialogues)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('❌ 密码错误')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

# ========= 🗑️ 删除功能 =========
@app.route('/delete/<int:id>', methods=['POST'])
def delete_dialogue(id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. 查找文件路径以便物理删除
    c.execute("SELECT audio_path, source_filename FROM dialogues WHERE id=?", (id,))
    row = c.fetchone()
    
    if row:
        try:
            audio_full_path = os.path.join(BASE_DIR, row[0])
            if os.path.exists(audio_full_path):
                os.remove(audio_full_path)
            
            pdf_full_path = os.path.join(app.config['UPLOAD_FOLDER'], row[1])
            if os.path.exists(pdf_full_path):
                os.remove(pdf_full_path)
        except Exception as e:
            print(f"⚠️ 文件删除警告: {e}")

        # 2. 删除数据库记录
        c.execute("DELETE FROM dialogues WHERE id=?", (id,))
        conn.commit()
        flash('🗑️ 课件已删除！')
    
    conn.close()
    return redirect(url_for('home'))
# ==============================

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        pdf_file = request.files.get('pdf_file')
        audio_file = request.files.get('audio_file')
        
        current_source = request.form.get('trans_source', TRANSLATION_SOURCE)

        if pdf_file and audio_file:
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            audio_file.save(audio_path)
            pdf_file.save(pdf_path)

            extracted_text = extract_text_from_pdf(pdf_path)
            grammar_data = analyze_text_with_gemini(extracted_text)

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            db_audio_path = f"static/uploads/{audio_file.filename}"
            c.execute("INSERT INTO dialogues (english_text, audio_path, grammar_json, source_filename, translator_source) VALUES (?, ?, ?, ?, ?)",
                      (extracted_text, db_audio_path, grammar_data, pdf_file.filename, current_source))
            conn.commit()
            conn.close()

            flash(f'✅ 发布成功！翻译使用: {current_source}')
            return redirect(url_for('admin'))

    return render_template('admin.html')

# ========= 🚑 急救路由 (修复数据库) =========
@app.route('/fix-db')
def fix_db():
    try:
        init_db()
        return f"<h1>✅ 数据库表已修复！</h1><p>路径: {DB_PATH}</p><a href='/'>返回首页</a>"
    except Exception as e:
        return f"<h1>❌ 修复失败: {e}</h1>"
# ==========================================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)