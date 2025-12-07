import google.generativeai as genai
import json

# ================= 配置区域 =================
# 1. 把你的 API KEY 填在这里
API_KEY = "AIzaSyDJnQnbDYM487X4XLEmDF-45vNo4jFbkIU"

# 2. 配置模型
genai.configure(api_key=API_KEY)

# 使用 gemini-2.5-flash，因为它速度快且免费额度高
# response_mime_type="application/json" 是关键！它强制 AI 只输出 JSON
model = genai.GenerativeModel( 'gemini-2.5-flash',
    generation_config={"response_mime_type": "application/json"}
)
# ===========================================

def analyze_sentence(text):
    print(f"🔄 正在请求 Gemini 分析句子: '{text}' ...")
    
    # 3. 编写提示词 (Prompt)
    # 这里的指令决定了 AI 给你返回什么格式的数据
    prompt = f"""
    你是一位专业的英语语法老师。请分析这个句子："{text}"

    请返回一个纯 JSON 对象，必须包含以下字段：
    1. "translation": 中文翻译
    2. "analysis": 一个对象，包含 "subject"(主语), "verb"(谓语), "object"(宾语)。
       - 如果某个成分不存在（比如不及物动词没有宾语），请填 null。
       - 只提取核心词。
    3. "tense": 句子的时态（中文）。
    """

    try:
        # 4. 发送请求
        response = model.generate_content(prompt)
        
        # 5. 解析结果
        # 因为我们强制了 JSON 模式，所以可以直接用 json.loads 解析
        result_json = json.loads(response.text)
        return result_json

    except Exception as e:
        print(f"❌ 出错了: {e}")
        return None

# ================= 测试区域 =================
if __name__ == "__main__":
    # 测试句子 1: 简单的主谓宾
    sentence1 = "The programmer wrote some code."
    data1 = analyze_sentence(sentence1)
    
    if data1:
        print("\n✅ 分析成功! 结果如下:")
        print(json.dumps(data1, ensure_ascii=False, indent=4))

    print("-" * 30)

    # 测试句子 2: 稍微复杂一点（不及物动词）
    sentence2 = "She serves in the army."
    data2 = analyze_sentence(sentence2)
    
    if data2:
        print("\n✅ 分析成功! 结果如下:")
        print(json.dumps(data2, ensure_ascii=False, indent=4))