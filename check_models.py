import google.generativeai as genai

# ⚠️ 记得填你的 Key
genai.configure(api_key="AIzaSyDJnQnbDYM487X4XLEmDF-45vNo4jFbkIU")

print("正在查询可用模型列表...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"查询失败: {e}")