import os
import requests

# ===============================
# 配置区域
# ===============================
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN", "")
REPORTS_DIR = "./reports"
MAX_CHARS = 1900

# ===============================
# 读取有效报告
# ===============================
def load_reports(reports_dir):
    summary_list = []
    if not os.path.exists(reports_dir):
        print(f"⚠️ {reports_dir} 不存在，未生成报告")
        return ""
    
    files = sorted(os.listdir(reports_dir))
    for f in files:
        if f.endswith(".md") or f.endswith(".txt"):
            path = os.path.join(reports_dir, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content and "可能退市" not in content:  # 跳过无效股票
                    summary_list.append(content)
    
    if not summary_list:
        print("⚠️ 没有有效报告可推送")
    
    return "\n\n".join(summary_list)

# ===============================
# PushPlus 推送函数
# ===============================
def push_pushplus(text):
    if not PUSHPLUS_TOKEN:
        print("❌ PushPlus Token 未配置，无法推送")
        return
    
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n...(内容过长被截断)"
    
    url = "http://www.pushplus.plus/send"
    payload = {
        "token": PUSHPLUS_TOKEN,
        "title": "每日股票分析（汇总）",
        "content": text,
        "template": "html"
    }
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        result = res.json()
        if result.get("code") == 200:
            print(f"✅ PushPlus 推送成功: {result}")
        else:
            print(f"❌ PushPlus 推送失败: {result}")
    except Exception as e:
        print(f"❌ PushPlus 推送异常: {e}")

# ===============================
# 主程序
# ===============================
if __name__ == "__main__":
    summary_text = load_reports(REPORTS_DIR)
    if summary_text:
        push_pushplus(summary_text)
    else:
        print("⚠️ 没有生成有效报告内容，跳过推送")
