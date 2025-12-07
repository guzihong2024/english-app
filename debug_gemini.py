import os
import google.generativeai as genai
import socket

# ================= 配置区域 =================
# 1. 再次填入你的 API Key
API_KEY = "AIzaSyDJnQnbDYM487X4XLEmDF-45vNo4jFbkIU" 

# 2. 你的代理端口 (Clash通常是7890, v2rayN通常是10809)
PROXY_PORT = "7890" 
# ===========================================

def get_wsl_host_ip():
    # 获取 WSL 宿主机 (Windows) 的真实 IP
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if 'nameserver' in line:
                    return line.split()[1]
    except:
        return "127.0.0.1"
    return "127.0.0.1"

def test_connection():
    print("-" * 30)
    print("🔍 开始 Gemini 连接诊断...")
    print(f"🔑 API Key 长度: {len(API_KEY)} (如果小于 30 肯定错了)")

    # 1. 尝试直接连接 (127.0.0.1)
    print("\n[尝试 1] 使用 localhost (127.0.0.1) 连接代理...")
    os.environ["HTTP_PROXY"] = f"http://127.0.0.1:{PROXY_PORT}"
    os.environ["HTTPS_PROXY"] = f"http://127.0.0.1:{PROXY_PORT}"
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    
    try:
        response = model.generate_content("Say hello")
        print("✅ 成功！方案 1 (Localhost) 可行！")
        print(f"🤖 AI 回复: {response.text}")
        return
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 2. 尝试使用 WSL 宿主机 IP 连接
    host_ip = get_wsl_host_ip()
    print(f"\n[尝试 2] 使用 Windows 宿主机 IP ({host_ip}) 连接代理...")
    print("⚠️ 注意：请确保你的代理软件开启了 'Allow LAN' (允许局域网连接) 功能！")
    
    os.environ["HTTP_PROXY"] = f"http://{host_ip}:{PROXY_PORT}"
    os.environ["HTTPS_PROXY"] = f"http://{host_ip}:{PROXY_PORT}"
    
    try:
        response = model.generate_content("Say hello")
        print(f"✅ 成功！方案 2 (Host IP) 可行！")
        print(f"ℹ️ 请把 app.py 里的代理 IP 改成: {host_ip}")
        print(f"🤖 AI 回复: {response.text}")
        return
    except Exception as e:
        print(f"❌ 失败: {e}")

    print("\nSUMMARY: 两次尝试都失败了。")
    print("1. 请检查 API Key 是否正确。")
    print("2. 请检查代理软件是否开启，端口是否为 " + PROXY_PORT)
    print("3. (重要) 如果是 WSL，请在代理软件设置中开启 'Allow LAN' 或 '允许来自局域网的连接'。")

if __name__ == "__main__":
    test_connection()